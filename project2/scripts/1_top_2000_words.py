import pandas as pd
from collections import Counter
import re

# Load the dataset with UTF-8 encoding to ensure Urdu script is read correctly
df = pd.read_csv(r"D:\sem3\DH\Final Project\Finalized\Clean\final_clean_cmnts1.csv", encoding='utf-8')

# Ensure the comment_text column is treated as string and handle potential NaNs
text_data = df['comment_text'].astype(str).tolist()

# Combine all comments into one large string
full_corpus = " ".join(text_data)

# Tokenize: splitting by whitespace is the 'purest' way to see raw strings.
# This preserves both Urdu script and Roman characters.
words = full_corpus.split()

# Count frequencies
word_counts = Counter(words)

# Get the 2000 most frequent words
top_2000 = word_counts.most_common(2000)

# Convert to DataFrame for easy export and viewing
df_freq = pd.DataFrame(top_2000, columns=['Word', 'Frequency'])

# Save to CSV with UTF-8 encoding (specifically 'utf-8-sig' for Excel compatibility with Urdu)
df_freq.to_csv('top_2000_raw_frequencies.csv', index=False, encoding='utf-8-sig')

print(f"Extraction complete. {len(df_freq)} words saved to 'top_2000_raw_frequencies.csv'.")

# Optional: Display the top 15 just to verify Urdu rendering in your console
print("\nTop 15 Raw Words:")
print(df_freq.head(15))
