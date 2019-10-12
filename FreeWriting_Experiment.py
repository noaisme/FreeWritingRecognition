#-------------------------------------------------------------------------------
# Name:        Automatic Writing Experiment
# Purpose:      Conduct the experiment, using data from previous files
#
# Author:      Gal Hai
#
# Created:     10/05/2017
# Copyright:   (c) shmuelHanagid 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import codecs
import string
import random
# import tkinter.messagebox
from tkinter import *
from tkinter.filedialog import askopenfilename
from nltk import ngrams # need to install this: python -m pip install nltk
import re


Katavti = u'\u05db\u05ea\u05d1\u05ea\u05d9'
LoKatavti = u'\u05dc\u05d0  \u05db\u05ea\u05d1\u05ea\u05d9'
TOTAL_BIGRAMS_EXPECTED = 20



global order
global orderIdx
global allbGrams
global root
global bigramIdx
global resultFile
global inputSID
global welcomeTxt
global endTxt

def CustomMsgPopUp(msgTxt):
    global MsgRoot
    MsgRoot = Tk()
    MsgRoot.title("Experiment")
    d = CustomMsg(MsgRoot,msgTxt)
    MsgRoot.mainloop()
    return


def flipBigram(bigram):
    """ Simple function to flip the bigram, just for RTL text display correctness"""
    spl = bigram.split()
    flipped = spl[1] + " " + spl[0]
    return flipped

class CustomMsg:
    def __init__(self, parent,msgTxt):
        # Frame to place the label and buttons
        f = Frame(parent)
        f.pack()
        f.pack_propagate(True)

        # Label: this will show the current bigram text
        self.lbl = Label(f, text=msgTxt,justify = RIGHT)
        self.lbl.pack()
        # 'Lo / Katavti' buttons
        b1 = Button(f, text='OK', command=self.Done)
        b1.pack(pady=10,side = BOTTOM)


    def Done(self):
        global MsgRoot
        # destroy root object -> GUI disappears.
        MsgRoot.destroy()
        return

# BiGram data-type class, containing the text, half and user/Controlled data
class bigram:
    def __init__(self, txt , isuser, half):
        """Return a bigram object."""
        self.Text = txt
        self.isUser = isuser
        self.Half = half
        return


# GUI Class:
class MyDialog:
    def __init__(self, parent):
        global allbGrams
        global bigramIdx
        global welcomeTxt
        # Frame to place the label and buttons

        f = Frame(parent,width=250,height=120)
        f.pack(padx=15,pady=15)
        f.pack_propagate(0)


        # Label: this will show the current bigram text
        # self.lbl = Label(f, text=flipBigram(allbGrams[bigramIdx].Text))
        self.lbl = Label(f, text=allbGrams[bigramIdx].Text)
        self.lbl.pack()

        # 'Lo / Katavti' buttons
        b1 = Button(f, text=Katavti, command=self.katavti)
        b1.pack(pady=10,side = LEFT)
        b2 = Button(f, text=LoKatavti, command=self.lokatavti)
        b2.pack(padx=10,side = RIGHT)



    # User Hit 'Katavti':
    def katavti(self):
        global allbGrams
        global bigramIdx
        # Logic -> Determine if the bigram is indeed user or control data,
        #           and print results to file.



##        print(allbGrams[bigramIdx].Text + ' is the bigram')#debug print
##        print(str(allbGrams[bigramIdx].isUser) + ' : this is user input True/False') #debug print


        userAnswer = 'User'
        if (allbGrams[bigramIdx].isUser):
            # user indicated correctly that he wrote this bigram
            correctness = 'True'
            truthData = 'User'
            fault = '----'
        else:
            # user indicated in-correctly that he wrote this bigram
            correctness = 'False'
            truthData = 'Control'
            fault = 'Commission'
        # This function writes to file:
        self.writeData(allbGrams[bigramIdx],userAnswer,correctness,truthData,fault)
        # advances to next bigram in random order.
        self.MoveToNext()
        return

    #User Hit 'Lo Katavti': (very similar, complementary case)
    def lokatavti(self):
        global allbGrams
        global bigramIdx
        userAnswer = 'Control'
        if (allbGrams[bigramIdx].isUser):
            # user indicated in-correctly that he didn't write this bigram
            correctness = 'False'
            truthData = 'User'
            fault = 'Ommission'
        else:
            # user indicated correctly that he didn't write this bigram
            correctness = 'True'
            truthData = 'Control'
            fault = '----'

        self.writeData(allbGrams[bigramIdx],userAnswer,correctness,truthData,fault)
        self.MoveToNext()

        return

    def writeData(self,bigram,userAnswer,correctness,truthData,fault):
        global resultFile
        global inputSID
