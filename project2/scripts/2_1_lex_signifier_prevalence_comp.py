import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from arabic_reshaper import reshape
from bidi.algorithm import get_display

# --- 1. LOAD THE DATA GENERATED FROM PREVIOUS SCRIPT ---
try:
    # This reads the CSV we just created
    summary_df = pd.read_csv("Signifier_Prevalence_Comparison.csv")
except FileNotFoundError:
    print("Error: Signifier_Prevalence_Comparison.csv not found. Please run the calculation script first.")
    exit()

# --- 2. URDU RENDERING HELPER ---
def fix_urdu(text):
    if any("\u0600" <= c <= "\u06FF" for c in text):
        return get_display(reshape(text))
    return text

# --- 3. CREATE THE VISUALIZATION ---
plt.figure(figsize=(10, 7))

# Set a clean aesthetic
sns.set_style("whitegrid")

# Create the bar plot
# We use a custom palette to distinguish between 'diluted' and 'concentrated'
plot = sns.barplot(
    data=summary_df, 
    x='Metric', 
    y='Prevalence (%)', 
    palette=['#95a5a6', '#e74c3c']  # Grey for total, Red for substantive
)

# Add the percentage values on top of the bars for clarity
for p in plot.patches:
    plot.annotate(format(p.get_height(), '.3f') + '%', 
                   (p.get_x() + p.get_width() / 2., p.get_height()), 
                   ha = 'center', va = 'center', 
                   xytext = (0, 9), 
                   textcoords = 'offset points',
                   fontsize=12, fontweight='bold')

# --- 4. FORMATTING THE LABELS ---
plt.title(fix_urdu("Lexical Density: Colonial Signifiers in Perspective"), fontsize=16, pad=20)
plt.ylabel("Prevalence (%)", fontsize=12)
plt.xlabel("Calculation Baseline", fontsize=12)

# Adjust the Y-axis to give some breathing room for the annotations
plt.ylim(0, summary_df['Prevalence (%)'].max() * 1.2)

# Ensure no labels are cropped
plt.tight_layout()

# Save the output
plt.savefig("Signifier_Prevalence_Comparison_Chart.png", dpi=300)
plt.show()

print("Visualization saved as 'Signifier_Prevalence_Comparison_Chart.png'")
