---
title: Digitization
permalink: /Digitization/
layout: page
---

![Digitization Banner]({{ site.baseurl }}/images/final_banner_digitization.jpg)

# Digitizing 'The Book of Wonders for the Beholders": a Shia Ismaili manuscript from Gilgit-Baltistan published in 1940.


This project aimed at applying machine learning1 to digitize a manuscript of Shia Ismaili religious scholarship from South Asia written in Persian. By training a model and applying it on the manuscript, the efficacy of machine learning for digitization of Persian manuscripts was increased as its scope widened to include manuscripts from Central and South Asia written in the mid-20th century. On the other hand, the project also preserved the manuscript itself and made it available for digital humanities research. 


![Image of the manuscripts title page]({{ site.baseurl }}/assets/images/manuscript_titlepage.jpg)


To be specific, the digitized manuscript is   کتاب تحفته النّاظِرین المعروف صَحیفَہ  (trans: kitāb-i tuḥfatah al-nāẓirīn al-maʿrūf ṣaḥīfah) which roughly translates into “Selection of Famous Pages from the Book of Wonders for the Beholders”. This book is a commentary on selections of works originally authored by Syed Sohrab Badakshani. The manuscript gives almost a step-by-step guide to theology, cosmology and ethics in the Central Asian and northern South Asian Ismaili tradition. It was an official publication of the Shia Ismaili institutions’ representatives in Gilgit. Gilgit town was the administrative and commercial center of the greater area that is now Gilgit-Baltistan. Being at the confluence of South and Central Asia, Islamic scholarship here at the time reflected the influence of traditions and institutions from both regions. This manuscript is published under the ambit of the modern Ismaili institutions, wherein, the Gilgit-Baltistan area was connected to the South Asian center at Bombay and Karachi. Whereas, its content addresses works originating in the Badakshan and broader Central Asian region. It is an important text in revealing the point of view of Ismaili scholars of Gilgit-Baltistan on theology, and one sanctioned by the Ismaili institutions, around the time of publication. Additionally, the work is compiled by Qudrat Ullah Baig and Ghulam Uddin who are noted as two of the three earliest scholars with extant written works in the history of Gilgit-Baltistan. Thus the manuscript carries importance as a historical document for Gilgit-Baltistan in general, beyond Ismailism.


![Image: Generic photo of a book scanner]({{ site.baseurl }}/assets/images/scanner.jpg)


The manuscript was scanned using an overhead book scanner. The scanner took an image of each page (one side of a leaf) one at a time. It created files in png format in the attached laptop. Section title or section starting images and page numbers were noted on a page with a pencil along with duplicates and poorer quality images. A white colored snake was used to keep pages open. After all pages were scanned, team members re-cropped all images to keep the image within the boundaries of each page and saved it as the same image. Later, the team went through all images and one page was detected to be missing from the scanned images. It was rescanned and added to the folder. [Click here]({{ site.baseurl }}/project1-digitization/Rasail_Metadata.txt) to access the Metadata and [here]({{ site.baseurl }}/project1-digitization/Rasail_Group_Sheet2.csv) to see a csv of table of contents of the manuscript.


![Image: screenshot of homepage of Escriptorium]({{ site.baseurl }}/assets/images/escriptorium.png)


Next, the Optical Character Recognition (OCR) process was conducted on Escriptorium2 which is an open-source platform for OCR/HTR (Hand-written Text Recognition) of both latin and non-latin scripts. It integrates machine learning models — providing tools for fine-tuning, training and execution —3 for OCR. On Escriptorium, a joint project was created for the team and then each team member worked on a separate document. We began working on three pages per team member. Pages were selected in sequence instead of a randomized or a diverse case basis, which we later identified as a possible shortcoming. Anyhow, each member used two tools including Segmentation and Transcription. First, segmentation refers to labeling of the different parts of a page such as page/folio numbers, main texts, marginalia and footnotes etc. To keep a uniform system of labelling, we created common segmentation guidelines in view of the Zone guideline system used by Segmonto Documentation4 and the variations of regions existing in our samples of 3 pages each between this team and our other course mates who were digitizing another manuscript written in Persian. In total, we had 21 pages to start with between 7 students (3 pages each). You can see the segmentation guidelines including a list and explanation of each region/zone label here. These labels were input as a common ontology in each document (3 pages each). A segmentation model used previously by the OpenITI team was used to run automatic segmentation. Then the segmentation was corrected for regions and lines, and regions were labeled according to the guidelines.


