import pandas as pd
import re
import nltk
from nltk.corpus import stopwords

# Ensure NLTK English stopwords are downloaded
nltk.download('stopwords', quiet=True)

# --- 1. LOAD DATA ---
df = pd.read_csv(r"D:\sem3\DH\Final Project\Finalized\Clean\final_clean_cmnts1.csv")
col_lex = pd.read_csv(r"D:\sem3\DH\Final Project\Finalized\Analysis\co_occurence_matrix\ref_col_terms.csv", encoding='utf-8-sig')
col_signifiers = set(col_lex['word'].dropna().astype(str).str.lower().str.strip())

# --- 2. LOAD STOPWORDS FROM ALL 4 SOURCES ---
# 1) English (NLTK)
stop_eng = set(stopwords.words('english'))

# 2) Urdu (txt file - assuming one word per line)
try:
    with open(r"D:\sem3\DH\Final Project\Finalized\Analysis\stopwords\master_urdu_stopwords.txt", 'r', encoding='utf-8') as f:
        stop_urdu = set(line.strip() for line in f)
except FileNotFoundError:
    stop_urdu = set()
    print("Warning: urdu_stopwords.txt not found.")

# 3) Roman Urdu (csv - assuming a 'word' column)
try:
    stop_roman = set(pd.read_csv(r"D:\sem3\DH\Final Project\Finalized\Analysis\stopwords\RomanUrdu_stopwords.csv")['word'].astype(str).str.lower().str.strip())
except FileNotFoundError:
    stop_roman = set()
    print("Warning: roman_urdu_stopwords.csv not found.")

# 4) Custom Stopwords (csv - assuming a 'word' column)
try:
    stop_custom = set(pd.read_csv(r"D:\sem3\DH\Final Project\Finalized\Analysis\stopwords\my_custom_stopwords.csv")['word'].astype(str).str.lower().str.strip())
except FileNotFoundError:
    stop_custom = set()
    print("Warning: custom_stopwords.csv not found.")

# Combine all into one Substantive Filter
all_stopwords = stop_eng | stop_urdu | stop_roman | stop_custom

# --- 3. THE CALCULATION LOGIC ---
all_tokens = []
for comment in df['comment_text'].astype(str).str.lower():
    # Basic tokenization by splitting on whitespace/punctuation
    tokens = re.findall(r'\b\w+\b', comment)
    all_tokens.extend(tokens)

total_word_count = len(all_tokens)
substantive_tokens = [t for t in all_tokens if t not in all_stopwords]
substantive_word_count = len(substantive_tokens)

# Count Signifiers
signifier_hits = sum(1 for t in all_tokens if t in col_signifiers)

# --- 4. RESULTS GENERATION ---
prevalence_all = (signifier_hits / total_word_count) * 100 if total_word_count > 0 else 0
prevalence_substantive = (signifier_hits / substantive_word_count) * 100 if substantive_word_count > 0 else 0

# --- 5. OUTPUT REPORT ---
print("--- COLONIAL SIGNIFIER PREVALENCE REPORT ---")
print(f"Total Words in Corpus: {total_word_count:,}")
print(f"Substantive Words (Non-Stopwords): {substantive_word_count:,}")
print(f"Total Colonial Signifier Hits: {signifier_hits:,}")
print("-" * 40)
print(f"Prevalence among ALL words: {prevalence_all:.4f}%")
print(f"Prevalence among SUBSTANTIVE words: {prevalence_substantive:.4f}%")
print("-" * 40)

# Create a small summary table for your thesis
summary_df = pd.DataFrame({
    'Metric': ['Total Corpus', 'Substantive Only'],
    'Prevalence (%)': [prevalence_all, prevalence_substantive]
})
summary_df.to_csv("Signifier_Prevalence_Comparison.csv", index=False)
