import numpy as np
import nltk
import cPickle
import collections
import os
import matplotlib.pyplot as plt
import numpy as np

NUM_SAMPLE = 15

class Document_Data():
    def __init__(self, filename, f, gloveDict):
        self.filename = filename
        self.wordDict = collections.defaultdict(int)
        self.wordList = []
        self.closestWords = []
        self.rank = 0
        for line in f:
            tokens = nltk.tokenize.word_tokenize(line.decode('utf8'))
            for x in tokens:
                if x in gloveDict: self.wordDict[x] += 1
                self.wordList += [word for word in tokens if word in gloveDict]

    def getRank(self, gloveDict, embeddings,targets):
        distanceList = [(x, min([np.linalg.norm(embeddings[gloveDict[curTarget]] - embeddings[gloveDict[x]]) for curTarget in targets])) for x in self.wordDict]
        distanceList = sorted(distanceList, key = lambda x: x[1])
        sumList = [self.wordDict[x[0]]*x[1] for x in distanceList[0:NUM_SAMPLE]]
        #storer[name] = [(x[0], self.wordDict[x[0]]) for x in distanceList[0:NUM_SAMPLE]]
        self.rank =  sum(sumList)/float(sum([self.wordDict[x[0]] for x in distanceList[0:NUM_SAMPLE]]))
        self.closestWords = distanceList[0:NUM_SAMPLE]
        print self.rank
        return self.rank


def record_rankings(sorted_document_data, targets):
    textData = open('Rankings_' + '_'.join(targets) + '.txt', 'w')
    count = 0
    for doc in sorted_document_data:
        textData.write(str(count) + ': ' + doc.filename + ' :' + str(doc.rank)+'\n')
        for word in doc.closestWords:
            textData.write(word[0] + ': ' + str(word[1]) + '\n')
        count += 1
        textData.write('-----------------------------------------\n')

def graph_rankings(sorted_document_data, targets):
    keys = [x.filename[:-8] for x in sorted_document_data]
    vals = [x.rank for x in sorted_document_data]
    x_pos = np.arange(len(keys))
    plt.figure()
    plt.bar(x_pos, vals, align='center', alpha=0.5)
    plt.xticks(x_pos, keys, rotation = 'vertical')
    plt.ylabel('Distance Metric')
    plt.title('Distance from target words: ' + ' '.join(targets))
    plt.tight_layout()
    plt.savefig('Distances' + ' _'.join(targets))
    #plt.show()

def main(argumentList):
    gloveDict = cPickle.load(open('labelsDict'))
    embeddings = np.load(open('embeddings'))
    for targetList in argumentList:
        docu_datas = []
        for filename in os.listdir('./Textified_Reports'):
            if filename[-4:] == '.txt':
                docu_datas.append(Document_Data(filename, open('./Textified_Reports/'+filename), gloveDict))
                docu_datas[-1].getRank(gloveDict, embeddings, targetList)
        finalRankings = sorted(docu_datas, key = lambda x: x.rank)
        record_rankings(finalRankings, targetList)
        graph_rankings(finalRankings, targetList)



main([['culture','gender','ethnicity'], ['gender'],['culture'],['ethnicity'],['elderly'],['poverty'])

#'Europe','Asia','America','Africa', 'China', 'Germany', 'France', 'Italy', 'Mexico', 'Switzerland', 'Canada', 'England', 'Japan', 'Sweden', 'Australia', 'Spain', 'India', 'Russia'