# file format: 'IDSID, Bigram,  UserAnswer,   Is answer Correct?,   Truth data,  fault class,  What half? \n'
# values are Comma seperated as this is a CSV file.
        resultFile.write(inputSID + ',\"' + bigram.Text.strip() + '\",' + userAnswer + ',' + correctness + ',' + truthData + ',' + fault + ',' + bigram.Half + '\n' )


        return

    def MoveToNext(self):
        global order
        global orderIdx
        global bigramIdx
        # the index of the random order is a global variable.
        orderIdx += 1
        if orderIdx >= len(order):
            # we are done, end the GUI infinite loop.
            self.EndLoop()
            return
        bigramIdx = order[orderIdx]
##        print('orderIdx is ' + str(orderIdx) )#debug print
##        print('bigramIdx is ' + str(order[orderIdx]) )#debug print

##        self.lbl.config(text=flipBigram(allbGrams[bigramIdx].Text))
        # Change the label text according to the updated bigram value
        # When localization issues occur, sometimes The bigram has to be switched since it is hebrew - RTL
        # self.lbl['text'] = flipBigram(allbGrams[bigramIdx].Text)
        self.lbl['text'] = allbGrams[bigramIdx].Text
        return




    def EndLoop(self):
        global root
        # destroy root object -> GUI disappears.
        root.destroy()
        return



# Small GUI handle for the "open file" protocol, used to load pretest file.
appFile = Tk() # just for "askopenfilename"...
appFile.withdraw() # we don't want a full GUI, so keep the root window from appearing


# prompt to enter the SID
inputSID = input('Please Enter Subject ID (numbers Only)\n')
##inputSID = 'testest'
filename = askopenfilename(title = 'Pick PreTest File for this subject ID') # show an "Open" dialog box and return the path to the selected file
appFile.destroy()

#open PreTest data file for reading
f = codecs.open(filename,'r',encoding='UTF-8')

# welcome and ending messages:
welcomeMsgPath = 'welcome.txt'
endMsgPath = 'Thanks.txt'
welcomeFile = codecs.open(welcomeMsgPath,'r',encoding='UTF-8')
endFile = codecs.open(endMsgPath,'r',encoding='UTF-8')
welcomeTxt = welcomeFile.read()
endTxt = endFile.read()

# Read all lines from pretest file.
allLines = f.readlines()

# 3 states in parsing the preTest File: Controlled bigrams part, 1st half, 2nd half. before all is state 0.
state = 0;

allbGrams = []
for line in allLines:
    if '------' in line:
        continue
    if 'Controlled' in line:
        state = 1
        continue
    if 'First Half' in line:
        state = 2
        continue
    if 'Second Half' in line:
        state = 3
        continue
    # assign bigrams according to 'state', while reading the file.
    if state == 1:
        allbGrams.append(bigram(line,False,'None'))
        continue
    if state == 2:
        allbGrams.append(bigram(line,True,'1st'))
        continue
    if state == 3:
        allbGrams.append(bigram(line,True,'2nd'))
        continue

if (len(allbGrams) < TOTAL_BIGRAMS_EXPECTED):
    print('Error! Expecting 20 Bigrams in PreTest file!')
    f.close()


#Prepare results file if input is valid.
resultFile = codecs.open('MemoryTestResults_' + inputSID + '.csv','wb',encoding='UTF-8')
resultFile.write('Subject ID,Bigram,UserAnswer,Is answer Correct?,Is it a user bigram?,Fault Type,What half?\n')


# Randomize an order to go over all of the data.
order = random.sample(range(len(allbGrams)),TOTAL_BIGRAMS_EXPECTED)
# Start running the GUI on this random order - these vars are global and used by GUI.
bigramIdx = order[0]
orderIdx = 0;

CustomMsgPopUp(welcomeTxt)

# initiate the GUI:
root = Tk()
root.title("Experiment")
d = MyDialog(root)
root.mainloop()


CustomMsgPopUp(endTxt)


resultFile.close()




