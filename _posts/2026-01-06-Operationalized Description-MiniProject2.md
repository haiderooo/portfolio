---
title: "Operationalized: Colonialism as signifier in social media users' response to Gilgit-Baltistan Land Reforms Act 2025"
excerpt_separator: "<!--more-->"
categories:
  - project2
tags:
  - digital humanities
  - social media topic modelling
  - social media research
  - gilgit-baltistan
  - political ecology
image: images/protest.jpg
---

# Operationalized project description after data collection and analysis methods testing.

<!--more-->


This research looks at the perceptions of facebook users about a recently instituted law called Gilgit-Baltistan Land Reforms Act 2025 (GBLRA 2025). It investigates the use of colonialism as a signifier for the relationship between Pakistan and Gilgit-Baltistan amongst facebook users in context of the GBLRA 2025. A BERTopic modelling method is used to identify whether or not colonialism is used as a signifier. For more background on this research see earlier posts on this blog. 

# Research Question

Do facebook users use colonialism as a signifier to refer to the relationship between Pakistan and Gilgit-Baltistan in discourse around the GBLRA 2025?

To answer this research question this research frames the following hypothesis:

# Hypothesis

<u>Conceptual hypothesis</u>

Colonialism is directly and indirectly used as a signifier to describe the current system of governance by people of Gilgit-Baltistan on facebook in discussions about the Gilgit-Baltistan Land Reforms Act 2025.

<u>Operational hypothesis</u>

In a guided BERTopic model of Facebook comments on posts related to GBLRA 2025, a topic characterized by colonial and governance-related keywords will account for at least 15% of all comments.

# Methodology

This research is a two-stage BERTopic modelling of facebook comments on public facebook posts about the GBLRA 2025.

Corpus:
The corpus of this study includes comments on posts from 4 public pages from Gilgit-Baltistan including Gilgit-Baltistan Assembly, Pamir Times, Ibex Media Network and Progressive Gilgit-Baltistan. The period of time for these posts are delimited from 2023 to 2025. Note that the GBLRA 2025 was under discussion in 2023 and 2024 as well as up to its promulgation as the Gilgit-Baltistan Land Reforms Bill 2023, 2024 and 2025, respectively.

These four pages were selected to allow for a substantial sample while incorporating platforms across the spectrum. The Gilgit-Baltistan Assembly is that assembly’s official page. Pamir Times is a pioneering internet and social media news platform from GB which has been the leading local news platform in the last decade or so. Ibex Media Network is another social media news platform known for driving engagement through video production quality and it is known as a “middle of the road” platform. Whereas, Progressive Gilgit-Baltistan is the leading leftist social media news and commentary page in GB in terms of audience numbers. To include wider representation, other region-wide pages as well as pages focusing on sub-regions within GB and pages of political parties and activists could also have been included. However, time limitations of the project demanded limiting the scope to the selected 4 pages as initial identification of posts was a time-taking endeavour. 

<u>Data collection</u>

Posts were identified by running searches on the selected 4 pages using the search keyword: “Land Reforms” and its translation in urdu لینڈ ریفارمز. Furthermore, selection of posts was made on two qualifiers. Only posts with one or more comments were selected and only posts made from the pages were selected. Posts made from other pages or profiles and tagging these pages were not selected. As a result a total of 113 posts were selected.

After shortlisting, links to these posts were generated through the copy link button which generated “share links” and not “pfbid” links. “pfbid” type links are the new canonical URLs for facebook posts, however, they require one more manual step to generate, taking more time. “share” link type URLs were acceptable for this study’s data collection strategy through a selenium based scraper model run on python. As a result a “source links” csv was obtained with three columns including a column for Page Name, one for an arbitrary sequential post_id system for each post and one for corresponding share link type URL to each post.


A manual counting of number of comments on each post by looking at the number of comments shown against each post on the facebook UI amounted to a total of more than 2000 comments. This was deemed as a good fit for a robust topic modelling. 

The second stage of the data collection entailed creating an automated scraper. This was achieved through a selenium based facebook comments scraper script run on python. The development environment for running python was IDLE for python 3.12. This script used the URL column of the source links csv to reach the selected posts on Google Chrome web browser. It collected all comments on each post. The scraper initializer was set to Headless=False, so the researcher could see its function in real time to confirm that it was opening the correct URLs, switching to All Comments and scrolling enough times to load all comments. Scroll count was set to 5 and wait time to 2 seconds. 

As a result, the scraper gave output of a csv with columns for the page name, post ID, and comment text as well as metadata on the post including post date, anonymous usernames, comment number (as ID), reply number (as ID), number of reactions and post collection date. Usernames were collected in anonymized form using hashlib.sha1. 

However, note that the model only collected 702 comments rather than an anticipated 1500-2000 comments. One explanation can be platform-limitation factors such as showing more comment count on the UI than existing. More importantly, this is explained by the scroll count of the scraper model. A test was run on one post carrying 185 comments from where the scraper collected 78 comments. So, a limitation of the scraper was detected. The study proceeded towards next steps due to time limitations. However, the study intends to attempt data collection and then analysis in one more round, starting with a greater scroll count. However, during the analysis steps, the 702 comments did reveal meaningful topics but the researcher could observe that the clusters were not distinct enough.

