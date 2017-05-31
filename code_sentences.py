
import numpy as np
import nltk
import cPickle
import collections
import os
import matplotlib.pyplot as plt

#Constants: change these depending on the folders you want to save files and graphs
#in and the parameters you want the program to use.
#-------------------------------------------------------------------------------------------------------------
#WINDOW_SIZE determines the length of a "sentence", when ranking. Set to longer or shorter
#Depending on preference.
WINDOW_SIZE = 20

#FOLDER_FOR_SAVING is the folder to which text files containing a summary of
#results will be saved. Folder must be in same folder as the program (unless
#you state the specific filepath). Make sure the file name is surrounded by
# ' or ", i.e. if your file name is Text Files, make sure to write "Text Files"
# or 'Text Files'.
FOLDER_FOR_SAVING = 'Text Files'

#TEXT_FOLDER is the name of the folder containing the documents to be analized.
#Files should be in .txt format. It is recommended that the TEXT_FOLDER contain
#only the documents to be analized and no other files.
#Make sure the file name is surrounded by
# ' or ", i.e. if your file name is Text Files, make sure to write "Text Files"
# or 'Text Files'.
TEXT_FOLDER = 'Readable Files'

#TARGETS is a variable representing the words that will be used as "targets" when comparing
#documents. Write the Target words inside two brackets, and separate them by comma
#if using multpiles at a time.
TARGETS = ['ethnicity','culture','gender']
#-----------------------------------------------------------------------------------------------------
#End of Variables. From here on out, unless you are familiar with coding or Python,
#it is highly recommended that nothing below is altered. (if you are familiar with coding,
#feel free to alter as needed!)


def convertToArr(f, gloveDict, embeddings):
    wordList = []
    for line in f:
        tokens = nltk.tokenize.word_tokenize(line.decode('utf8'))
        wordList += [(word, embeddings[gloveDict[word]]) for word in tokens if word in gloveDict]
    return wordList

def getWindows(wordList):
    windows = [wordList[i:i+WINDOW_SIZE] for i in  range(len(wordList)-WINDOW_SIZE+1)]
    return windows

def convertToDistaces(windowList, targets, gloveDict, embeddings):
    newList = []
    for window in windowList:
        distance = sum([min([np.linalg.norm(embeddings[gloveDict[curTarget]] - x[1]) for curTarget in targets]) for x in window])/len(window)
        newList.append(([x[0] for x in window], distance))
    return newList

def code_sentence(sentence, codes):
    gloveDict = cPickle.load(open('labelsDict'))
    embeddings = np.load(open('embeddings'))
    sentence = nltk.tokenize.word_tokenize(sentence)
    minCode = None
    minDist = 9999999999999
    for curCode in codes:
        curDist = sum([min([np.linalg.norm(embeddings[gloveDict[curTarget]] - embeddings[gloveDict[x]]) for curTarget in curCode]) for x in sentence])/len(sentence)
        if curDist <= minDist:
            minDist = curDist
            minCode = curCode
    print minCode
    print minDist


def main(targetList):
    gloveDict = cPickle.load(open('labelsDict'))
    embeddings = np.load(open('embeddings'))
    wordList = []
    for filename in os.listdir('./'+TEXT_FOLDER):
        if filename[-4:] == '.txt':
            wordList = convertToArr(open('./'+TEXT_FOLDER), gloveDict, embeddings)
            wordList = getWindows(wordList)
            wordList = convertToDistaces(wordList, targetList, gloveDict, embeddings)
            wordList = sorted(wordList, key = lambda x: x[1])
            write = open(FOLDER_FOR_SAVING+'/'+filename + '_sentences: ' + '_'.join(targetList), 'w')
            i = 0
            for word in wordList[0:100]:
                write.write(str(i) + ' Distance = ' + str(word[1]) + ' :\n' )
                write.write(' '.join(word[0]) + '\n')
                i+=1
main(TARGETS)
