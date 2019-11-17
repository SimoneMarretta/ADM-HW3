# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 16:35:50 2019

@author: HP
"""
import pandas as pd
import csv
from bs4 import BeautifulSoup
import requests
import time
#This function take all url of wiki pages
def get_url(links, path):
    i = 0
    for l in links:
        try:
            response = requests.get(l)
            soup = BeautifulSoup(response.text, 'html.parser')
            time.sleep(2)
            path_directory=path + str(i) +'.html'

            with open(path_directory, "w", encoding='utf-8') as file:
                file.write(str(soup))
                file.close()
            i+=1    
        except:
            time.sleep(1210) 
            response = requests.get(l)
            soup = BeautifulSoup(response.text, 'html.parser')
            time.sleep(2)
            path_directory=path + str(i) +'.html'

            with open(path_directory, "w", encoding='utf-8') as file:
                file.write(str(soup))
                file.close()
            i+=1