<u>Data cleaning</u>

The dataset obtained as a csv had a number of problems requiring cleaning. This was done through a automated cleaning scripts on python. First, in the comment text column, the text of replies to comments carried usernames of commenters to whom the replies were made to. This was fixed by keeping only the text in the comment text column and shifting the usernames to another column that stored the “replied to” usernames. Secondly, the comment text column was normalized to lower case, normalized for single spaces and both punctuations and non-text objects such as emojis and URLs were removed. Finally, the column for number of reactions was deleted because it was unnecessary. As a result, a machine-readable csv was obtained which was fit for BERTopic modelling.

<u>Analysis plan</u>
See below section titled ‘Analysis’, for steps taken in analysis so far. 

# Analysis

The analysis followed a two-stage BERTopic modelling. Instead of going for a guided BERTopic modelling right away, the study opted to start from an exploratory BERTopic modelling to inductively obtain some keywords for the guided stage. This was done to avoid using non-contextual keywords and framings. 

<u>Exploratory BERTopic Modelling</u>
The first stage BERTopic modelling was exploratory, as mentioned above. 

Before conducting the modelling, a for loop was used to identify the 40 most frequent words in each comment. This revealed English, Urdu and Latinized Urdu stopwords that had to be accounted for in the subsequent BERTopic modelling. 

Then an Exploratory BERTopic modelling was run on the cleaned dataset, accounting for nltk library’s English stopwords and custom stopwords revealed through the earlier top frequent word search. Note that using ‘numpy’ and ‘umap’ random seed was set to “42” to ensure reproducibility. Moreover, the topic model was set to multilingual. The generated model was saved and a csv was generated by the script that introduced a new column at the right in the dataset. This column carried topic numbers from -1 to 2, with -1 accounting for noise.

Subsequently, an interpretation model was run on this new dataset with topic numbers. This was used to generate the following files:
1) a histogram plot of the counts of comments per topic. See figure 1.
2) a distribution plot showing proportion of each topic per facebook page. See figure 2.
3) a csv each for each of the topics to show 10 representative comments for each topic.

Result 1: the count of comments per topic for -1 (noise) was 260, for 0 was 169, for 1 was 119 and for 2 was 85. 

The researcher looked at the representative comments for each topic in order to feed labels for the next step. Instead of forcing vocabulary related to colonialism, the researcher used descriptive and precise labels including: for topic 0: “legalizing dispossession”, for topic 1: “compromised legislators”, for 2: “incompetent legislators” and for topic -1: “noise.”  

These labels were fed into the interpretation step in exploratory BERTopic modelling. This resulted in another column added to the csv that showed the corresponding label against each topic number.  

<u>Guided BERTopic Modelling</u>

Words shortlisted manually by the researcher from looking at representative comments were used alongside theory guided keywords to run a Guided BERTopic modelling. See below list of seed words utilized:

seed_topic_list:
- "colonial", "نوآبادیاتی", "قبضہ", "imposed law", "حکمرانی" 
- "puppet", "کٹھ پتلی", "fake assembly", "غیر نمائندہ", "غلام"
- "facilitators", "مقامی اشرافیہ", "beneficiaries", "supporters", "سہولت کار", "collaborators", "حکم پر چلتے", "gaddar", "dalal", "wafaq parast", "وفاق پرست"

Note that, stopwords used in the previous stage were also accounted for. 

This stage resulted in a column added in the original cleaned dataset with a column for topics from -1 to 3. However, interpretation stage to add labels is yet to be conducted.

Result 2: Guided BERTopic analysis shows distinct clustering of comments into 4 topics. 

Hypothesis testing: Yet to be determined. 


# Limitations

So far there are errors and drawbacks in the data collection and analysis stages which need to be corrected in order to produce robust results. At the data collection stage, it includes the collection of less comments than anticipated and non-inclusion of video type URLs or failure to switch to All Comments on video type posts. This might require a login included approach. 

At the analysis stage, interpretation of Guided BERTopic is yet to be conducted. Moreover, the study will attempt analysis with a dataset precleaned of stopwords.

# Conclusion

This study conducted a two-stage BERTopic modelling of facebook comments on public posts regarding the Gilgit-Baltistan Land Reforms Act 2025. The principle concern of the study was to see if the institution of this law has prompted utilization of colonialism as signifier for relationship between Pakistan and Gilgit-Baltistan in social media discourse in Gilgit-Baltistan. Data was collected through a selenium based script with a scroll count of 5 and wait time of 2 seconds. This resulted in collection of less than anticipated total number of comments. 

An exploratory BERTopic Modelling revealed a significant clustering of the discourse into topics. These generated labels that point towards an answer for the research question. There is substantial presence of each topic on comments for all of the four facebook pages. Moreover, representative comments reveal usage of words that signal the use of colonialism as signifier. Furthermore, at least two labels obtained from representative comments (“legalizing dispossession” and “compromised legislators”) suggest the use of colonialism as signifier. 

Finally, a guided BERTopic Modelling also reveals significant clustering. However, it has not been interpreted through labeling yet. 

Visualization techniques for analysis such as word clouds and visualization methods for presentation are yet to be generated. 
