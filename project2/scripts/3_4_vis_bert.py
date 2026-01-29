import pandas as pd
from bertopic import BERTopic
import matplotlib.pyplot as plt
import seaborn as sns
import arabic_reshaper
from bidi.algorithm import get_display
import matplotlib.font_manager as fm
from sklearn.metrics.pairwise import cosine_similarity

# --- 1. LOAD THE MODEL ---
# Point this to the folder created by your fit_transform script
MODEL_PATH = "GB_Colonialism_Model"
topic_model = BERTopic.load(MODEL_PATH)

# --- 2. URDU RENDERING CONFIGURATION ---
configuration = {
    'delete_harakat': True,
    'support_unshaped_char': True,
    'language': 'Urdu'
}
reshaper = arabic_reshaper.ArabicReshaper(configuration)

def fix_urdu(text):
    if not text or not isinstance(text, str): return text
    return get_display(reshaper.reshape(text))

# Path to Jameel Noori font
font_path = 'C:/Windows/Fonts/Jameel Noori Nastaleeq.ttf' 
urdu_font = fm.FontProperties(fname=font_path, size=12)

# --- 3. GENERATE SEMANTIC SIMILARITY HEATMAP ---
def save_similarity_heatmap(model):
    print("Generating Similarity Heatmap...")
    embeddings = model.topic_embeddings_
    sim_matrix = cosine_similarity(embeddings)
    
    # Create labels using Top 2 words per topic
    labels = []
    for i in range(len(embeddings)):
        topic_id = i - 1
        words = model.get_topic(topic_id)
        if words:
            urdu_label = " | ".join([w[0] for w in words[:2]])
            labels.append(f"T{topic_id}: {fix_urdu(urdu_label)}")
        else:
            labels.append(f"T{topic_id}")

    plt.figure(figsize=(16, 12))
    sns.heatmap(sim_matrix, cmap="YlGnBu", xticklabels=labels, yticklabels=labels, square=True)
    
    ax = plt.gca()
    for label in ax.get_xticklabels(): label.set_fontproperties(urdu_font)
    for label in ax.get_yticklabels(): label.set_fontproperties(urdu_font)
    
    plt.title("Topic Semantic Overlap Matrix", fontsize=16)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig("Thesis_Topic_Similarity.png", dpi=300)
    print("Saved: Thesis_Topic_Similarity.png")

# --- 4. GENERATE HIERARCHICAL DENDROGRAM ---
def save_hierarchy_plot(model):
    print("Generating Hierarchical Dendrogram...")
    # BERTopic has a built-in viz, but we want to control the labels for Urdu
    fig = model.visualize_hierarchy(width=1000, height=600)
    # This saves as HTML so you can hover over nodes
    fig.write_html("Thesis_Topic_Hierarchy.html")
    print("Saved: Thesis_Topic_Hierarchy.html")

# --- 5. GENERATE COLONIAL-SPECIFIC BARCHARTS ---
def save_colonial_barcharts(model, top_n_topics=10):
    print("Generating c-TF-IDF Barcharts...")
    # This identifies the most distinctive words for your top topics
    fig = model.visualize_barchart(top_n_topics=top_n_topics, n_words=10)
    fig.write_html("Thesis_Topic_Word_Profiles.html")
    print("Saved: Thesis_Topic_Word_Profiles.html")

# EXECUTE ALL
save_similarity_heatmap(topic_model)
save_hierarchy_plot(topic_model)
save_colonial_barcharts(topic_model)
