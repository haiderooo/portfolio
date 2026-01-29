---
title: "Colonialism as signifier in social media discourse around Gilgit-Baltistan Land Reforms Act 2025"
excerpt_separator: "<!--more-->"
categories:
  - project2
tags:
  - digital humanities
  - social media topic modelling
  - social media research
  - gilgit-baltistan
image: images/edited_banner_image.png
---

## Introduction
This study analyzed facebook comments between 2023-25 on public pages prominent in Gilgit-Baltistan to investigate the use of colonialism as signifier in
discourse around a recently instituted property law called Gilgit-Baltistan Land Reforms Act 2025. 

<!--more-->

## Context
Gilgit-Baltistan (GB) is a disputed territory between India and Pakistan. At the time of the partition of India, GB was a territory of the Kashmir Dogra kingdom
which was a vassal state of the British Raj. In 1947, a rebellion by local military officers led to liberation of the region from colonial rule. The early
leadership, however, handed over GB to Pakistan. Yet, the region has since remained as one part of the former Kashmir territories under administration of Pakistan
without formal integration. It's 2.3 million people don’t have access to national representative forums. 

Within this geopolitical arrangement, Pakistani rule has meant a continuation of colonial structures leading to long-standing grievances. In other words, GB has
remained an internal colony of Pakistan. Over the decades, people of GB have increasingly come to use ‘colonialism as signifier’ for this ‘colonialism as
structure.’<sup>1</sup> Within global literature, land ownership and control regimes are considered central to understanding of colonialism. In GB, land regimes imposed from
above by Pakistan have remained ambiguous on the question of communal ownership. Under Kashmir Dogra rule, communal land or land outside of village boundaries, in
some parts of GB, had been demarcated as state land. The operative law was called ‘Khalisa Sarkar.’<sup>2</sup> It is widely understood by local people that the Khalisa
Sarkar regime has been null and void with the end of Dogra rule. Thus, communal property was governed through a mix of indigenous customary law and Pakistan’s
postcolonial land regimes, with conflicts arising between different regimes as well. Local legislative bodies were missing in Gilgit-Baltistan, until a Gilgit
Baltistan Assembly was formed in 2009 with authority over limited subjects. In 2025, as part of Pakistani state’s wider push for intensifying extractive
mechanisms, a new law was produced through the GB Assembly called Gilgit-Baltistan Land Reforms Act 2025. This law consolidates the control over all communal
lands in the hands of the state while nominally recognizing collective ownership of all non-private land by the people of GB.

When the law was scheduled for discussion in the GB Assembly, local activists began agitating widely. Many of them were arrested and jailed.<sup>3</sup> At the same time, widespread opposition was expressed on social media. Within this discourse, semantic signifiers of colonialism could be observed. These signifiers ranged from likening Pakistan’s rule to that of the former Dogra rule and even the East India Company to branding members of the GB Assembly as traitors (قوم کے غدار) and as collaborators (صہولت کار). The question of land has long animated the politics of GB, with anxieties of demographic change and dispossession of resources. In the last two decades, the anxieties around land have shaped people’s signifying of the relationship between Pakistan and GB as colonialism. This research is an attempt to account for colonialism as a signifier on social media.


## Research Question

Is there substantial signifying of the relationship between Pakistan and Gilgit-Baltistan as colonial in social media discourse around Gilgit-Baltistan Land Reforms Act 2025?


## Corpus

<u>Corpus selection</u>

This research looked at facebook comments on public posts relevant to GBLRA 2025 made by prominent social media pages catering to audiences in GB. The selection
of facebook as the target platform was driven by its number of users and percentage of engagement via text. X and Threads favor text content more than Facebook.
However, in 2025 the audience of Facebook in Pakistan is 44.9 Million (based on ad reach stats) as compared to X’s user count of 1.9 Million, with Threads
trailing behind significantly. Therefore, Facebook remains the most widely used “text-heavier” platform in Pakistan.

For this research, four (4) prominent public pages were selected. These include Gilgit-Baltistan Assembly, Pamir Times, Progressive Gilgit - Baltistan and Ibex
Media Network. Gilgit-Baltistan Assembly with 27k followers is the official page of that government body, sharing official updates on legislative activities such
as for the GBLRA 2025. Pamir Times with 634k followers is a pioneering social media news page, known as a middle of the road platform. Progressive Gilgit -
Baltistan with 41k followers is the leading left-leaning social media news page and Ibex Media Network with a follower count of 943k followers is the leading
social media news page of GB.

