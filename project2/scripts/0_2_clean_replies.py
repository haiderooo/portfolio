import pandas as pd
import re

def extract_and_clean_usernames(csv_path, comment_column='comment_text', output_path='cleaned_comments.csv'):
    """
    Extract usernames from comment text and create a new column while cleaning the original.
    
    Parameters:
    -----------
    csv_path : str
        Path to your CSV file
    comment_column : str
        Name of the column containing comment text (default: 'comment_text')
    output_path : str
        Path for the output CSV file (default: 'cleaned_comments.csv')
    
    Returns:
    --------
    pandas.DataFrame
        DataFrame with new 'replied_to_username' column and cleaned comment text
    """
    
    # Read the CSV with UTF-8 encoding for Urdu/South Asian scripts
    df = pd.read_csv(csv_path, encoding='utf-8')
    
    # Function to extract username from comment
    def extract_username(text):
        if pd.isna(text):
            return None
        # Match @username pattern (assuming usernames are alphanumeric, underscores, dots)
        # This captures the first @mention at the start of the comment
        match = re.match(r'^@([\w.]+)\s*', str(text))
        if match:
            return match.group(1)
        return None
    
    # Function to remove username from comment text
    def remove_username(text):
        if pd.isna(text):
            return text
        # Remove @username from the beginning of the text
        cleaned = re.sub(r'^@[\w.]+\s*', '', str(text))
        return cleaned.strip()
    
    # Create new column with extracted usernames
    df['replied_to_username'] = df[comment_column].apply(extract_username)
    
    # Clean the comment text column
    df[comment_column] = df[comment_column].apply(remove_username)
    
    # Save to new CSV with UTF-8 encoding and BOM for Excel compatibility
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    
    print(f"Processing complete!")
    print(f"Total comments: {len(df)}")
    print(f"Comments with replies: {df['replied_to_username'].notna().sum()}")
    print(f"Output saved to: {output_path}")
    
    return df

# If you want to see a preview of what changed:
def preview_changes(csv_path, comment_column='comment_text', n=5):
    """
    Preview the first n comments that have usernames to see the extraction.
    """
    df = pd.read_csv(csv_path, encoding='utf-8')
    
    # Find comments with @mentions
    has_username = df[comment_column].str.match(r'^@[\w.]+\s*', na=False)
    sample = df[has_username].head(n)
    
    print("Preview of comments with usernames:\n")
    for idx, row in sample.iterrows():
        original = row[comment_column]
        username = re.match(r'^@([\w.]+)\s*', str(original))
        if username:
            cleaned = re.sub(r'^@[\w.]+\s*', '', str(original)).strip()
            print(f"Original: {original}")
            print(f"Username: @{username.group(1)}")
            print(f"Cleaned: {cleaned}")
            print("-" * 80)

# ============================================================================
# RUN THE SCRIPT - Your actual file processing happens here
# ============================================================================

# Step 1: Preview the changes (optional - shows first 5 comments with usernames)
print("STEP 1: Previewing changes...\n")
preview_changes('raw_consol_cmnts.csv', comment_column='comment_text', n=5)

# Step 2: Process the full file
print("\n" + "="*80)
print("STEP 2: Processing full file...\n")
df = extract_and_clean_usernames(
    csv_path='raw_consol_cmnts.csv',
    comment_column='comment_text',
    output_path='clean_usernames_cmnts.csv'
)

print("\nDone! Check 'cleaned_usernames_cmnts.csv' for results.")
