import pandas as pd
from datetime import datetime
import os
from pathlib import Path

def split_facebook_posts_by_type(input_csv, output_prefix):
    """
    Split Facebook post URLs into video (_v) and regular post (_r) type CSVs.
    """
    
    print("="*80)
    print("FACEBOOK POST TYPE SPLITTER")
    print("Separating video posts (/v/) from regular posts (/p/)")
    print("="*80)
    
    # Load the CSV
    try:
        # Converting Path object to string for pandas compatibility
        df = pd.read_csv(str(input_csv))
        print(f"\n✅ Loaded CSV: {input_csv}")
        print(f"   Total rows: {len(df)}")
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        return None, None, None
    
    if 'post_url' not in df.columns:
        print("❌ Error: 'post_url' column not found in CSV")
        return None, None, None
    
    def get_post_type(url):
        if pd.isna(url):
            return 'unknown'
        url_str = str(url).lower()
        if '/share/v/' in url_str or '/videos/' in url_str:
            return 'video'
        elif '/share/p/' in url_str or '/posts/' in url_str or '/photo' in url_str:
            return 'post'
        else:
            return 'unknown'
    
    print("\n🔍 Analyzing post URLs...")
    df['post_type'] = df['post_url'].apply(get_post_type)
    
    # Split dataframes
    video_df = df[df['post_type'] == 'video'].copy().drop('post_type', axis=1)
    post_df = df[df['post_type'] == 'post'].copy().drop('post_type', axis=1)
    unknown_df = df[df['post_type'] == 'unknown'].copy().drop('post_type', axis=1)
    
    # Define exact filenames as requested: source_links_v.csv and source_links_r.csv
    # .with_name replaces the filename but keeps the folder path intact
    video_csv = output_prefix.with_name(f"{output_prefix.name}_v.csv")
    post_csv = output_prefix.with_name(f"{output_prefix.name}_r.csv")
    
    # Save video posts
    if len(video_df) > 0:
        video_df.to_csv(str(video_csv), index=False, encoding='utf-8-sig')
        print(f"\n💾 Video posts saved: {video_csv}")
    else:
        print("\n⚠️  No video posts found.")
        video_csv = None
    
    # Save regular posts
    if len(post_df) > 0:
        post_df.to_csv(str(post_csv), index=False, encoding='utf-8-sig')
        print(f"💾 Regular posts saved: {post_csv}")
    else:
        print("\n⚠️  No regular posts found.")
        post_csv = None

    # Handle unknown
    if len(unknown_df) > 0:
        unknown_csv = output_prefix.with_name(f"{output_prefix.name}_unknown.csv")
        unknown_df.to_csv(str(unknown_csv), index=False, encoding='utf-8-sig')
        print(f"⚠️  Unknown types saved to: {unknown_csv}")

    stats = {'total': len(df), 'v': len(video_df), 'r': len(post_df)}
    return video_csv, post_csv, stats

def preview_split(input_csv):
    df = pd.read_csv(str(input_csv))
    print(f"Previewing {len(df)} rows...")
    # (Simplified preview for brevity)

if __name__ == "__main__":
    # --- PATH CONFIGURATION ---
    # Current folder (scripts/)
    SCRIPT_DIR = Path(__file__).parent
    
    # Target folder (scripts/ -> ../ -> corpus/raw/)
    RAW_DATA_DIR = SCRIPT_DIR.parent / "corpus" / "raw"
    
    # Define Input and Output Prefix
    input_file = RAW_DATA_DIR / "source_links.csv"
    output_base = RAW_DATA_DIR / "source_links" 
    
    # Check if input exists before running
    if not input_file.exists():
        print(f"❌ File not found at: {input_file}")
    else:
        print("Running split...\n")
        
        # Run the split
        video_csv, post_csv, stats = split_facebook_posts_by_type(
            input_csv=input_file,
            output_prefix=output_base
        )
        
        print("\n✅ Split complete!")
        print(f"Find your files in: {RAW_DATA_DIR}")