To select posts from which comments could be scraped, this research used the search terms ‘Land Reforms’ and ‘لینڈ ریفارمز’ to find relevant posts. Qualifiers applied
for selection included selection of posts made by the pages and posts with a comment count of 1 or more. This selection was done manually. As a result, 110 posts
were selected (2 posts out of 112 were disqualified later). See Table 1 below for the number of posts selected for each page. 


Table 1: Pages and Number of Posts

![t1 no of posts per page]({{site.baseurl}}images/t1.png)




<u>Data Collection</u>

First, the posts selected through the search terms and qualifiers were then recorded manually. URLs and page names of each post were then manually copied into a
source links csv with an additional column of post ID. 

To scrape comments from these posts, a selenium based script was used in headless mode. It used the URLs from the source links csv to find posts. Usernames were
collected as hashed anonymized IDs. Facebook’s platform specific limitations meant that script could not be optimized for both video and regular type posts. So,
the source links data was divided into two new csv files according to the post type indicated within the URL. 

For video type posts scraper, a scroll count of 20 and a wait time of 2 seconds were used in addition to the script first clicking on “All Comments” and then
clicking on “view more comments” as many times until the “view more comments” tab disappeared. The scrolling was conducted in two directions.

For regular type (‘/v/’) posts scraper, the selenium based script followed a strategy of clicking on “All Comments” and then scrolling with a scroll count of 15
and a wait time of 2 seconds.

Sanity checks: 5 posts from each category were manually checked for match between actual comment counts and number of scraped comments. Note that Facebook UI’s
report of number of comments is misleading and comments have to be manually counted in order to get actual comment count. 

Data from both the csv files was then consolidated into one UTF-8 csv with now a total 112 posts. See Table 2 below for structure of this csv with consolidated
raw corpus.


Table 2: Structure of raw data csv file.
![t2 rows raw data csv]({{site.baseurl}}images/t2_5_rows_raw.png)



Comments were stored in a comment_text column with corresponding metadata for each comment in the rest of the columns. 


<u>Data Cleaning</u>

The first task in cleaning was to separate usernames recorded within the comment text column. Usernames in the comment text existed only in replies to other
comments. The usernames were removed and collected into a separate “replied_to_username” column. 

Secondly, another data cleaning script was run to lowercase text, remove punctuation, remove extra spaces and non human language characters in the comment text
column. Then another script was run to remove rows with empty comment text cells created as a result of removing non-text objects, URLs and symbols where comments
consisted of only non-human language objects. 

See Table 3 below for structure of clean corpus.

Table 3: Structure of clean data csv file.
![t3 rows clean data csv]({{site.baseurl}}images/t3__rows_clean.png)



Note on language of corpus: this corpus contains English, Urdu and Romanized Urdu text alongside some relatively rare occurrences of words in local languages of
Gilgit-Baltistan. However, analysis of the corpus along linguistic lines was avoided (aside from during interpretation of BERTopic modelling analysis) because of
the complexities in demarcation of romanized Urdu and English through automated methods. Moreover, comments are many times in mixed formats, for instance,
romanized Urdu words used in a comment written mostly in English. 



## Analysis

<u>Methodology</u>

This research took a two-pronged analysis approach including both concordance analysis and
BERTopic modelling to triangulate results. 

Before starting with deeper analysis, descriptive and structural analyses of the corpus was
conducted to establish data context. See Tables 4-8 below for descriptive statistics of the
data. 




Table 4, 5 and 6: Overview Descriptive Statistics of Corpus, Distribution of Comments by Page and Descriptive Statistics of Text in Comment_Text Column.
![t4 5 and 6]({{site.baseurl}}images/t4_5_6.png)


Table 7 and 8: Distribution of Comments by Posts and Distribution of Comments by Users.
![t7 and 8]({{site.baseurl}}images/t7_8.png)




