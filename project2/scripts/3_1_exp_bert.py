import pandas as pd
from bertopic import BERTopic
from umap import UMAP
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer

# 1. LOAD DATA
# Ensure this is your clean, original corpus
df_original = pd.read_csv(r"D:\sem3\DH\Final Project\Finalized\Clean\final_clean_cmnts1.csv", encoding="utf-8-sig")
docs = df_original["comment_text"].astype(str).tolist()

# 2. COMPONENT SETUP (Reproducibility & Quality)
umap_model = UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric='cosine', random_state=42)
hdbscan_model = HDBSCAN(min_cluster_size=15, min_samples=5, metric='euclidean', cluster_selection_method='eom', prediction_data=True)

# Urdu-aware Vectorizer
urdu_regex = r"(?u)\b\w\w+\b|[\u0600-\u06FF]+"
vectorizer_model = CountVectorizer(token_pattern=urdu_regex, stop_words=None)

# 3. INITIALIZE & RUN
print("Starting BERTopic fit_transform... This may take a moment.")
topic_model = BERTopic(
    umap_model=umap_model,
    hdbscan_model=hdbscan_model,
    vectorizer_model=vectorizer_model,
    calculate_probabilities=True,
    verbose=True
)

topics, probs = topic_model.fit_transform(docs)

# 4. CREATE THE MASTER MAPPED CSV (1,439 Rows)
master_df = topic_model.get_document_info(docs)
final_mapped_df = pd.concat([df_original.reset_index(drop=True), 
                            master_df.drop(columns=['Document'])], axis=1)

# 5. EXPORT EVERYTHING
final_mapped_df.to_csv("BERTopic_Master_Map.csv", index=False, encoding="utf-8-sig")
topic_model.get_topic_info().to_csv("BERTopic_Topic_Summary.csv", index=False, encoding="utf-8-sig")

# Visualizations
topic_model.visualize_topics().write_html("BERTopic_Intertopic_Map.html")
topic_model.visualize_barchart(top_n_topics=15).write_html("BERTopic_Keywords.html")

# 6. SAVE THE MODEL OBJECT (New Section)
# This creates a folder/file containing the 'brain' of your analysis
topic_model.save("GB_Colonialism_Model", serialization="safetensors", save_ctfidf=True)

print("Analysis Complete. Model saved to folder: 'GB_Colonialism_Model'")
