import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
# Ensure your file is named 'gb_comments.csv' or update the path below
df = pd.read_csv(r"D:\sem3\DH\Final Project\Finalized\Clean\final_clean_cmnts1.csv")

# 1. Save PNG of first 5 rows
# This creates a clean visual snippet of your cleaned data
fig, ax = plt.subplots(figsize=(15, 3)) 
ax.axis('off')
table = ax.table(cellText=df.head().values, colLabels=df.columns, loc='center', cellLoc='left')
table.auto_set_font_size(False)
table.set_fontsize(9)
plt.savefig('first_5_rows.png', bbox_inches='tight', dpi=300)
plt.close()

# 2. Descriptive Stats Calculations
# Basic Counts
unique_posts = df['post_id'].nunique()
unique_users = df['username_anonymised'].nunique()
total_comments = len(df)
num_replies = len(df[df['reply_no'] > 0])
percent_replies = (num_replies / total_comments) * 100

# Page-wise Distribution
page_distribution = df.groupby('page_name').agg(
    post_count=('post_id', 'nunique'),
    comment_count=('comment_text', 'count')
).reset_index()

# Textual Stats (Word Counts)
df['word_count'] = df['comment_text'].apply(lambda x: len(str(x).split()))

text_stats = {
    'Total Words in Corpus': df['word_count'].sum(),
    'Max Words (Single Comment)': df['word_count'].max(),
    'Min Words (Single Comment)': df['word_count'].min(),
    'Mean Words per Comment': df['word_count'].mean(),
    'Median Words per Comment': df['word_count'].median(),
    'Mode Words per Comment': df['word_count'].mode()[0]
}

# Engagement Stats per Post
comments_per_post = df.groupby('post_id')['comment_text'].count()
post_stats = {
    'Mean Comments per Post': comments_per_post.mean(),
    'Median Comments per Post': comments_per_post.median(),
    'Mode Comments per Post': comments_per_post.mode()[0] if not comments_per_post.mode().empty else 0,
    'Max Comments per Post': comments_per_post.max(),
    'Min Comments per Post': comments_per_post.min()
}

# User Activity Stats
comments_per_user = df.groupby('username_anonymised')['comment_text'].count()
user_stats = {
    'Mean Comments per User': comments_per_user.mean(),
    'Median Comments per User': comments_per_user.median(),
    'Max Comments per User': comments_per_user.max(),
    'Min Comments per User': comments_per_user.min()
}

# 3. Consolidating into DataFrames for Export
summary_general = pd.DataFrame({
    'Metric': ['Total Rows', 'Total Columns', 'Unique Posts', 'Unique Users', 'Total Comments', 'Total Replies', 'Percentage of Replies'],
    'Value': [len(df), len(df.columns), unique_posts, unique_users, total_comments, num_replies, f"{percent_replies:.2f}%"]
})

summary_text = pd.DataFrame(list(text_stats.items()), columns=['Metric', 'Value'])
summary_post_eng = pd.DataFrame(list(post_stats.items()), columns=['Metric', 'Value'])
summary_user_eng = pd.DataFrame(list(user_stats.items()), columns=['Metric', 'Value'])

# 4. Exporting to Excel with Multiple Sheets
# Note: Requires 'openpyxl' library installed (pip install openpyxl)
with pd.ExcelWriter('gb_land_reforms_descriptive_stats.xlsx', engine='openpyxl') as writer:
    summary_general.to_excel(writer, sheet_name='General Overview', index=False)
    page_distribution.to_excel(writer, sheet_name='Page Distribution', index=False)
    summary_text.to_excel(writer, sheet_name='Text Analysis', index=False)
    summary_post_eng.to_excel(writer, sheet_name='Post Stats', index=False)
    summary_user_eng.to_excel(writer, sheet_name='User Stats', index=False)

print("Success! 'first_5_rows.png' and 'gb_land_reforms_descriptive_stats.xlsx' have been created.")