![Image: Screenshot of a segmentation process on Escriptorium]({{ site.baseurl }}/assets/images/segmentation.png)


![Image: Screenshot of a transcription process on Escriptorium]({{ site.baseurl }}/assets/images/transcription.jpg)


Second, an automatic transcription was applied on each document using a kraken based model. This was followed by manual transcription of each page. Third, the same process of fine-tuning transcription and segmentation was applied for two new pages per student. At the end of the process, the models were fine-tuned for a total of 35 pages between all students of course consisting of two teams for each manuscript. The segmentation and transcription models were finetuned and then trained using the feedback of the fine-tuning process. Fourth, automatic segmentation and transcription were applied on all pages of the manuscript. This was not corrected/fine-tuned further. The OCR process was concluded here. You can [click here]({{ site.baseurl }}/project1-digitization/README.txt) to see the output of the transcription in ALTO XML format as well as the images of the manuscript.


![Image: Screenshot of export process of ALTO XML files including images on Escriptorium]({{ site.baseurl }}/assets/images/export_screenshot.jpg)


Finally, OCR models were tested for Character Error Rates5 and Character Accuracy Rates6 using a python script comparing the manual transcriptions and the transcriptions conducted by the model. [Click here](https://github.com/haiderooo/portfolio/tree/master/project1-digitization/CAR_CER_Comparison/ground_truth_layers) to see the manual transcription text files (ground truth) and here [Click here](https://github.com/haiderooo/portfolio/tree/master/project1-digitization/CAR_CER_Comparison/model_transcriptions) to see the model transcription layers. Through this process the model “kraken_gen2-print-n7m5-union-ft_best” delivered the most optimal results with a CER of 0.165 (CAR: 0.835) and WER7 of 0.47. [Click here]({{ "project1-digitization/CAR_CER_Comparison/haider_evaluate_transcription.py" | relative_url }}) to see the python script utilized for the test.


The process of digitization provided a useful experience in learning multiple technical steps involved in a digital humanities project. At the same time, it provided practical results in the form of training and testing a model for a historically valuable manuscript. One shortcoming of the project as identified earlier was the non-systematic selection of training data. This is taken as a learning from the project. At the beginning of the project we had an idea of what Machine Learning generally meant and what large-scale digital humanities projects look like8. However, from the theory, we went into a hands-on experience of what it means to do a DH project, which exposed us to both the tools and the method in its systematic and complex reality.


# Project related files:
- [ALTO XML files of transcribed manuscript exported from Escriptorium (including images)]({{ '/project1-digitization/README.txt' | relative_url }})
- [Python script for CER, CAR and WER comparison]({{ '/project1-digitization/CAR_CER_Comparison/haider_evaluate_transcription.py' | relative_url }})
- [Ground truth (manual transcription text files)]({{ '/project1-digitization/CAR_CER_Comparison/ground_truth_layers/' | relative_url }})
- [Model transcription layers (text files)]({{ '/project1-digitization/CAR_CER_Comparison/model_transcriptions/' | relative_url }})
- [Segmentation guidelines]({{ '/project1-digitization/segmentation_guidelines_DH25.pdf' | relative_url }})
- [Manuscript metadata]({{ '/project1-digitization/Rasail_Metadata.txt' | relative_url }})
- [Table of contents (csv file)]({{ '/project1-digitization/Rasail_Group_Sheet2.csv' | relative_url }})


# EndNotes:


1. Machine Learning. <https://haiderooo.github.io/portfolio/project1/2025/10/12/ml-podcast-cs50-summary.html>
2. Escriptorium. <https://escriptorium.openiti.org/>
3. Sidenote on the long-hyphen: I have always loved to use the long-hyphen to manage a complex sentence but its overuse by ChatGPT has meant that people now see it as a sign of AI text generation. This is another example of the now increasingly blurred lines between LLM generated text patterns and pre/post normalized patterns in natural language.
4. Segmonto. <https://segmonto.github.io/>
5. Character Error Rates. <https://haiderooo.github.io/portfolio/project1/2025/10/21/Eval_OCR.html>
6. Character Accuracy Rates. <https://haiderooo.github.io/portfolio/project1/2025/10/21/Eval_OCR.html>
7. Word Error Rates. <https://haiderooo.github.io/portfolio/project1/2025/10/21/Eval_OCR.html>
8. FIHRIST PROJECT. <https://haiderooo.github.io/portfolio/summary%20of%20a%20dh%20project/2025/09/16/about-fihrist.html>



