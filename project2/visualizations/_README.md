# visualizations
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
