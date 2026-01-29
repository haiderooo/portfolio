# Project 2 Folder Organization

## corpus folder
contains: 
- #### "raw" folder for all raw data files
  contains:
  -   "source_links.csv" with URLs to all selected posts for research corpus
  -   "source_links_v.csv" with URLs to video posts from selected posts list
  -   "source_links_r.csv" with URLs to regular posts from selected posts list
  -   "consol_raw_cmnts.csv" with all scraped comments along with metadata columns.
- #### "clean" folder for all clean data files:
  contains:
  - "clean_usernames.csv" which was obtained after separating usernames from within comment_text column to a separate "replied_to_username" column
  - "final_clean_cmnts1.csv" which was obtained after applying all other cleaning tasks on "clean_usernames.csv"
  - "ref_col_terms.csv" which was the list of signifiers of colonialism that was validated for presence in the corpus. Examples are "نوآبادیاتی", "قبضہ".
  - "ref_ntrl_terms.csv" which was the list of 'anchor terms' like government, land etc which were used to map relationships with the signifiers of colonialism onto.


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


## visualizations
contains:
- "1_page_structural_analysis.png" which shows Total Comments per Page and Average Comment Length per Page
- "1_user_correlation.png" is a line chart showing correlation between user repeat comment frequency and total words density of user in corpus
- "1_user_length_distribution.png" is a histogram showing the distribution of users in the data according to avg length of comments. 
- "1_word_contribution_pie.png" is a pie chart showing Percentage of Total Corpus Words by Users with 5< comments, 2-5 comments and single comment users.
- "1_page_reply_ratio.png" is a bar chart showing number of Replies to number of Comments ratios by Page Name.
- "2_Colonial_Prevalence_Donut.png" is a Donut chart showing the percentage and number of comments with signifiers of colonialism within total number of comments.
- "2_Explicit_Colonial_Mapping.png" is a bipartite co-occurrence heatmap between categories from "ref_col_terms.csv" and categories from "ref_ntrl_terms.csv"
- "2_Length_Comparison_Colonial_Framing.png" is a box-plot comparing Avg. Comment Length between comments which use signifiers of colonialism and comments which donot use signifiers of colonialism as defined by "ref_col_terms.csv" 
- "2_Signifier_Prevalence_Comparison_Chart.png" is a bar chart showing density of signifiers of colonialism in the total word count of the corpus and in the count of substantive words defined by difference from stopwords. To see the lists of stopwords used in this study in addition to nltk library for Enlgish stopwords, you can see stopword list files on google drive by clicking [here](https://drive.google.com/drive/folders/1p-RY4dFUXIYLLVPtNUwRdrVTLgx9__K7?usp=sharing).
- "2_User_Persistence_Colonial_Framing.png" is a bar chart showing Comparison of Number of Comments per User between Users mentioning signifiers of colonialism versus those who do not mention these signifiers.
- "3_Topic_Colonial_Density.png" shows the Density of Signifiers of Colonialism within word counts of 20 topics provided by BERTopic clustering.
- #### "tables" folder
  contains:
  - "t1.png" which shows the number of posts selected for each post for "source_links.csv"
  - "t2_5_rows_raw.png" shows table for structure of raw corpus csv file. 
  - "t3__rows_clean.png" shows table for structure of clean corpus csv file.
  - "t4_5_6.png" shows 3 tables for Overview Descriptive Statistics of Corpus, Distribution of Comments by Page and Descriptive Statistics of Text in Comment_Text Column.
  - "t7_8.png" show 2 tables for Distribution of Comments by Posts and Distribution of Comments by Users.
