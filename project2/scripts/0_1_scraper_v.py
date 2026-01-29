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

def initialize_scraper(headless=False):
    """Initialize Chrome driver for Windows 11"""
    chrome_options = Options()
    
    if headless:
        chrome_options.add_argument('--headless')
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
    
    # Additional options
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--allow-running-insecure-content')
    
    print("Initializing Chrome WebDriver...")
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
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

def parse_comment_text(comment_text, usernames_d):
    """Extract relevant information from a comment text with anonymization"""
    comment_text_lines = comment_text.splitlines()
    if len(comment_text_lines) < 2:
        print("Something wrong with this comment:", comment_text_lines)
        return dict()
    
    # Remove "Top fan" line if present
    if "Top fan" in comment_text_lines[0]:
        comment_text_lines.pop(0)
    
    # Remove "Top contributor" line if present
    if "Top contributor" in comment_text_lines[0]:
        comment_text_lines.pop(0)
        
    # Username should be first line
    commenter_username = comment_text_lines.pop(0)
    
    # Anonymise username
    username_anonymised = hashlib.sha1(commenter_username.encode()).hexdigest()
    usernames_d[commenter_username] = username_anonymised
    
    # Check for reactions (last line)
    if re.sub(r"[\d\s]+", "", comment_text_lines[-1]) == "":
        n_reactions = comment_text_lines.pop(-1)
    else:
        n_reactions = "0"
    
    # Date line
    post_date = comment_text_lines.pop(-1) if comment_text_lines else "Unknown"
    
    # Remaining text is the comment
    comment_text = " ".join(comment_text_lines)
    for username, hashed in usernames_d.items():
        comment_text = re.sub("@?" + re.escape(username), "@" + hashed, comment_text)

    comment_d = {
        "username_anonymised": username_anonymised,
        "n_reactions": n_reactions,
        "post_date": post_date,
        "comment_text": comment_text
    }
    return comment_d

def click_view_more_buttons(driver, max_attempts=50):
    """
    Aggressively click all 'View more' type buttons to expand comments.
    Enhanced for video posts.
    """
    attempts = 0
    consecutive_failures = 0
    
    # Multiple button text variations to search for
    button_texts = [
        "View more comments",
        "View more replies", 
        "View previous comments",
        "View all",
        "View 1 reply",
        "See more",
        "Load more comments"
    ]
    
    print("\n🔄 Expanding all comment sections...")
    
    while attempts < max_attempts and consecutive_failures < 5:
        found_button = False
        
        for button_text in button_texts:
            try:
                # Try different XPath strategies
                xpaths = [
                    f"//span[contains(text(), '{button_text}')]",
                    f"//div[contains(@role, 'button') and contains(., '{button_text}')]",
                    f"//*[contains(text(), '{button_text}')]"
                ]
                
                for xpath in xpaths:
                    try:
                        buttons = driver.find_elements(By.XPATH, xpath)
                        
                        for btn in buttons:
                            try:
                                # Check if button is visible
                                if btn.is_displayed():
                                    # Scroll into view
                                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                                    time.sleep(0.5)
                                    
                                    # Try to click
                                    driver.execute_script("arguments[0].click();", btn)
                                    print(f"✅ Clicked: '{button_text}'")
                                    found_button = True
                                    consecutive_failures = 0
                                    time.sleep(1.5)  # Wait for content to load
                                    break
                            except Exception as e:
                                continue
                        
                        if found_button:
                            break
                    except:
                        continue
                
                if found_button:
                    break
                    
            except Exception as e:
                continue
        
        if not found_button:
            consecutive_failures += 1
            # Scroll down a bit to potentially reveal more buttons
            driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(1)
        
        attempts += 1
    
    print(f"🛑 Finished expanding comments (attempts: {attempts})")