As shown in Tables 4-8 above, the cleaned corpus had a total of 96 posts with a total of 1439
comments from which 243 were replies to comments. Total number of words in
the comment_text column were 29,141. Pamir Times had an overwhelming majority of 826 comments.
The mean comment length was almost 15. 

After descriptive statistics, a deeper structural analysis was conducted to investigate how
page level variation and user level variation shape the data. See
Figures 1-5 below for results of structural analysis. 




Figure 1: Reply to Comment Ration by Page.
![figure 1]({{site.baseurl}}images/1_page_reply_ratio.png)

Figure 2: Total Number of Comments by Page and Average Comment Length by Page.
![figure 2]({{site.baseurl}}images/1_page_structural_analysis.png)

Figure 3: Distribution of Users by Average Comment Length.
![figure 3]({{site.baseurl}}images/1_user_length_distribution.png)

Figure 4: Relation between Comment Frequency and Contribution of Words to Corpus.
![figure 3]({{site.baseurl}}images/1_user_correlation.png)

Figure 5: Contribution of Words by Frequent Users to Corpus.
![figure 5]({{site.baseurl}}images/1_word_contribution_pie.png)




Progressive Gilgit-Baltistan shows the highest ratio of replies to comments and the most
comment length as well, showing a greater peer-to-peer engagement by users on posts by this
page for GBLRA 2025 discourse. Comments by most users fall within 1-100 word comment length.
There is a correlation between the number of comments and greater lengths of comments. However,
frequent users account for 17.6% of text in the corpus, suggesting the presence of frequent
‘power-users’ but
their contribution to the corpus is not overwhelming and therefore does not skew the data severely.  

Given this description of data, the methodology moves towards addressing the research question. 
First step was to create a lexicon or list of words, bigrams and trigrams that can be judged to signal framing the issue of GBLRA 2025 as an issue of or linked to
colonialism by people of Gilgit-Baltistan. This lexicon was then used to check the presence and prevalence of (de)colonial framings in the data. 

To create the lexicon, a PMI score method was used to analyze frequent unigrams, bigrams and trigrams. However, before doing so, the stopwords had to be
identified. For English stopwords the existing stopwords list from nltk was used. For Urdu and Romanized Urdu, a stopwords list for each was selected from online
community forums. However, to ensure stopwords from the corpus are targeted, stopwords from the corpus were manually identified from a list of 2000 most frequent
words within the corpus. 

Unigrams, bigrams and trigrams provided by a PMI score based method were then manually coded to create a categorized and grounded lexicon based in the corpus
itself. This was, however, then added to with theoretically judged words and phrases to ensure coverage. Two sets of words/terms were created with one carrying
colonial signifiers and another carrying neutral terms on which the colonial signifiers were later mapped to. A test of occurrence then filtered out those
theoretically added words which did not exist in the corpus. Frequency of the colonial signifiers in the lexicon was analyzed for the whole corpus as well as for
its distribution with respect to users, length of comments and as percentage within non-stopword words in the corpus. Then, a co-occurrence mapping was conducted
based upon categories in the lexicon. See findings section below for detailed results.

BERTopic modelling was then run on the corpus to triangulate the previous method. During the trial stage of this study, stopwords dilemma was already identified
to be applicable for BERTopic, therefore, avoided in this stage. Moreover, a random seed number of 42 was used to ensure reproducibility. See findings for
detailed results of BERTopic modelling.

<u>Findings</u>

The list of signifiers of colonialism included 72 single word and 2-word terms which were proven to exist at least once within the corpus. See figures 6-8 for
statistical distribution of these signifiers within the corpus.


Figure 6: Volume and Density of Signifiers of Colonialism in the Corpus.
![figure 6]({{site.baseurl}}images/2_Signifier_Prevalence_Comparison_Chart.png)


Figure 7: Distibution of Signifiers of Colonialism by Comments.
![figure 7]({{site.baseurl}}images/2_Colonial_Prevalence_Donut.png)


Figure 8: Comment Length of Users mentioning Signifiers of Colonialism.
![figure 8]({{site.baseurl}}images/2_Length_Comparison_Colonial_Framing.png)


