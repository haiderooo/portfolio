import pandas as pd

# 1. LOAD THE MASTER MAPPED DATA
# This assumes you have the file from the "Clean Slate" BERTopic run
df = pd.read_csv("BERTopic_Master_Map.csv", encoding="utf-8-sig")

# 2. DEFINE THE EXTRACTION LOGIC
def get_top_representative(group):
    # Sort by probability to get the most "prototypical" comments first
    # If probabilities are equal, it maintains the original order
    return group.sort_values(by='Probability', ascending=False).head(15)

# 3. APPLY TO EACH TOPIC
# We group by 'Topic' and apply our top-15 filter
top_representative_df = df.groupby('Topic', group_keys=False).apply(get_top_representative)

# 4. SORT FOR READABILITY
# This ensures the CSV starts with Topic -1, then 0, 1, 2...
top_representative_df = top_representative_df.sort_values(by=['Topic', 'Probability'], ascending=[True, False])

# 5. EXPORT THE CONSOLIDATED FILE
output_filename = "BERTopic_Top15_Per_Topic_Consolidated.csv"
top_representative_df.to_csv(output_filename, index=False, encoding="utf-8-sig")

# 6. PRINT SUMMARY FOR VERIFICATION
print(f"Consolidated file created: {output_filename}")
print(f"Total rows in sample: {len(top_representative_df)}")
print("\nTopic Breakdown in Sample:")
print(top_representative_df['Topic'].value_counts().sort_index())
