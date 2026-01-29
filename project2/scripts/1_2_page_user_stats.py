import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the dataset
# Ensure your file is named 'gb_comments.csv' or update the path below
df = pd.read_csv(r"D:\sem3\DH\Final Project\Finalized\Clean\final_clean_cmnts1.csv")

# Pre-processing: Calculate word counts for structural metrics
df['comment_length'] = df['comment_text'].apply(lambda x: len(str(x).split()))

# --- 1. COMPARISON BY PAGE NAME ---
page_stats = df.groupby('page_name').agg(
    num_posts=('post_id', 'nunique'),
    num_comments=('comment_text', 'count'),
    total_words=('comment_length', 'sum'),
    avg_comment_length=('comment_length', 'mean')
).reset_index()

# Calculate Replies per Comment Ratio
# Note: reply_no > 0 indicates the entry is a reply to a parent comment
replies_count = df[df['reply_no'] > 0].groupby('page_name')['reply_no'].count()
page_stats['replies_per_comment_ratio'] = page_stats['page_name'].map(replies_count) / page_stats['num_comments']
page_stats['replies_per_comment_ratio'] = page_stats['replies_per_comment_ratio'].fillna(0)

# Visualization 1: Page Distribution (Comments & Length)
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
sns.barplot(data=page_stats, x='page_name', y='num_comments', ax=axes[0], palette='viridis')
axes[0].set_title('Total Comments per Page', fontsize=14)
axes[0].tick_params(axis='x', rotation=45)

sns.barplot(data=page_stats, x='page_name', y='avg_comment_length', ax=axes[1], palette='magma')
axes[1].set_title('Average Comment Length (Words) per Page', fontsize=14)
axes[1].tick_params(axis='x', rotation=45)
plt.tight_layout()
plt.savefig('page_structural_analysis.png', bbox_inches='tight')

# NEW: Visualization 1b: Replies to Comments Ratio per Page
plt.figure(figsize=(10, 6))
sns.barplot(data=page_stats, x='page_name', y='replies_per_comment_ratio', palette='coolwarm')
plt.title('Deliberation Index: Replies-to-Comments Ratio by Page', fontsize=14)
plt.ylabel('Ratio (Replies / Total Comments)')
plt.xlabel('Page Name')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig('page_reply_ratio.png', bbox_inches='tight', dpi=300)
plt.close()

# --- 2. USERNAME ANALYSIS ---
user_grouped = df.groupby('username_anonymised').agg(
    num_comments=('comment_text', 'count'),
    total_user_words=('comment_length', 'sum'),
    mean_len=('comment_length', 'mean'),
    median_len=('comment_length', 'median'),
    max_len=('comment_length', 'max'),
    min_len=('comment_length', 'min')
).reset_index()

unique_usernames = user_grouped['username_anonymised'].nunique()
avg_comments_per_user = user_grouped['num_comments'].mean()
users_more_than_one = len(user_grouped[user_grouped['num_comments'] > 1])
correlation = user_grouped['num_comments'].corr(user_grouped['total_user_words'])

# Percentage of total corpus words by user activity levels
total_corpus_words = user_grouped['total_user_words'].sum()
user_grouped['word_perc'] = (user_grouped['total_user_words'] / total_corpus_words) * 100

# Visualization 2: Correlation with Line of Best Fit
plt.figure(figsize=(10, 6))
sns.regplot(data=user_grouped, x='num_comments', y='total_user_words', 
            scatter_kws={'alpha':0.5}, line_kws={"color": "red"})
plt.title(f'Correlation: Num Comments vs Total Words (r={correlation:.2f})', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.savefig('user_correlation.png', bbox_inches='tight')

# Visualization 3: Pie Chart of Word Contribution (Fixed Labels)
def activity_tier(n):
    if n == 1: return 'Single Comment Users'
    if 1 < n <= 5: return 'Occasional (2-5)'
    return 'Frequent (>5)'

user_grouped['tier'] = user_grouped['num_comments'].apply(activity_tier)
tier_data = user_grouped.groupby('tier')['word_perc'].sum()

plt.figure(figsize=(10, 10))
plt.pie(tier_data, labels=tier_data.index, autopct='%1.1f%%', 
        colors=sns.color_palette('pastel'), startangle=140, pctdistance=0.85)
plt.title('Percentage of Total Corpus Words by User Activity Tier', fontsize=14, pad=20)
plt.savefig('word_contribution_pie.png', bbox_inches='tight', dpi=300)
plt.close()

# --- 3. DISTRIBUTION CHART: USERS VS LENGTH ---
plt.figure(figsize=(10, 6))
sns.histplot(user_grouped['mean_len'], bins=30, kde=True, color='teal')
plt.xlabel('Average Length of Comments (Words)')
plt.ylabel('Number of Users')
plt.title('Distribution of Users by Average Comment Length', fontsize=12)
plt.savefig('user_length_distribution.png', bbox_inches='tight')

# --- EXPORT TO EXCEL ---
user_summary_stats = pd.DataFrame({
    'Metric': ['Unique Usernames', 'Avg Comments per User', 'Users with >1 Comment', 'Comment-Length Correlation'],
    'Value': [unique_usernames, avg_comments_per_user, users_more_than_one, correlation]
})

with pd.ExcelWriter('structural_analysis_summary.xlsx', engine='openpyxl') as writer:
    page_stats.to_excel(writer, sheet_name='Page Comparison', index=False)
    user_summary_stats.to_excel(writer, sheet_name='User General Stats', index=False)
    user_grouped.to_excel(writer, sheet_name='Per User Data', index=False)

print("Analysis complete. Check 'page_reply_ratio.png' for the new visualization.")
