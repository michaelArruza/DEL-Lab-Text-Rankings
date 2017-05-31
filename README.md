# DEL-Lab-Text-Rankings
This repository contains two programs that may be useful to researchers that deal with text data:
getRank.py: This program allows the user to rank documents based on their proximity to certain target words. For example, one could see which documents talk the most about culture or gender and which ones have different topics. Note that a document does not need to specifically mention the target words to correlate highly with them; documents using synonyms or words that are close in meaning to the target words will also correlate highly. Creates both a text file summarizing the ordering and distance metrics of each document and the words in the document most closely correlated with the target words, and a bar graph showing the distance metrics of the different documents against each other.

code_sentences.py: This program works similarly to getRank, but ranks groups of words within the document against each other. This is useful if a researcher is looking for the specific places in a document wherein an author talks about a particular topic (or things closely related to that topic). Creates a text file ranking the groups of words from closest to farthest.

Requirements:
All of the programs here require the use of a computer with the following programs installed:
-Python 2
-Numpy
-Matplotlib
-Nltk (Natural Language Toolkit)

Use:
In order to use the programs, documents must be converted to .txt format (if they are in pdf format, a converter such as pdftotext may be used) and placed within a folder in the same location as the programs. The user must also specify where they would like the graphs and text files created by the program to be saved in, and the target words to be utilized. These can be specified by opening the program files and altering the fields pspecified within.
