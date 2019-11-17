# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 17:40:17 2019

@author: simo2
"""
from collections import defaultdict
import numpy as np
import json
import pandas as pd
#This function creates a vocabulary that maps each word of the dataset to an integer
def building_and_save_vocabulary(n,path):
    vocabulary = {}
    integer = 1
    for i in range(1, n):
        try:
            df = pd.read_csv(path+str(i)+'.tsv',encoding = 'utf-8', sep="\t")#Create a dataframe for each tsv
            intro_and_plot = df['Intro'][0].split()+df['Plot'][0].split()#Save as a list the Intro and Plot section of each tsv
            for word in intro_and_plot:
                        if word not in vocabulary:
                            vocabulary[word] = integer
                            integer += 1 
        except:
            continue                       
    json.dump(vocabulary, open('vocabulary.json', 'w', encoding='utf-8'))                        
    json.load(open('vocabulary.json', 'r')) 
    return vocabulary
#This function creates an Inverted Index dictionary,so each integer(that refers to a word) has as values the documents in which is contained
#We use the dictionary that we have created
def invertedIndexAdd(n,vocabulary,path):
    Inverted_index={}
    for i in range(1,n):
        try:
            df = pd.read_csv(path+str(i)+'.tsv',encoding = 'utf-8', sep="\t")
            intro_and_plot = df['Intro'][0].split()+df['Plot'][0].split()
            if intro_and_plot!=[]:        
                for word in intro_and_plot:
                    term_id=vocabulary[word]
                    if term_id not in Inverted_index:
                        s = set()
                        a='document_'+str(i)
                        s.add(a)
                        Inverted_index[term_id]=s
                    else:
                        s2 = Inverted_index[term_id]
                        a = 'document_'+str(i)
                        s2.add(a)
                        Inverted_index[term_id]=s2
        except:
            continue               
    return Inverted_index
#This function returns a dictonary that maps for each word the list of documents in which it is contained in, and the relative tfIdf score
def Index_TFIDF(n,vocabulary,Inverted_index,path):
    
    inv_ind_TFIDF = defaultdict(list) 
                    
    for i in range(1,n):
        try:
            df = pd.read_csv(path+str(i)+'.tsv',encoding = 'utf-8', sep="\t")
            
            intro_and_plot = df['Intro'][0].split()+df['Plot'][0].split()
            dict_TF = defaultdict(int)           
            for word in intro_and_plot:
                term_id = vocabulary[word]
                dict_TF[term_id] += 1
                
                        
                #TFIDF
            for term_id in dict_TF:
                inv_ind_TFIDF[term_id].append(('document_'+str(i), (dict_TF[term_id]/len(intro_and_plot)) * (np.log(20000/(len(Inverted_index[term_id]))))))
        except:
            continue
    np.save('inv_ind_TFIDF.npy', inv_ind_TFIDF)
    inv_ind_TFIDF = np.load('inv_ind_TFIDF.npy',allow_pickle=True).item()
    return inv_ind_TFIDF