As shown in figure 6 above, signifiers of colonialism accounted for 0.857% of all words within the corpus of 29,140 words i.e. mentioned a total of 249 times and
amongst substantive words they account for 1.56% of the words. This shows that these terms occupy a very thin part of the volume. However, as shown in Figure 7
above, they are distributed widely, so much so that they are present in 13.8% (198 comments) from all the 1439 comments. Moreover, figure 8 shows that users who
do use colonial signifiers tend to write lengthier comments, which makes it less likely for multiple colonial signifiers to be used within these comments. 

Co-occurrence heatmap, as shown in Figure 9 below, reveals more about how these colonial signifiers are used within discourse. 


Figure 9: Bipartite Heatmap of Signifiers of Colonialism Lexicon to Anchor Lexicon
![figure 9]({{site.baseurl}}images/2_Explicit_Colonial_Mapping.png)


33% of the comments which mention the
Government of Gilgit-Baltistan or GB government for short, also use words signifying “colonial collaborators” such as ‘سہولتکار’, ‘غدار’, ‘دلال’. Whereas, 31% of comments mentioning the GB government use framings
of colonialism related to land such as ‘قبضہ’, ‘خالصہ سرکار’, and ‘land grab.’ In 23% of the comments mentioning politicians of Gilgit-Baltistan, most mentioned of
them including Haji Gulbar Khan (the Chief Minister) and Amjad Hussain Advocate (the Leader of the Opposition), the mention of colonial collaboration co-occurs.
The co-occurrence heatmap reveals that when used, signifiers of colonialism in this corpus target the government, assembly and politicians of Gilgit-Baltistan who
are seen as responsible for ‘facilitating’ the GBLRA 2025 law. This pattern was also observable during qualitative coding of representative comments of topics. They are not only blamed through accusing them of incompetence and corruption but also
through framing them as colonial collaborators. 

BERTopic modelling provided 20 topics including the noise topic (-1). Topic clustering was skewed on linguistic lines with three topics dominated by Roman Urdu, 5
dominated by Urdu script and 9 dominated by English text.

A review of representative comments revealed the marked presence of signifiers of colonialism. Interestingly, BERTopic provided 3 topics (13, 9, 5) which were
organized around support for leaders of resistance movements and parties in Gilgit-Baltistan who themselves frame the relationship between Pakistan and Gilgit
Baltistan as colonial. There was at least one topic dominated by discussion around a power generation project in Hunza of the for-profit side of Aga Khan
Development Network called the Aga Khan Fund for Economic Development. Comments showed a polarization of opinions between some people defending the project and
others considering it a project of capitalist extraction. The representative comments of four other topics showed marked presence of signifiers of colonialism,
especially through the terming of the GB government, GB Assembly and GB politicians as collaborators. See Figure 10 below for identification of these topics which
show greater presence of signifiers of colonialism. Note that the clustering of BERTopic did not always show meaningful clusters, at least as revealed by the
representative comments with representative comments of 4 topics (0, 7, 10, 14, 15) dominated by ‘social noise.’


Figure 10: Comparison between Topics for Prevalence of Signifiers of Colonialism.
![figure 10]({{site.baseurl}}images/3_Topic_Colonial_Density.png)


To sum up, this study showed that the signifiers of colonialism are present in facebook comments on posts relevant to the Gilgit-Baltistan Land Reforms Act 2025.
They are thin within the collection of total words but substantially present within a section of users.

## Conclusion

This research investigated the use of signifiers of colonialism invoked in discourse around the Gilgit-Baltistan Land Reforms Act 2025 in comments on posts
relevant to this discourse on public facebook pages catering to audiences in Gilgit-Baltistan. An analysis of 1439 comments from 110 posts revealed that there is
presence of signifiers of colonialism in this discourse which takes up a small percentage of total word volume but is substantially present across comments. It is
mostly present in the form of terming of Gilgit-Baltistan's assembly, government and mainstream politicians as colonial collaborators. BERTopic modelling revealed
at least three clusters within this discourse dominated by support for resistance leaders like Advocate Ehsan Ali and Nawaz Khan Naji who themselves frame the
relationship between Pakistan and Gilgit-Baltistan as colonial. 

<u>Limitations and Reflections</u>

