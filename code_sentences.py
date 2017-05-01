
import numpy as np
import nltk
import cPickle
import collections
import os
import matplotlib.pyplot as plt

WINDOW_SIZE = 20

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



def main(targetList):
    gloveDict = cPickle.load(open('labelsDict'))
    embeddings = np.load(open('embeddings'))
    wordList = []
    for filename in os.listdir('./Textified_Reports'):
        if filename[-4:] == '.txt':
            wordList = convertToArr(open('./Textified_Reports/'+'Merck-2015-Mabe.pdf.txt'), gloveDict, embeddings)
            wordList = getWindows(wordList)
            wordList = convertToDistaces(wordList, targetList, gloveDict, embeddings)
            wordList = sorted(wordList, key = lambda x: x[1])
            for word in wordList[0:10]:
                print word[0]
        break
main(['culture', 'ethnicity', 'racial'])
