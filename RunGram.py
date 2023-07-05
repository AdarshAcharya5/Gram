# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 18:49:20 2022

@author: Adarsh Acharya
"""

from gramformer import Gramformer
import torch
from textblob import TextBlob 
from tkinter import *
from PIL import ImageTk, Image


def set_seed(seed):
  torch.manual_seed(seed)
  if torch.cuda.is_available():
    torch.cuda.manual_seed_all(seed)

set_seed(1212)
gf = Gramformer(models = 1, use_gpu=False) 

Tags_Index={'CC': 'coordinating conjunction',
'CD':'cardinal digit',
'DT' : 'determiner',
'EX' : 'existential there (like: “there is” … think of it like “there exists”)',
'FW' : 'foreign word',
'IN' : 'preposition/subordinating conjunction',
'JJ' : 'adjective',
'JJR' : 'adjective, comparative',
'JJS' : 'adjective, superlative',
'LS' : 'list marker',
'MD' : 'modal could, will',
'NN' :  'noun, singular',
'NNS' : 'noun plural',
'NNP' : 'proper noun, singular',
'NNPS' : 'proper noun, plural',
'PDT' :  'predeterminer',
'POS' : 'possessive ending',
'PRP' : 'personal pronoun I, he, she',
'PRP$' : 'possessive pronoun my, his, hers',
'RB' : 'adverb',
'RBR' : 'adverb, comparative',
'RBS' : 'adverb, superlative',
'RP' : 'particle give up',
'TO' : 'to go ‘to‘',
'UH' : 'interjection',
'VB' : 'verb, base form',
'VBD' : 'verb, past tense',
'VBG' : 'verb, gerund/present participle',
'VBN' : 'verb, past participle',
'VBP' : 'verb,present',
'VBZ' : 'verb, 3rd person. present',
'WDT' : 'wh-determiner which',
'WP' : 'wh-pronoun who, what',
'WP$' : 'possessive wh-pronoun whose',
'WRB' : 'wh-adverb where, when'}


def getPolarity(text):
    return TextBlob(text).sentiment.polarity

def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity

def getTags(text):
    return TextBlob(text).tags


def getcorrectedsentence(influent_sentence):
    corrected_sentence = gf.correct(influent_sentence, max_candidates=1)
    return corrected_sentence


def getPolarityExplanation(corrected_sentence):
    Polarity=getPolarity(corrected_sentence)
    PExplanation=''
    if int(Polarity*100)==-100:PExplanation="\n This sentence is heavily negative -> Polarity : "+str(Polarity)
    elif int(Polarity*100)==0:PExplanation="\n This sentence is neutral (Most likely a Fact/Question/Statement) -> Polarity : "+str(Polarity)
    elif int(Polarity*100)==100:PExplanation="\n This sentence is heavily positive -> Polarity : "+str(Polarity)
    elif int(Polarity*100) >-100 and int(Polarity*100) <= -50:PExplanation="\n This sentence is negative -> Polarity : "+str(Polarity)
    elif int(Polarity*100) >-50 and int(Polarity*100) < 0:PExplanation="\n This sentence is mildly negative -> Polarity : "+str(Polarity)
    elif int(Polarity*100) > 0 and  int(Polarity*100) <= 50:PExplanation="\n This sentence is mildly positive -> Polarity : "+str(Polarity)
    else:PExplanation="\n This sentence is positive -> Polarity : "+str(Polarity)
    return PExplanation
    
    
def getSubjectivityExplanation(corrected_sentence):
    Subjectivity=getSubjectivity(corrected_sentence)
    SExplanation=''
    if int(Subjectivity*100)==0:SExplanation="\n This sentence is heavily factual -> Subjectivity : "+str(Subjectivity)
    elif int(Subjectivity*100)==100:SExplanation="\n This sentence contains a strong personal opinion -> Subjectivity : "+str(Subjectivity)
    elif int(Subjectivity*100) > 0 and int(Subjectivity*100) < 50:SExplanation="\n This sentence is mostly factual -> Subjectivity : "+str(Subjectivity)
    else:SExplanation="\n This sentence is mostly a personal opinion -> Subjectivity : "+str(Subjectivity)
    return SExplanation


#Main GUI + Correction Function Call
def MakeGramGUI():
    def correction(e):
        #Getting influent sentence + first correction layer
        influent_sentence_temp=tf.get(1.0,END + "-1c")+e.char
        test=list(influent_sentence_temp.split("\n"))
        influent_sentence=test[-1]
        corrected_sentence=str(TextBlob(influent_sentence).correct())
        tf.delete(1.0, END)
        
        #second correction layer
        corrected_sentence_2=''.join(ele for ele in getcorrectedsentence(corrected_sentence))
        
        #Polarity + Subjectivity getter methods
        polarity.configure(text=getPolarityExplanation(corrected_sentence_2))
        subjectivity.configure(text=getSubjectivityExplanation(corrected_sentence_2))
        
        #Tagging
        tempstring=''
        tagsList=getTags(corrected_sentence_2)
        for t in tagsList:
            word,tags=t
            if not (tagsList.index(t)%3):
                tempstring+="\n"
            tempstring+=str("["+word+"]"+" : "+Tags_Index[tags]+" ")
            tag.configure(text="Tags : "+tempstring)
            
        #Insertion of corrected sentence
        test[-1]=corrected_sentence_2
        final_sentence=''.join(ele+"\n" for ele in test)
        tf.insert(1.0,final_sentence[:-1])
        
        
    
    #Root Frame    
    root = Tk()
    root.geometry("800x800")
    root.configure(background="black")
    root.title("Gram: grammar, made light")
    root.resizable(False, False)
    
    #Image Configurations
    img = Image.open("G2.png")
    resized = img.resize((350,350))
    logo = ImageTk.PhotoImage(resized)
    logolbl = Label(root, image=logo,background="black")
    logolbl.place(x=227,y=-100)
    
    #TextBox
    tf = Text(root, height=6, width=80, background="black", foreground="white", insertbackground="white")
    tf.place(x=80, y=220)
    
    tf.bind("<Return>", correction)
    
    prompt = Label(root, text="Enter text here:", background="black", foreground="white", font=('Helvetica', 10))
    prompt.place(x=80, y=190)
    
    #Polarity Label
    polarity = Label(root, text="Polarity : ",background="black", foreground="white", font=('Helvetica', 10))
    polarity.place(x=80, y=340)
    
    #Subjectivity Label
    subjectivity = Label(root, text="Subjectivity : ", background="black", foreground="white", font=('Helvetica', 10))
    subjectivity.place(x=80, y=380)
    
    #Tags Label
    tag = Label(root, text="Tags: ", background="black", foreground="white", font=('Helvetica', 10))
    tag.place(x=80, y=430)
    
    #Footer
    disclaimer = Label(root, text="A light-weight Grammer correction tool by Adarsh Acharya & Amogh Shet", background="black", foreground="white", font=('Helvetica', 8), fg='white')
    disclaimer.place(x=175, y=695)

    root.mainloop() 

MakeGramGUI()

      