Handling social media text during data scrapping and analysis presents several challenges owing to platform-based limitations and the multiple layered nature of
social media discourse. It took me at least a few days to come up with a working selenium based scrapper with the help of my instructors and with assistance of
ChatGPT and other AI chatbots. When I finally did make a script, Facebook's platform limitations ensured that video post optimized script would not work well for regular posts. This is because of completely different structure of scrolling, differently labeled buttons and different positions of comment sections on the page. I did apply for Meta API Library access three times, however, they only got back to me during my third try after about two weeks, and that too asking for more information about me including how would this research contribute towards 'scientific knowledge.' 

Being new to code/python based analysis methods and generally to text analysis meant that I had to rely on AI chatbot assistance and the
guidance of my instructors. It was difficult to make decisions given many known unknowns and unknown unkowns. In this process I ended up experimenting with a
variety of analyses methods including GEPHI network visualization to wordtree maps, word clouds, kwic and collocations, in search for methods which might provide
unique insights about my data. 

Moreover, AI chatbots have a tendency to affirm one's biases unless explicitly checked. So, if ever I was unsure and made a tentative suggestion, it would
encouraged me to go for it. For example, I had used stopwords in BERTopic analysis during the trial stage and understood that accounting for stopwords could
lead to loss of syntax for BERTopic's modelling. However, when I tentatively made the suggestion during this stage that stopwords might provide better and more
meaningful clustering, it strongly encouraged me to go ahead and feed stopwords list to BERTopic script. It was only when I checked it asking it to be honestly
review the decision that it mentioned the risk of stopwords disturbing the syntax. Speaking of meaningfulness, whenever I asked ChatGPT as well as Gemini that my
visualizations and analyses methods are not providing meaningful methods, it kept on giving me suggestions which would exaggerate the substantiality of signifiers
of colonialism in my data. It understood that meaningful should actually mean more appropriate methods but it added quotation marks to the word meaningful in its
responses to suggest that it knows I am looking for just straightforward validation of my biases or completion of a task. So, unless explicitly requested, ChatGPT 
and Gemini AI would prioritize user satisfaction over systematic and scientific process while assisting with research.

Finally, I see that qualitative coding and thematic analysis has its own value. From looking at the data myself, I felt like the signifying of colonialism was not restricted to a "vocal minority" as found through these methods. Multiple researchers have argued that the signifiers of colonialism are no more restricted to a vocal minority in Gilgit-Baltistan as it used to be the case before as pointed out for example by Sokefeld for the 1990s. However, I would be very interested to learn about ways to enhance this analysis for example through bringing the actual posts by the pages into context of the comments. 

Amongst some things that this research missed from within the data was accounting for replied to usernames which were in another column to enhance the estimate of frequency of repeat users. Secondly, timestamps were obtained only as 'X weeks old' as displayed on Facebook UI, so a time-based analysis could not be made which would've involved changing the inputs everytime the analysis was repeated for example for trial and error. 


# References

1. Sōkefeld, Martin. "From colonialism to postcolonial colonialism: changing modes of domination in the Northern areas of Pakistan." The journal of Asian studies 64, no. 4 (2005): 939-973. Retrieved from [https://www.jstor.org/stable/25075905](https://www.jstor.org/stable/25075905).

2. Bhatti, Muhammad Ajmal, and Zahir Ali. "Land tenure and title system in gilgit-baltistan." Journal of Studies in Social Sciences 15, no. 1 (2016). Retrieved from [https://umangpoetry.org/poem/dheere-dheere-aur-kis-ne/](https://infinitypress.info/index.php/jsss/article/viewFile/1327/597).

3. Ali, Haider, and Qalandar Memon. Why Gilgit-Baltistan Is Rising Against Pakistan’s Land Seizures - NAKED PUNCH. June 14, 2025. Retrieved from [https://nakedpunch.com/why-gilgit-baltistan-is-rising-against-pakistans-land-seizures/](https://nakedpunch.com/why-gilgit-baltistan-is-rising-against-pakistans-land-seizures/).


# Credits
Banner Image: Edited Image. Photograph by Salim Khan, edited to add text.

Text on Banner Image: Verse from poem by Abdul Hafeez Shakir. Retrieved from [https://umangpoetry.org/poem/dheere-dheere-aur-kis-ne/ ](https://umangpoetry.org/poem/dheere-dheere-aur-kis-ne/)
