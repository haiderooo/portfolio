import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
from arabic_reshaper import reshape
from bidi.algorithm import get_display

# --- 1. LOAD DATA ---
# This file should have columns: ['comment_text', 'Topic', 'author_id', 'reply_no']
df = pd.read_csv(r"D:\sem3\DH\Final Project\Finalized\Analysis\bertopic\BERTopic_Master_Map.csv") 

col_lex = pd.read_csv(r"D:\sem3\DH\Final Project\Finalized\Analysis\co_occurence_matrix\ref_col_terms.csv", encoding='utf-8-sig')
neu_lex = pd.read_csv(r"D:\sem3\DH\Final Project\Finalized\Analysis\co_occurence_matrix\ref_ntrl_terms.csv", encoding='utf-8-sig')

col_words = set(col_lex['word'].dropna().astype(str).str.lower().str.strip())
neu_words = set(neu_lex['word'].dropna().astype(str).str.lower().str.strip())

# --- 2. DEFINE ANALYSIS FUNCTIONS ---
def get_lexical_stats(text):
    tokens = re.findall(r'\b\w+\b', str(text).lower())
    if not tokens: return 0, 0, 0
    c_hits = sum(1 for t in tokens if t in col_words)
    n_hits = sum(1 for t in tokens if t in neu_words)
    return len(tokens), c_hits, n_hits

# Apply stats to every comment
df[['word_count', 'col_hits', 'neu_hits']] = df['comment_text'].apply(
    lambda x: pd.Series(get_lexical_stats(x))
)

# --- 3. AGGREGATE PER TOPIC ---
topic_stats = df.groupby('Topic').agg({
    'comment_text': 'count',
    'word_count': 'mean',
    'col_hits': 'sum',
    'neu_hits': 'sum'
}).rename(columns={'comment_text': 'Comment_Count', 'word_count': 'Avg_Length'})

# Calculate Colonial Density: (Total Colonial Hits in Topic / Total Words in Topic)
total_words_per_topic = df.groupby('Topic')['word_count'].sum()
topic_stats['Colonial_Signifier_Density'] = (topic_stats['col_hits'] / total_words_per_topic) * 100

# Calculate "Thematic Bias" - Ratio of Colonial to Neutral terms
topic_stats['Colonial_to_Neutral_Ratio'] = topic_stats['col_hits'] / (topic_stats['neu_hits'] + 1)

# --- 4. VISUALIZATION 1: COLONIAL DENSITY BY TOPIC ---
plt.figure(figsize=(14, 7))
# Sort topics by density to see the "hotspots"
plot_df = topic_stats.sort_values('Colonial_Signifier_Density', ascending=False).reset_index()

sns.barplot(data=plot_df, x='Topic', y='Colonial_Signifier_Density', palette='Reds_r', order=plot_df['Topic'])
plt.title("Colonial Signifier Density Across BERTopic Clusters", fontsize=15)
plt.ylabel("Density (% of words that are Colonial Signifiers)")
plt.xlabel("BERTopic ID")
plt.savefig("Topic_Colonial_Density.png", bbox_inches='tight')

# --- 5. VISUALIZATION 2: COMMENT VOLUME VS. COLONIAL INTENSITY ---
plt.figure(figsize=(12, 8))
sns.scatterplot(data=topic_stats, x='Comment_Count', y='Colonial_Signifier_Density', 
                size='Avg_Length', hue='Colonial_Signifier_Density', palette='viridis', sizes=(100, 1000))

# FIXED LABELING LOOP: iterates over the dataframe index safely
for idx, row in topic_stats.iterrows():
    plt.text(row['Comment_Count'] + 1, # Small offset to the right
             row['Colonial_Signifier_Density'], 
             str(idx), # This is the Topic ID
             fontsize=10, 
             weight='bold',
             va='center')

plt.title("Topic Volume vs. Colonial Signifier Intensity", fontsize=15)
plt.xlabel("Number of Comments in Topic")
plt.ylabel("Colonial Signifier Density (%)")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("Topic_Volume_vs_Intensity_Fixed.png", bbox_inches='tight')
# --- 6. EXPORT STATS ---
topic_stats.to_csv("BERTopic_Colonial_Analysis.csv")
print("Analysis complete. Check 'BERTopic_Colonial_Analysis.csv' for full stats.")
