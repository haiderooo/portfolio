from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import hashlib
from datetime import datetime
import re
import os
import hashlib

def initialize_scraper(headless=False):
    """Initialize Chrome driver for Windows 11"""
    chrome_options = Options()
    
    if headless:
        chrome_options.add_argument('--headless')  # Run in background
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    
    # Windows 11 specific settings
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # User agent for Windows 11 Chrome
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    chrome_options.add_argument(f'user-agent={user_agent}')
    
    # Additional options to avoid detection
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--allow-running-insecure-content')
    
    print("Initializing Chrome WebDriver...")
    
    try:
        # Automatic driver management
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Hide automation
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("WebDriver initialized successfully!")
        
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        print("\nIf you see ChromeDriver errors, try:")
        print("1. Close all Chrome windows")
        print("2. Update Chrome: chrome://settings/help")
        print("3. Run: pip install --upgrade webdriver-manager")
        raise
    return driver

def login_to_facebook(driver, email=None, password=None):
    """Optional: Login if required to see comments"""
    if not email or not password:
        print("No credentials provided. Trying without login...")
        return False
    
    try:
        print("Attempting to login to Facebook...")
        driver.get("https://www.facebook.com")
        time.sleep(3)
        
        # Enter email
        email_field = driver.find_element(By.ID, "email")
        email_field.send_keys(email)
        
        # Enter password
        password_field = driver.find_element(By.ID, "pass")
        password_field.send_keys(password)
        
        # Click login
        login_button = driver.find_element(By.NAME, "login")
        login_button.click()
        
        time.sleep(5)
        print("✅ Login attempt completed")
        return True
        
    except Exception as e:
        print(f"Login failed: {e}")
        return False

def parse_comment_text(comment_text, usernames_d):
    """Extract the relevant information from a comment text.

    Using a simplified method because of the complex structure of Facebook comments.

    The function anonymises the usernames using SHA1 hashes.
    The usernames_d is used to anonymise user names in the comment texts.
    """
    comment_text_lines = comment_text.splitlines()
    if len(comment_text_lines) < 2:
        print("Something wrong with this comment:", comment_text_lines)
        return dict()
    
    # remove the "top fan" line:
    if "Top fan" in comment_text_lines[0]:
        comment_text_lines.pop(0)
        
    # After removing the top fan line, the username should be the first line:
    commenter_username = comment_text_lines.pop(0)
    
    # Anonymise the username:
    username_anonymised = hashlib.sha1(commenter_username.encode()).hexdigest()

    # Add the username and anonymization to the usernames_d:
    usernames_d[commenter_username] = username_anonymised
    
    # if people reacted to the comment, the last line will display the number of reactions:
    if re.sub(r"[\d\s]+", "", comment_text_lines[-1]) == "":
        n_reactions = comment_text_lines.pop(-1)
    else:
        n_reactions = "0"
    # the line above the reactions is an indication of the date:
    post_date = comment_text_lines.pop(-1)
    # the remainder is the comment text
    comment_text = " ".join(comment_text_lines)
    for username, hashed in usernames_d.items():
        comment_text = re.sub("@?"+username, "@"+hashed, comment_text)

    comment_d = {
        "username_anonymised": username_anonymised,
        "n_reactions": n_reactions,
        "post_date": post_date,
        "comment_text": comment_text
        }
    return comment_d


