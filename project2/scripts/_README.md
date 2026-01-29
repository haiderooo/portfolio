## scripts
contains:
- "0_source_links_split.py" is script to split "source_links.csv" into two based on type of posts as shown in URL /v/ video or /p/ regular 
- "0_1_scraper_r.py" is selenium based script to scrap comments from regular posts from "source_links_r.csv"
- "0_1_scraper_v.py" selenium based script to scrap comments from video posts from "source_links_r.csv"
- "0_2_clean_replies.py" is script to clean "consol_raw_cmnts.csv" to separate usernames from within comment_text column to a separate "replied_to_username" column
- "0_2_clean_general.py" is script to clean "clean_usernames.csv" to remove lowercase text, remove punctuation, remove links, remove objects, remove symbols and remove n_reactions column, to develop "final_clean_cmnts1.csv"
- "1_1_desc_stats.py" is script for descriptive stats and summary of clean corpus --> "final_clean_cmnts1.csv"
- "1_2_page_user_stats.py" is script for descriptive stats according to users and according to pages.
- "1_PMI_n_grams.py" is script to generate csv with top unigrams, bigrams and trigrams from the comment_text column in the clean corpus. Used to build list in "ref_col_terms.csv" and "ref_ntrl_terms.csv".
- "1_top_2000_words.py" is script to generate csv with top 2000 words in the corpus. Used to develop grounded stopwords list and grounded lexicon csv files.
- "2_1_lex_signifier_prevalence_comp.py" is script to calculate prevalence of signifiers of colonialism in the comments --> comment_text column in the clean corpus.
- "2_2_lex_signifier_prevalence_visual.py" is script to visualize prevalence of signifiers of colonialism in the comments.
- "2_3_lex_top10_donut.py" is script to visualize number and percentage of comments carrying signifiers of colonialism in the comments.
- "3_1_exp_bert.py" is script for exploratory BERTopic model execution with a random seed number of 42 and to save model and save csv file with topics mapped onto the comments.
- "3_2_rprsnt_cmnts_exp_bert.py" is script that uses saved BERTopic model to create csv of 15 representative comments for each topic.
- "3_3_stats_on_topics.py" is script using saved BERTopic model and saved csv of mapped topics to create csv file with summary statistics for topics.
- "3_4_vis_bert.py" creates visuals including html and png files for representation of BERTopic model analysis of the data.
