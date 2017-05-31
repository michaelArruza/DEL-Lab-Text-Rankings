import numpy as np
import nltk
import cPickle
import collections
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

#Constants: change these depending on the folders you want to save files and graphs
#in and the parameters you want the program to use.
#-------------------------------------------------------------------------------------------------------------
#NUM_SAMPLE is the number of words closest to the target words used when sampling.
#Set higher or lower depending on the size of the documents being compared
#(For larger documents a bigger NUM_SAMPLE may yield better results)
NUM_SAMPLE = 15

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
TARGETS = [['ethnicity','culture','gender']]
#-----------------------------------------------------------------------------------------------------
#End of Variables. From here on out, unless you are familiar with coding or Python,
#it is highly recommended that nothing below is altered. (if you are familiar with coding,
#feel free to alter as needed!)

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
        self.rank =  sum(sumList)/float(sum([self.wordDict[x[0]] for x in distanceList[0:NUM_SAMPLE]]))
        self.closestWords = distanceList[0:NUM_SAMPLE]
        print self.rank
        return self.rank


def record_rankings(sorted_document_data, targets):
    textData = open(FOLDER_FOR_SAVING+'/Rankings_' + '_'.join(targets) + '.txt', 'w')
    count = 0
    for doc in sorted_document_data:
        textData.write(str(count) + ': ' + doc.filename + ' :' + str(doc.rank)+'\n')
        for word in doc.closestWords:
            textData.write(word[0] + ': ' + str(word[1]) + '\n')
        count += 1
        textData.write('-----------------------------------------\n')

def graph_rankings(sorted_document_data, targets):
    #[:10]
    keys = [x.filename[:-8].decode('utf8') for x in sorted_document_data]
    print keys
    vals = [x.rank for x in sorted_document_data]
    x_pos = np.arange(len(keys))
    plt.figure()
    plt.bar(x_pos, vals, align='center', alpha=0.5)
    plt.xticks(x_pos, keys, rotation = 'vertical')
    plt.ylabel('Distance Metric')
    plt.title('Distance from target words: ' + ' '.join(targets))
    plt.tight_layout()
    plt.savefig('Graphs' + '/Distances' + ' _'.join(targets))
    #plt.show()

def main(argumentList):
    gloveDict = cPickle.load(open('labelsDict'))
    embeddings = np.load(open('embeddings'))
    for targetList in argumentList:
        docu_datas = []
        for filename in os.listdir('./'+ TEXT_FOLDER):
            if filename[-4:] == '.txt':
                docu_datas.append(Document_Data(filename, open('./'+ TEXT_FOLDER+'/'+filename), gloveDict))
                docu_datas[-1].getRank(gloveDict, embeddings, targetList)
        finalRankings = sorted(docu_datas, key = lambda x: x.rank)
        record_rankings(finalRankings, targetList)
        graph_rankings(finalRankings, targetList)



main(TARGETS)

#The following two methods are methods that I made to plot more complex graphs,
#left here in case someone wants to alter and use it, but note it is NOT
#used in the main program.
#---------------------------------------------------------------------------------------------------------------------------------
"""
def graph_rankings2(sorted_document_data, targets):
    colorDict = {'CS':'red', 'Math': 'blue', 'Gender Studies': 'green', 'Sociology': 'yellow', 'Psychology':'brown', '311c':'magenta'}
    keys = [x.folder[:-9] for x in sorted_document_data]
    vals = [x.rank for x in sorted_document_data]
    x_pos = np.arange(len(keys))
    plt.figure()
    bars = plt.bar(x_pos, vals, align='center', alpha=0.5)
    for i in range(len(bars)):
        bars[i].set_color(colorDict[sorted_document_data[i].folder[:-9]])
    plt.legend(handles = [mpatches.Patch(color=colorDict[key], label= key) for key in colorDict] )
    plt.xticks(x_pos, keys, rotation = 'vertical')
    plt.ylabel('Distance Metric')
    plt.title('Distance from target words: ' + ' '.join(targets))
    plt.tight_layout()
    plt.savefig(FOLDER_FOR_SAVING + '/Distances_' + ' _'.join(targets))
    #plt.show()
def main2(argumentList, folderList):
    gloveDict = cPickle.load(open('labelsDict'))
    embeddings = np.load(open('embeddings'))
    for targetList in argumentList:
        docu_datas = []
        for folder in folderList:
            for filename in os.listdir('./Readable Files/'+ folder):
                if filename[-4:] == '.txt':
                    docu_datas.append(Document_Data(filename, open('./'+ 'Readable Files/'+filename), gloveDict))
                    docu_datas[-1].getRank(gloveDict, embeddings, targetList)
                    docu_datas[-1].folder = folder
        finalRankings = sorted(docu_datas, key = lambda x: x.rank)
            #record_rankings(finalRankings, targetList)
        graph_rankings2(finalRankings, targetList)
    #plt.show()
"""
#--------------------------------------------------------------------------------------------------------------------------------------
