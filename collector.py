# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 16:33:16 2019

@author: HP
"""
import pandas as pd
import csv
from bs4 import BeautifulSoup
import requests
import time

# The follow code take all the link which are in files movies 1, 2 ,3 and put them in list "link"
links = []
path="C:/Users/HP/Desktop/file hw3/"
movies1=open(path+'movies1.html', "r")
soup_movies1 = BeautifulSoup(movies1, 'lxml')

movies2=open(path+'movies2.html', "r")
soup_movies2 = BeautifulSoup(movies2, 'lxml')

movies3=open(path+'movies3.html', "r")
soup_movies3 = BeautifulSoup(movies3, 'lxml')

for tag in soup_movies1.find_all('a', href=True):
    links.append(tag['href'])

for tag in soup_movies2.find_all('a', href=True):
    links.append(tag['href'])
    
for tag in soup_movies3.find_all('a', href=True):
    links.append(tag['href'])

# The function below make a for loop through the list "links" for obtain the different lists of urls
get_url(links,path)