def scrape_comments_from_post(driver, post_url, scroll_count=15, wait_time=2):
    """Main method to scrape comments from a Facebook post"""
    print(f"\nNavigating to: {post_url}")
    driver.get(post_url)
    time.sleep(5)  # Initial page load
    
    # Save page source for debugging
    with open('facebook_selenium_page.html', 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    print("Page source saved to: facebook_selenium_page.html")
    
    comments_data = []

    # PV: Click the Allow all cookies button
    selector = 'div[aria-label^="Allow all cookies"]'
    for btn in driver.find_elements(By.CSS_SELECTOR, selector):
        print(btn.get_attribute("outerHTML")[:200])
        try:
            driver.execute_script("arguments[0].click();", btn)
            time.sleep(1)
        except:
            print("clicking this button failed:")

    #PV: show all comments instead of only the most relevant:

    try:
        selector = "//span[contains(text(), 'Most relevant')]"
        element = driver.find_element(By.XPATH, selector)
        driver.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(1)
        element.click()
        time.sleep(1)
        selector = "//span[contains(text(), 'All comments')]"
        all_comments = driver.find_element(By.XPATH, selector)
        driver.execute_script("arguments[0].scrollIntoView();", all_comments)
        time.sleep(1)
        all_comments.click()
        print("Clicked 'All comments'")
        time.sleep(2)
    except:
        pass

    # PV: I haven't made any changes here as this seems to work:
    try:
        # ========== STRATEGY 1: Click "View more comments" UNTIL GONE ==========
        while True:
            try:
                btn = driver.find_element(
                    By.XPATH,
                    "//span[contains(text(), 'View more comments')]"
                )
                driver.execute_script("arguments[0].scrollIntoView();", btn)
                time.sleep(1)
                btn.click()
                print("✅ Clicked 'View more comments'")
                time.sleep(2)
            except:
                # Button no longer exists → all comments loaded
                print("🛑 No more 'View more comments' button")
                break
            
        # ========== STRATEGY 2: Scroll to load comments ==========
        print(f"\nScrolling {scroll_count} times to load comments...")
        for i in range(scroll_count):
            # Scroll down
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print(f"  Scroll {i+1}/{scroll_count}...")
            time.sleep(wait_time)
            
            # Also try scrolling comments section specifically
            try:
                driver.execute_script("""
                    var commentSections = document.querySelectorAll('[role="article"], [data-commentid]');
                    for(var section of commentSections) {
                        section.scrollIntoView();
                    }
                """)
            except:
                pass
        
        # ========== EXTRACT COMMENTS AND METADATA  ==========
        print("\nExtracting comments using Peter's method...")

        #PV:
        # create a dictionary of the user names,
        # so that we can anonymize them in replies:
        usernames_d = dict()
        comment_no = 0
        for comment_div in driver.find_elements(By.CSS_SELECTOR, 'div[aria-label^="Comment by"]'):
            comment_no += 1
            # extract the text and metadata from the comment text:
            comment_d = parse_comment_text(comment_div.text, usernames_d)
            # skip to the next comment if it was not 
            if len(comment_d.keys()) == 0:
                continue
            comment_d["comment_no"] = comment_no
            comment_d["reply_no"] = 0
            comments_data.append(comment_d)
            
            print(f"""
---
comment_no:            {comment_d["comment_no"]}
username_anonymised:   {comment_d["username_anonymised"]}
post_date:             {comment_d["post_date"]}
comment_text:          {comment_d["comment_text"]}
---""")

            # expand the replies:
            parent_div = comment_div.find_element(By.XPATH, '..')
            if "View all" in parent_div.text or "View 1" in parent_div.text:
                selector = ".//span[contains(text(), 'View all') or contains(text(), 'View 1')]"
                buttons = parent_div.find_elements(By.XPATH, selector)
                for b in buttons:
                    print("-> Expanding Replies")
                    driver.execute_script("arguments[0].click();", b)
                    time.sleep(1)
                    
            # add the replies to the comments_d:   
            replies = []
            reply_no = 0
            for reply in parent_div.find_elements(By.CSS_SELECTOR, 'div[aria-label^="Reply by"]'):
                reply_no += 1
                reply_d = parse_comment_text(reply.text, usernames_d)
                reply_d["comment_no"] = comment_no
                reply_d["reply_no"] = reply_no
                comments_data.append(reply_d)

                print(f"""
===
comment_no:            {comment_d["comment_no"]}
reply_no:              {reply_d["reply_no"]}
username_anonymised:   {reply_d["username_anonymised"]}
post_date:             {reply_d["post_date"]}
comment_text:          {reply_d["comment_text"]}
===""")
            

        
        
        
        print(f"\n✅ Successfully extracted {len(comments_data)} unique comments")
        
    except Exception as e:
        print(f"❌ Error during scraping: {e}")
        import traceback
        traceback.print_exc()
    
    return comments_data



def save_to_csv(all_comments_data, output_filename):
    """Save all comments from multiple posts to a single CSV"""
    if not all_comments_data:
        print("❌ No comments to save!")
        return None

    df = pd.DataFrame(all_comments_data)
    
    # Reorder columns
    columns_order = [
        'page_name',
        'post_id',
        'comment_no',
        'reply_no',
        'comment_text',
        'username_anonymised',
        'n_reactions',
        'post_date',
        'collection_date',
    ]
    
    df = df[columns_order]
    
    # Save
    df.to_csv(output_filename, index=False, encoding='utf-8-sig')
    print(f"\n💾 CSV saved: {output_filename}")
    print(f"   Location: {os.path.abspath(output_filename)}")
    
    # Show summary
    print(f"\n📊 Collection Summary:")
    print(f"   Total comments: {len(df)}")
    print(f"   Unique posts: {df['post_id'].nunique()}")
    
    return df

# ============ MAIN FUNCTION ============
def main(input_csv, url_column='post_url', page_name_column='page_name', 
         post_id_column='post_id', FB_EMAIL="", FB_PASSWORD="",
         scroll_count=15, wait_time=2, headless=False):
    """
    Scrape comments from multiple Facebook posts listed in a CSV file.
    
    Parameters:
    -----------
    input_csv : str
        Path to CSV file containing post URLs
    url_column : str
        Name of column containing Facebook post URLs (default: 'post_url')
    page_name_column : str
        Name of column containing page names (default: 'page_name')
    post_id_column : str
        Name of column containing post IDs (default: 'post_id')
    """
    print("="*80)
    print("FACEBOOK COMMENT SCRAPER - MULTI-POST VERSION")
    print("For Digital Humanities Research: Gilgit-Baltistan Land Reforms Act 2025")
    print("="*80)
    
    # Load input CSV
    try:
        posts_df = pd.read_csv(input_csv)
        print(f"\n✅ Loaded {len(posts_df)} posts from {input_csv}")
        print(f"   Columns found: {list(posts_df.columns)}")
        
        # Validate required columns
        if url_column not in posts_df.columns:
            raise ValueError(f"Column '{url_column}' not found in CSV. Available columns: {list(posts_df.columns)}")
        
        # Set defaults for missing columns
        if page_name_column not in posts_df.columns:
            print(f"⚠️  Column '{page_name_column}' not found. Using 'Unknown' as default.")
            posts_df[page_name_column] = 'Unknown'
        
        if post_id_column not in posts_df.columns:
            print(f"⚠️  Column '{post_id_column}' not found. Using row numbers as post IDs.")
            posts_df[post_id_column] = range(1, len(posts_df) + 1)
            
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        return
    
    # Initialize scraper
    driver = initialize_scraper(headless=headless)
    
    # Storage for all comments
    all_comments = []
    
    try:
        # Login if credentials provided
        if FB_EMAIL and FB_PASSWORD:
            login_to_facebook(driver, FB_EMAIL, FB_PASSWORD)
        
        # Process each post
        for idx, row in posts_df.iterrows():
            post_url = row[url_column]
            page_name = row[page_name_column]
            post_id = row[post_id_column]
            
            print(f"\n{'='*80}")
            print(f"Processing post {idx+1}/{len(posts_df)}")
            print(f"Page: {page_name} | Post ID: {post_id}")
            print(f"{'='*80}")
            
            try:
                # Scrape comments for this post
                comments = scrape_comments_from_post(
                    driver,
                    post_url,
                    scroll_count=scroll_count,
                    wait_time=wait_time
                )
                
                # Add metadata to each comment
                collection_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                for comment in comments:
                    comment['page_name'] = page_name
                    comment['post_id'] = post_id
                    comment['collection_date'] = collection_date
                
                all_comments.extend(comments)
                print(f"✅ Collected {len(comments)} comments from this post")
                
            except Exception as e:
                print(f"❌ Error scraping post {post_id}: {e}")
                import traceback
                traceback.print_exc()
                continue
            
            # Add delay between posts to avoid rate limiting
            if idx < len(posts_df) - 1:
                print(f"\n⏳ Waiting 10 seconds before next post...")
                time.sleep(10)
        
        # Save all results to single CSV
        if all_comments:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f'facebook_comments_multi_{timestamp}.csv'
            save_to_csv(all_comments, output_filename)
        else:
            print("\n⚠️  No comments collected from any posts.")
            
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("\n⏳ Browser will close in 10 seconds...")
        time.sleep(10)
        driver.quit()

if __name__ == "__main__":
    # ============ CONFIGURATION ============
    
    # Path to your input CSV file
    input_csv = "fb_posts_regular_posts.csv"
    
    # Column names in your CSV (adjust if different)
    url_column = "post_url"        # Column containing Facebook post URLs
    page_name_column = "page_name" # Column containing page names
    post_id_column = "post_id"     # Column containing post IDs
    
    # Optional: Facebook login credentials (if needed)
    FB_EMAIL = ""  # Leave empty if not needed
    FB_PASSWORD = ""  # Leave empty if not needed
    
    # Scraping parameters
    scroll_count = 15  # Number of scrolls per post
    wait_time = 2     # Seconds between scrolls
    headless = False  # Set to True to run in background
    
    # =======================================
    
    main(input_csv, 
         url_column=url_column,
         page_name_column=page_name_column,
         post_id_column=post_id_column,
         FB_EMAIL=FB_EMAIL, 
         FB_PASSWORD=FB_PASSWORD,
         scroll_count=scroll_count,
         wait_time=wait_time,
         headless=headless)
