#-------------------------------------------------------------------------------
# Name:        FreeWritingParse.py
# Purpose:      Bigram Split for Hebrew text file
#
# Author:      Gal Hai
#
# Created:     25/03/2017
# Copyright:   (c) shmuelHanagid 2017
#-------------------------------------------------------------------------------

#!/usr/bin/python3
import codecs
import string
import random
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from nltk import ngrams # need to install this: python -m pip install nltk
import re

NUM_CONTROLLED = 10;
NUM_GENERATED_USER_BIGRAMS = 10; # for every 'half' of the user raw text.
inputSID = input('Please Enter Subject ID (numbers Only)\n')

preTestFile = codecs.open('PreTest_' + inputSID + '.txt','w',encoding='UTF-8')



def SplitHebFileToBigrams(filename):
# ***********************************
# Read Special encoding:
# **********************************
    f = codecs.open(filename,'r',encoding='UTF-8')


# *************************************************
# Split with multiple delimiters, for comprehensive bigrams:
# *************************************************
    allFileText = f.read()
    rawSentences = [] # this list will hold all 'natural segments' of the sentence.
    regex = re.compile(r'[%s\n]+' % re.escape(string.punctuation))
    for segment in regex.split(allFileText):
        rawSentences.append(segment.strip())



# to debug sentences:
##for sen in rawSentences:
##    print sen

# ***********************************
# Split to Bigrams:
# **********************************

##sentence = 'this is a foo bar sentences and i want to ngramize it'
    bigrams = []  # this list will hold all bi grams eventually.
    for sentence in rawSentences: #go over all sentences found
        tmpBigrams = ngrams(sentence.split(), 2)
        for grams in tmpBigrams:
            if grams not in bigrams:
                bigrams.append(grams)


    return bigrams




# ***********************************
# Browse GUI to get file:
# **********************************

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
##print(filename)

controlledFilename = u'controlledBigrams.txt'


userBigrams = SplitHebFileToBigrams(filename)
conBigrams = SplitHebFileToBigrams(controlledFilename)



## to print the bigrams (debug purpose):
# for gram in conBigrams:
   # for word in gram:
       # print word,
   # print


readyUsergrams = []
readyCongrams = []

for gram in userBigrams:
    if gram not in conBigrams:
        readyUsergrams.append(gram)


for gram in conBigrams:
    if gram not in userBigrams:
        readyCongrams.append(gram)



# to print the bigrams (debug purpose):
# for gram in readyCongrams:
    # for word in gram:
        # print word,
    # print


numChosenConbgrams = min(len(readyCongrams),NUM_CONTROLLED)


preTestFile.write('Unique Controlled Bigrams:\n------\n')
for idx in range(numChosenConbgrams):
    for word in readyCongrams[idx]:
        preTestFile.write(word + ' ')
    preTestFile.write('\n')
preTestFile.write('------\n')

N = len(readyUsergrams);
firstHalfIdxs = random.sample(range(0,int(N/2)),NUM_GENERATED_USER_BIGRAMS);
secHalfIdxs = random.sample(range(int(N/2) + 1, N),NUM_GENERATED_USER_BIGRAMS);

preTestFile.write('Unique User First Half Bigrams:\n------\n')
for idx in firstHalfIdxs:
    for word in readyUsergrams[idx]:
        preTestFile.write(word + ' ')
    preTestFile.write('\n')
preTestFile.write('------\n')

preTestFile.write('Unique User Second Half Bigrams:\n------\n')
for idx in secHalfIdxs:
    for word in readyUsergrams[idx]:
        preTestFile.write(word + ' ')
    preTestFile.write('\n')
preTestFile.write('------\n')




preTestFile.close()









