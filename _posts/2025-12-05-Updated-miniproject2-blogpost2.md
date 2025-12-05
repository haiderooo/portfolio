---
title: "Updated: Colonialism as signifier in social media users' response to Gilgit-Baltistan Land Reforms Act 2025"
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

# Revised project description according to dataset review and time limitations

<!--more-->


This project conducts a topic modelling research on social media users’ response to Gilgit-Baltistan Land Reforms Act 2025. Specifically, it looks at the prevalence and articulation of ‘colonialism’ as a signifier in social media discourse on facebook by people of Gilgit-Baltistan (GB). For more background on the project please refer to my earlier post on this blog. Moreover, major changes have occurred since the last blog post concerning the corpus after review of the available data and time limitations of the project.


# Research Question


Colonialism is directly and indirectly used as a signifier to describe the current system of governance by people of Gilgit-Baltistan on facebook in discussions about the Gilgit-Baltistan Land Reforms Act 2025.


Corpus:
To analyze users’ expression of opinion on the GB Land Reforms Act 2025 this project looks at comments on relevant posts made between 2023 and 2025 on four facebook pages. 

Links to pages with search operators applied unless specified otherwise:

Gilgit-Baltistan Assembly (search operator not applied)
[https://www.facebook.com/gblagb](https://www.facebook.com/gblagb)

Pamir Times
[https://www.facebook.com/profile/100064710099601/search/?q=land%20reforms](https://www.facebook.com/profile/100064710099601/search/?q=land%20reforms )

Ibex Media Network
[https://www.facebook.com/profile/100064048422419/search/?q=land%20reforms](https://www.facebook.com/profile/100064048422419/search/?q=land%20reforms)

Progressive Gilgit-Baltistan
[https://www.facebook.com/profile/100063700377023/search/?q=%D9%84%DB%8C%D9%86%DA%88%20%D8%B1%DB%8C%D9%81%D8%A7%D8%B1%D9%85%D8%B2](https://www.facebook.com/profile/100063700377023/search/?q=%D9%84%DB%8C%D9%86%DA%88%20%D8%B1%DB%8C%D9%81%D8%A7%D8%B1%D9%85%D8%B2)

These pages were selected to cover the most popular social media platforms of Gilgit-Baltistan as well as official platforms and oppositional platforms. To cover a greater diversity of opinion, a wider corpus would have been a stronger dataset, such as the corpus suggested in the last blog post. Due to time limitations of the project, that is not possible. Nonetheless, the current corpus is strong in terms of suitability for a python applied DH text analysis project. 

At the same time, the current corpus covers a holistic range of platforms in the context of Gilgit-Baltistan. The page of the Gilgit-Baltistan Assembly is an official government platform, both Pamir Times and Ibex Media Network are two of the most popular social media news platforms of the region known for being “middle of the road’’ and “neutral”. Whereas the page Progressive Gilgit-Baltistan is another popular news platform that focuses on leftist and social movement voices. In this way, the corpus covers platforms with broad and diverse audiences. 

See Table 1 below for details of the dataset. In total, 2,018 facebook comments are analyzed across a total of 132 posts on 4 pages.

The comments on these selected posts are mostly either in English or Urdu. Very few of them are in other languages spoken in Gilgit-Baltistan. Therefore, covering the English and Urdu comments will be largely representative of the data for social media users who interact with the selected facebook pages.

Table 1

![a random image]({{site.baseurl}}images/table-dataset-stats.png)


# Steps of methodology
To do a topic modelling the data needs to be scrapped and stored in normalized UTF-8 format, so that it can be analyzed using python. The steps in this methodology are described below. 

<u>Data collection, anonymization and translation</u>
First the comments will be copied and pasted into one single document with markers for separate pages and posts. Then, comments by pages will be deleted and names of users will be replaced with generic identifiers such as “User 1, User 2… User n.” After filtration and anonymization, comments in Urdu will be translated into English. 

<u>Data organization</u>
This data will then be stored in three different formats. First it will be converted into a csv file with 6 columns including Page Name, Post Number, Date of Post, Comment Content, Original Comment Language and Link to Post. This will become a master file which can be used to generate visualizations of the dataset and to store metadata.

Secondly, separate text files for each post will be created to all comments on each post together. These text files will be stored in one single folder instead of creating folders for each page. This is because the research is not looking for comparisons between responses of users of different pages. Moreover, that risks creating a dataset which may be misused to target community journalists who run these pages, if the security of the dataset is compromised at any point. 

Third, the single document created in the beginning (post anonymization, filtering and translation) will be kept to allow for analyses that may suit a single file instead of multiple. 

<u>Search terms and AI text mining</u>
The single file document will be uploaded to an AI LLM GPT to extract words in the document that may describe colonialism. Core search words before GPT’s extraction are:
1) Colonialism, 2) Occupation and 3) Dispossession. The list of search words extracted by the GPT and the core search words will be referred to as simply ‘search terms’. These will then be used for further analysis as described below. 

<u>Word Frequency</u>
The first analysis will be to run a word frequency query of the list of search terms.

<u>Collocations</u>
Secondly, a collocation search will be carried out to find what words and groups of words coincide most commonly with colonialism, other search terms and the word ‘land.’

<u>Topic Modelling</u>
Finally, an LDA topic modelling will be applied on all texts in the folder. This will group similar comments together and stable topics will emerge. While word frequency and collocations would answer whether colonialism as a signifier is used by social media users, topic modelling will reveal similarities and differences between different comments in terms of whether they do use colonialism as a signifier and if they do, how is it articulated. 

# Conclusion
This research analyzes a dataset of 2,018 comments by social media users on posts relevant to Gilgit-Baltistan Land Reforms Act 2025 for the period of time between 2023 and 2025 on four selected pages on facebook dealing with Gilgit-Baltistan. It seeks to study the use of the signifier ‘colonialism’ in social media discourse on the aforementioned Act of the Gilgit-Baltistan Assembly. 