def scrape_comments_from_post(driver, post_url, scroll_count=20, wait_time=2):
    """Enhanced method to scrape comments from Facebook posts, including video posts"""
    print(f"\nNavigating to: {post_url}")
    driver.get(post_url)
    time.sleep(5)  # Initial page load
    
    # Save page source for debugging
    with open('facebook_selenium_page.html', 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    print("Page source saved to: facebook_selenium_page.html")
    
    comments_data = []
    
    # Handle cookie consent
    try:
        selector = 'div[aria-label^="Allow all cookies"]'
        for btn in driver.find_elements(By.CSS_SELECTOR, selector):
            try:
                driver.execute_script("arguments[0].click();", btn)
                print("✅ Accepted cookies")
                time.sleep(1)
                break
            except:
                pass
    except:
        pass
    
    # For video posts, sometimes need to scroll to comments section first
    print("🎥 Scrolling to locate comments section...")
    for _ in range(3):
        driver.execute_script("window.scrollBy(0, 800);")
        time.sleep(1)
    
    # Switch to "All comments" view
    try:
        # Look for sorting dropdown
        selectors = [
            "//span[contains(text(), 'Most relevant')]",
            "//span[contains(text(), 'Top comments')]",
            "//div[contains(@aria-label, 'comment') and contains(@role, 'button')]"
        ]
        
        for selector in selectors:
            try:
                element = driver.find_element(By.XPATH, selector)
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                time.sleep(1)
                element.click()
                time.sleep(1)
                
                # Now click "All comments"
                all_comments = driver.find_element(By.XPATH, "//span[contains(text(), 'All comments')]")
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", all_comments)
                time.sleep(1)
                all_comments.click()
                print("✅ Switched to 'All comments' view")
                time.sleep(2)
                break
            except:
                continue
    except:
        print("ℹ️  Could not switch to 'All comments' - may already be in this view")
    
    try:
        # PHASE 1: Aggressively expand all comment sections
        click_view_more_buttons(driver, max_attempts=50)
        
        # PHASE 2: Deep scrolling to load all comments
        print(f"\n📜 Deep scrolling ({scroll_count} iterations)...")
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        for i in range(scroll_count):
            # Scroll down
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(wait_time)
            
            # Scroll up a bit (helps trigger lazy loading)
            driver.execute_script("window.scrollBy(0, -300);")
            time.sleep(0.5)
            
            # Scroll back down
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(wait_time)
            
            # Check for new "View more" buttons after scrolling
            if i % 5 == 0:
                click_view_more_buttons(driver, max_attempts=10)
            
            # Check if we've reached the bottom
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print(f"  📍 Reached bottom at scroll {i+1}")
            last_height = new_height
            
            print(f"  Scroll {i+1}/{scroll_count}...")
        
        # PHASE 3: One final expansion attempt
        print("\n🔄 Final expansion attempt...")
        click_view_more_buttons(driver, max_attempts=20)
        
        # PHASE 4: Extract all comments
        print("\n📝 Extracting comments...")
        
        usernames_d = dict()
        comment_no = 0
        
        # Try multiple selectors for comments (video posts may use different structure)
        comment_selectors = [
            'div[aria-label^="Comment by"]',
            'div[role="article"]',
            'div[data-visualcompletion="ignore-dynamic"]'
        ]
        
        all_comment_divs = []
        for selector in comment_selectors:
            try:
                divs = driver.find_elements(By.CSS_SELECTOR, selector)
                if divs:
                    all_comment_divs = divs
                    print(f"✅ Found {len(divs)} elements using selector: {selector}")
                    break
            except:
                continue
        
        # If standard selectors don't work, try aria-label approach
        if not all_comment_divs:
            try:
                all_comment_divs = driver.find_elements(By.XPATH, "//div[starts-with(@aria-label, 'Comment by')]")
                print(f"✅ Found {len(all_comment_divs)} comments using XPath")
            except:
                pass
        
        for comment_div in all_comment_divs:
            try:
                # Check if this is actually a comment (has Comment by aria-label)
                aria_label = comment_div.get_attribute('aria-label')
                if not aria_label or not aria_label.startswith('Comment by'):
                    continue
                
                comment_no += 1
                comment_d = parse_comment_text(comment_div.text, usernames_d)
                
                if len(comment_d.keys()) == 0:
                    continue
                
                comment_d["comment_no"] = comment_no
                comment_d["reply_no"] = 0
                comments_data.append(comment_d)
                
                print(f"""---
comment_no:            {comment_d["comment_no"]}
username_anonymised:   {comment_d["username_anonymised"]}
post_date:             {comment_d["post_date"]}
comment_text:          {comment_d["comment_text"][:100]}...
---""")
                
                # Expand and extract replies
                parent_div = comment_div.find_element(By.XPATH, '..')
                
                # Expand replies if they exist
                reply_button_texts = ["View all", "View 1", "View reply", "View replies"]
                for btn_text in reply_button_texts:
                    try:
                        selector = f".//span[contains(text(), '{btn_text}')]"
                        buttons = parent_div.find_elements(By.XPATH, selector)
                        for b in buttons:
                            try:
                                driver.execute_script("arguments[0].click();", b)
                                print(f"  -> Expanded replies ({btn_text})")
                                time.sleep(1)
                            except:
                                pass
                    except:
                        pass
                
                # Extract replies
                reply_no = 0
                for reply in parent_div.find_elements(By.CSS_SELECTOR, 'div[aria-label^="Reply by"]'):
                    try:
                        reply_no += 1
                        reply_d = parse_comment_text(reply.text, usernames_d)
                        
                        if len(reply_d.keys()) == 0:
                            continue
                        
                        reply_d["comment_no"] = comment_no
                        reply_d["reply_no"] = reply_no
                        comments_data.append(reply_d)
                        
                        print(f"""===
comment_no:            {comment_no}
reply_no:              {reply_d["reply_no"]}
username_anonymised:   {reply_d["username_anonymised"]}
comment_text:          {reply_d["comment_text"][:100]}...
===""")
                    except Exception as e:
                        print(f"  ⚠️  Error parsing reply: {e}")
                        continue
                        
            except Exception as e:
                print(f"⚠️  Error processing comment {comment_no}: {e}")
                continue
        
        print(f"\n✅ Successfully extracted {len(comments_data)} items (comments + replies)")
        
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
    print(f"   Total items: {len(df)}")
    print(f"   Top-level comments: {len(df[df['reply_no'] == 0])}")
    print(f"   Replies: {len(df[df['reply_no'] > 0])}")
    print(f"   Unique posts: {df['post_id'].nunique()}")
    
    return df

def main(input_csv, url_column='post_url', page_name_column='page_name', 
         post_id_column='post_id', scroll_count=20, wait_time=2, headless=False):
    """
    Scrape comments from multiple Facebook posts (including video posts).
    Enhanced version without login requirement.
    """
    print("="*80)
    print("ENHANCED FACEBOOK COMMENT SCRAPER - VIDEO POST SUPPORT")
    print("For Digital Humanities Research: Gilgit-Baltistan Land Reforms Act 2025")
    print("="*80)
    
    # Load input CSV
    try:
        posts_df = pd.read_csv(input_csv)
        print(f"\n✅ Loaded {len(posts_df)} posts from {input_csv}")
        print(f"   Columns found: {list(posts_df.columns)}")
        
        if url_column not in posts_df.columns:
            raise ValueError(f"Column '{url_column}' not found in CSV")
        
        if page_name_column not in posts_df.columns:
            print(f"⚠️  Column '{page_name_column}' not found. Using 'Unknown'.")
            posts_df[page_name_column] = 'Unknown'
        
        if post_id_column not in posts_df.columns:
            print(f"⚠️  Column '{post_id_column}' not found. Using row numbers.")
            posts_df[post_id_column] = range(1, len(posts_df) + 1)
            
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        return
    
    # Initialize scraper
    driver = initialize_scraper(headless=headless)
    
    all_comments = []
    
    try:
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
                comments = scrape_comments_from_post(
                    driver,
                    post_url,
                    scroll_count=scroll_count,
                    wait_time=wait_time
                )
                
                collection_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                for comment in comments:
                    comment['page_name'] = page_name
                    comment['post_id'] = post_id
                    comment['collection_date'] = collection_date
                
                all_comments.extend(comments)
                print(f"✅ Collected {len(comments)} items from this post")
                
            except Exception as e:
                print(f"❌ Error scraping post {post_id}: {e}")
                import traceback
                traceback.print_exc()
                continue
            
            # Delay between posts
            if idx < len(posts_df) - 1:
                print(f"\n⏳ Waiting 10 seconds before next post...")
                time.sleep(10)
        
        # Save results
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
    
    input_csv = "fb_posts_video_posts.csv"
    
    url_column = "post_url"
    page_name_column = "page_name"
    post_id_column = "post_id"
    
    # Enhanced scraping parameters for video posts
    scroll_count = 20  # Increased for video posts
    wait_time = 2
    headless = False
    
    # =======================================
    
    main(input_csv, 
         url_column=url_column,
         page_name_column=page_name_column,
         post_id_column=post_id_column,
         scroll_count=scroll_count,
         wait_time=wait_time,
         headless=headless)
