import pandas as pd
import regex as re

# Load CSV explicitly as UTF-8
df = pd.read_csv("clean_usernames_cmnts.csv", encoding="utf-8")

# Force comment_text to string (critical)
df["comment_text"] = df["comment_text"].astype(str)

# Drop n_reactions column
if "n_reactions" in df.columns:
    df = df.drop(columns=["n_reactions"])

def clean_comment_unicode(text):
    if text.lower() == "nan":
        return ""

    # lowercase (safe for Roman Urdu / English)
    text = text.lower()

    # remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # keep:
    # \p{L} = letters (Urdu, English, etc.)
    # \p{M} = combining marks (VERY IMPORTANT for Urdu)
    # \s     = whitespace
    text = re.sub(r"[^\p{L}\p{M}\s]", "", text)

    # normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text

# Apply cleaning
df["comment_text"] = df["comment_text"].apply(clean_comment_unicode)

# Remove empty rows
df = df[df["comment_text"] != ""]

# Save with UTF-8 BOM for Excel + corpus tools
df.to_csv(
    "final_clean_cmnts.csv",
    index=False,
    encoding="utf-8-sig"
)
