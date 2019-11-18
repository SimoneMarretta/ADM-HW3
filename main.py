# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 19:09:08 2019

@author: simo2
"""
from collections import defaultdict
from IPython import get_ipython
from scipy import spatial
import heapq
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
#Choose your search engine
choice=int(input('Choose your search engine:\n1 for the simpler one\n2 for a search engine that ranks films based on the cosine similarity with your query\n3 actors-based search engine\n--> '))
#Insert your query
query=input('Insert your query\n--> ')
#A function that is useful because it cleans the string from punctuations and stopwords.Moreover it stems the word
def documents_list(Inverted_index,cleaned_query):
        documents_appearances = set(Inverted_index[cleaned_query[0]])
        for i in range(1, len(cleaned_query)):
                    documents_appearances = documents_appearances.intersection(Inverted_index[cleaned_query[i]])
        documents_appearances=list(documents_appearances)
        return documents_appearances
def building_conjunctive_film_dataframe(path,documents_appearances,links):
        conjunctive_film_dataframe=pd.DataFrame(columns=['Title','Intro','Wikipedia Url'])#We create an empty dataframe
        for i in range(len(documents_appearances)):#We make a for loop:We retrieve the tsv,we clean it and we append it to the conjunctive film dataframe
            number_of_document=(documents_appearances[i].split('_'))[1]
            film_dataframe=pd.read_csv(path+'articolo'+number_of_document+'.tsv',encoding = 'utf-8', sep="\t")
            film_dataframe=film_dataframe[['Title','Intro']]
            film_dataframe['Wikipedia Url']=links[int(number_of_document)-1]
            conjunctive_film_dataframe=conjunctive_film_dataframe.append(film_dataframe,ignore_index=True)
        return conjunctive_film_dataframe    

def string_cleaning(text):
    if type(text) is str:
        
        tokenizer = RegexpTokenizer(r'\w+')
        words = tokenizer.tokenize(text)
        
        stopWords = set(stopwords.words('english'))
        wordsFiltered = []
        for w in words:
            if w not in stopWords:
                wordsFiltered.append(w)
        
        porter = PorterStemmer()
        listOfWords = [porter.stem(word) for word in wordsFiltered]
        result = ' '.join(listOfWords)
    else:
        result = np.nan
    return result  
links = []#the code creates a links list with BeautifulSoup and appends the link that we have.
#They are useful to retrieve the Wikipedia Urls
html_file=open(r'C:\Users\simo2\OneDrive\Desktop\arishomework3\filmproject.html', "r")
soup = BeautifulSoup(html_file, 'lxml')
for tag in soup.find_all('a', href=True):
    links.append(tag['href'])
html_file=open(r'C:\Users\simo2\OneDrive\Desktop\arishomework3\filmproject2.html', "r")
soup = BeautifulSoup(html_file, 'lxml')
for tag in soup.find_all('a', href=True):
    links.append(tag['href']) 
html_file=open(r'C:\Users\simo2\OneDrive\Desktop\arishomework3\filmproject3.html', "r")
soup = BeautifulSoup(html_file, 'lxml')
for tag in soup.find_all('a', href=True):
    links.append(tag['href']) 
if choice==1:
    cleaned_query=string_cleaning(query).split()#We clean the string
    cleaned_query = [vocabulary[key] for key in cleaned_query  if key in vocabulary]#Integer from the vocabulary of the query's words 
    #This lines of codes helps us to make a list of the documents that contain all of the query's words
    documents_appearances=documents_list(Inverted_index,cleaned_query)
    
    #We want to create a dataframe to display the output
    conjunctive_film_dataframe=building_conjunctive_film_dataframe('C:/Users/simo2/tsv files project aris/',documents_appearances,links)
    print(conjunctive_film_dataframe)
if choice==2:
    def cosine_similarity(array1,array2):#cosine similarity function
        return(1 - spatial.distance.cosine(array1, array2))
    k = int(input('Choose the number of documents you want as output\n--> '))#The user can choices how much documents he wants to display in the output
    cleaned_query=string_cleaning(query).split()
    #We create a TF dictionary of all the words in the query
    dict_TF = defaultdict(float)
    len_q = len(cleaned_query)
    for word in cleaned_query:
        term_id = vocabulary[word]
        dict_TF[term_id] += 1/len_q
        
    int_query = [vocabulary[key] for key in cleaned_query  if key in vocabulary]#The same as we did in the first search engine
    cleaned_query = dict_TF #Our cleaned_query becomes the dict that we have just created
    documents_appearances=documents_list(Inverted_index,int_query)
    result=documents_appearances
    dict_list_doc_words = defaultdict(list)
    for word in cleaned_query:#The tfidf of each word related to the document
            for elem in index_tfidf[word]:
             
                if elem[0] in result:
                    dict_list_doc_words[elem[0]].append(elem[1]) 
    heap = []#We create an heap structure to display only the first k documents as output
    list_query = list(cleaned_query.values())
    
    for doc in dict_list_doc_words:
        heapq.heappush(heap, (cosine_similarity(list_query, dict_list_doc_words[doc]), doc))
    heap_result = heapq.nlargest(k, heap)#We have a list of tuples.Each tuple is the document and the similarity of this document with the query
    similarity_film_dataframe=pd.DataFrame(columns=['Title','Intro','Wikipedia Url','Similarity'])
    
    for i in range(len(heap_result)):
        number_of_document=(heap_result[i][1].split('_'))[1]
        film_dataframe=pd.read_csv(r'C:\Users\simo2\tsv files project aris\articolo'+number_of_document+'.tsv',encoding = 'utf-8', sep="\t")
        film_dataframe=film_dataframe[['Title','Intro']]
        film_dataframe['Wikipedia Url']=links[int(number_of_document)-1]
        film_dataframe['Similarity']=round(heap_result[i][0],2)
        similarity_film_dataframe=similarity_film_dataframe.append(film_dataframe,ignore_index=True) 
    print(similarity_film_dataframe)    
if choice==3:# actors-based search engine
    actors=input('Insert the surname of your favorite actor or actors if you want,so we can rank your films in an easier way\n--> ').split()  
    cleaned_query=string_cleaning(query).split()
    int_query = [vocabulary[key] for key in cleaned_query  if key in vocabulary]
    documents_appearances=documents_list(Inverted_index,int_query)#A list of all the documents that contain all the query's words
    
    dict_actors_film={}
    for i in range(len(documents_appearances)):#W do a for loop to create a dictionary that have as keys the films and as values the actors in that particular film
        try:
            number_of_document=(documents_appearances[i].split('_'))[1]
            film_dataframe=pd.read_csv('C:/Users/simo2/tsv files project aris final and cleaned/'+'articolo'+number_of_document+'.tsv',encoding = 'utf-8', sep="\t")
            actors_string=film_dataframe['Starring'][0].split()
            dict_actors_film[number_of_document]=actors_string
        except:
            continue            
    #We take into consideration the actors that the user chose
    dict_plus_scores={}
    
    for j in range(len(documents_appearances)):#We search if the actors that the user chose are in the dict_actors_film.If that is the case,we add a score of 0.025 to the film.
        count=0
        for i in range(len(actors)):
            try:
        #for each actor we add 0.025
                number_of_document=(documents_appearances[j].split('_'))[1]
                if actors[i] in dict_actors_film[number_of_document]:
                    count+=0.025
                    dict_plus_scores[number_of_document]=count 
            except:
                continue
             
    dict_list_doc_words = defaultdict(list)
    
    for word in int_query:#The tfidf of each word related to the document
            for elem in index_tfidf[word]:
             
                if elem[0] in documents_appearances:
                    dict_list_doc_words[elem[0]].append(elem[1]) 
    k = int(input('Choose the number of documents you want as output\n--> '))
    for i in range(len(documents_appearances)):#We append eventually the actors scores 
        number_of_document=(documents_appearances[i].split('_'))[1]
        if number_of_document in dict_plus_scores:
            dict_list_doc_words[documents_appearances[i]].append(dict_plus_scores[number_of_document])            
    heap = []
    
    for doc in dict_list_doc_words:
        heapq.heappush(heap, (sum(dict_list_doc_words[doc]), doc))#Heap structure,we use to make the rank the sum of all the tf-idf between the query's word and the documents
    heap_result = heapq.nlargest(k, heap)
    Actors_engine_dataframe=pd.DataFrame(columns=['Title','Intro','Wikipedia Url','Ranking score'])
    for i in range(len(heap_result)):#We create the dataframe
        try:
            number_of_document=(heap_result[i][1].split('_'))[1]
            add_df=pd.read_csv(r'C:\Users\simo2\tsv files project aris\articolo'+number_of_document+'.tsv',encoding = 'utf-8', sep="\t")
            add_df=add_df[['Title','Intro']]
            add_df['Wikipedia Url']=links[int(number_of_document)-1]
            add_df['Ranking score']=heap_result[i][0]
            Actors_engine_dataframe=Actors_engine_dataframe.append(add_df,ignore_index=True)
        except:
            continue            
print(Actors_engine_dataframe)        