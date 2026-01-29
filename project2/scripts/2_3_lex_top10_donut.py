import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from arabic_reshaper import reshape
from bidi.algorithm import get_display
import re

# --- 1. LOAD DATA ---
# Using the output from your previous script
df = pd.read_csv('Corpus_with_Colonial_Signifier_Metrics.csv')
top_10_data = pd.read_csv('Top_10_Colonial_Signifiers_Frequency.csv')

# --- 2. URDU RENDERING HELPER ---
def fix_urdu(text):
    if any("\u0600" <= c <= "\u06FF" for c in text):
        # Reshape for cursive joining and apply Bidi for RTL direction
        reshaped_text = reshape(text)
        return get_display(reshaped_text)
    return text

# --- 3. VISUALIZATION 1: TOP 10 COLONIAL SIGNIFIERS ---
plt.figure(figsize=(12, 7))

# Apply the Urdu fix to the labels
top_10_data['Display_Word'] = top_10_data['Signifier'].apply(fix_urdu)

sns.barplot(
    data=top_10_data, 
    x='Count', 
    y='Display_Word', 
    palette='Reds_r'
)

plt.title(fix_urdu("Top 10 Prevalent Colonial Signifiers"), fontsize=16, pad=20)
plt.xlabel("Frequency (Number of Occurrences)", fontsize=12)
plt.ylabel("Signifier", fontsize=12)
plt.grid(axis='x', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig("Top10_Signifiers_Urdu_Corrected.png", dpi=300)
plt.show()

# --- 4. VISUALIZATION 2: CORPUS PREVALENCE (DONUT CHART) ---
# Calculate counts
total_comments = len(df)
colonial_count = df['invokes_colonial_frame'].sum()
neutral_count = total_comments - colonial_count

# Data for plotting
labels = ['Invokes Colonial Frame', 'Neutral/General Discourse']
sizes = [colonial_count, neutral_count]
colors = ['#d73027', '#4575b4'] # Red for Colonial, Blue for Neutral

fig, ax = plt.subplots(figsize=(10, 8))

# Create the pie chart
wedges, texts, autotexts = ax.pie(
    sizes, 
    labels=labels, 
    autopct=lambda p: '{:.1f}%\n({:,.0f})'.format(p, p * sum(sizes) / 100),
    startangle=140, 
    colors=colors,
    pctdistance=0.85, # Position of the percentage labels
    explode=(0.05, 0),  # Slightly pull out the colonial slice
    textprops={'fontsize': 12, 'fontweight': 'bold'}
)

# Draw a circle at the center to turn the pie into a donut
centre_circle = plt.Circle((0,0), 0.70, fc='white')
fig.gca().add_artist(centre_circle)

# Adjust label layout to prevent cropping
plt.setp(texts, size=11)
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.title("Prevalence of Colonial Signifiers in Corpus", fontsize=16, pad=20)

# This is the key to prevent cropping:
plt.tight_layout() 
plt.subplots_adjust(top=0.9) # Give title extra room

plt.savefig("Colonial_Prevalence_Donut.png", dpi=300, bbox_inches='tight')
plt.show()

print(f"Visualizations saved: \n1. Top10_Signifiers_Urdu_Corrected.png \n2. Colonial_Prevalence_Donut.png")
