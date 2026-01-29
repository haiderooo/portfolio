import pandas as pd
import nltk
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder
from nltk.collocations import TrigramAssocMeasures, TrigramCollocationFinder
from collections import Counter
import json

# 1. LOAD ALL STOPWORD SOURCES
with open(r"D:\sem3\DH\Final Project\Finalized\Analysis\stopwords\master_urdu_stopwords.txt", 'r', encoding='utf-8') as f:
    master_urdu_stops = set(json.load(f))

roman_df = pd.read_csv(r"D:\sem3\DH\Final Project\Finalized\Analysis\stopwords\RomanUrdu_stopwords.csv", encoding='utf-8')
roman_stops = set(roman_df['word'].astype(str).str.lower().tolist())

custom_df = pd.read_csv(r"D:\sem3\DH\Final Project\Finalized\Analysis\stopwords\my_custom_stopwords.csv", encoding='utf-8')
custom_stops = set(custom_df['word'].astype(str).str.lower().tolist())

nltk.download('stopwords')
from nltk.corpus import stopwords
en_stops = set(stopwords.words('english'))

all_stops = master_urdu_stops.union(roman_stops).union(custom_stops).union(en_stops)

# 2. LOAD AND CLEAN CORPUS
df = pd.read_csv(r"D:\sem3\DH\Final Project\Finalized\Clean\final_clean_cmnts1.csv", encoding='utf-8')

def clean_tokens(text):
    words = str(text).lower().split()
    return [w for w in words if w not in all_stops and len(w) > 2]

all_tokens = []
for comment in df['comment_text']:
    all_tokens.extend(clean_tokens(comment))

# 3. STATISTICAL DISCOVERY
# UNIGRAMS: Pure Frequency (The most common substantive words)
unigram_counts = Counter(all_tokens).most_common(200)
uni_df = pd.DataFrame(unigram_counts, columns=['word', 'frequency'])

# BIGRAMS: PMI (The strongest two-word semantic bonds)
bigram_measures = BigramAssocMeasures()
finder2 = BigramCollocationFinder.from_words(all_tokens)
finder2.apply_freq_filter(3) 
top_bigrams = finder2.score_ngrams(bigram_measures.pmi)

# TRIGRAMS: PMI (The strongest three-word semantic bonds)
trigram_measures = TrigramAssocMeasures()
finder3 = TrigramCollocationFinder.from_words(all_tokens)
finder3.apply_freq_filter(2)
top_trigrams = finder3.score_ngrams(trigram_measures.pmi)

# 4. EXPORT
bg_df = pd.DataFrame([{'phrase': " ".join(k), 'pmi_score': v} for k, v in top_bigrams])
tg_df = pd.DataFrame([{'phrase': " ".join(k), 'pmi_score': v} for k, v in top_trigrams])

with pd.ExcelWriter('Colonial_Signifier_Candidates.xlsx') as writer:
    uni_df.to_excel(writer, sheet_name='Unigram_Candidates', index=False)
    bg_df.to_excel(writer, sheet_name='Bigram_Candidates', index=False)
    tg_df.to_excel(writer, sheet_name='Trigram_Candidates', index=False)

print(f"Total tokens analyzed: {len(all_tokens)}")
print("Candidate list generated in 'Colonial_Signifier_Candidates.xlsx'")
