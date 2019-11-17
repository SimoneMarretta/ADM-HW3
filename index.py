# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 17:42:53 2019

@author: simo2
"""

from index_utils import *
#Building the vocabulary
vocabulary = building_and_save_vocabulary(30001,'C:/Users/simo2/tsv files project aris final and cleaned/articolo')
#Building the Inverted_index
Inverted_index=invertedIndexAdd(30001,vocabulary,'C:/Users/simo2/tsv files project aris final and cleaned/articolo')
#Building the Inverted index TFIDF
index_tfidf=Index_TFIDF(30001,vocabulary,Inverted_index,'C:/Users/simo2/tsv files project aris final and cleaned/articolo')