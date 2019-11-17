# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 16:38:23 2019

@author: HP
"""
import pandas as pd
import csv
from bs4 import BeautifulSoup
import requests
import time

#This function, for each link, take title, and the frist 2 section and write a tsv file for each wiki page
def parse_page(path):
    time = 0
    while time <=30000:
        try:
            with open(path+ str(time) +'.html', "r", encoding='utf-8') as file:
                articolo=file.read()
            soup = BeautifulSoup(articolo,'html.parser')
            
            
            title=soup.find_all('title')        
            title = title[0].get_text()
            title = title.split('-')
            title = str(title[0])
            mydiv = soup.find_all("div", class_="mw-parser-output")
            mydiv=mydiv[0] 
            par_and_head=mydiv.find_all(["p", "h2","h3","h4","h5","h6"])
            headings_list = ['h2','h3','h4','h5','h6']
            intro = ''
            plot = ''
            for i in range(len(par_and_head)):
                if par_and_head[i].name=='p':
                    intro += par_and_head[i].get_text()
                if par_and_head[i].name in headings_list and intro != '':
                    variabile = i
                    break   
            while variabile < len(par_and_head):
                if par_and_head[variabile].name == 'p':
                    plot += par_and_head[variabile].get_text()
                elif par_and_head[variabile].name in headings_list and plot != '':
                    break
                variabile+=1
            
               
            table=soup.find('table',{'class':'infobox vevent'})
            article_table_dataframe = pd.read_html(str(table))
            article_table_dataframe=article_table_dataframe[0]
            article_table_dataframe.columns = ['Category','info']
    
            for i in range(len(article_table_dataframe)):
                for j in range(len(article_table_dataframe['info'][i])):
                    if j!= 0:
                        if article_table_dataframe['info'][i][j].isupper() and article_table_dataframe['info'][i][j-1].islower():
                           article_table_dataframe['info'][i]= article_table_dataframe['info'][i][:j]+' '+article_table_dataframe['info'][i][j:]
            data_category = ['Title','Intro','Plot']
            data_to_merge1 = pd.DataFrame(data_category)
            data_tip = [title,intro,plot]
            data_to_merge2 = pd.DataFrame(data_tip)
            data_tip_merged=pd.merge(data_to_merge1, data_to_merge2, left_index=True, right_index=True) 
            data_tip_merged.columns = ['Category', 'info']
            film_info = pd.concat([article_table_dataframe, data_tip_merged], ignore_index=True)
            film_info=film_info.dropna(how='all')
            film_info=film_info.reset_index(drop=True)
            data_info_names=['Title','Intro','Plot', 'Directed by', 'Produced by', 'Written By', 'Starring', 'Music by', 'Release date', 'Running time', 'Country', 'Language', 'Budget']
            dataframe_info_names=pd.DataFrame(data_info_names)
            dataframe_info_names.columns=['Category']
            final_film_dataframe=pd.merge(dataframe_info_names, film_info, on='Category',how='left')
            with open(path+ str(time)+'.tsv', 'wt',encoding='utf-8') as out_file:
                tsv_writer = csv.writer(out_file, delimiter='\t')
               
                tsv_writer.writerow(final_film_dataframe['Category'])   
                tsv_writer.writerow(final_film_dataframe['info'])
            time+=1
        except:
            
            
            with open(path+ str(time) +'.html', "r", encoding='utf-8') as file:
                articolo=file.read()
            soup = BeautifulSoup(articolo,'html.parser')
            title=soup.find_all('title')        
            
            title = title[0].get_text()
            title = title.split('-')
            title = str(title[0])
            mydiv = soup.find_all("div", class_="mw-parser-output")
            if len(mydiv)!=0:
                mydiv=mydiv[0] 
                par_and_head=mydiv.find_all(["p", "h2","h3","h4","h5","h6"])
                headings_list = ['h2','h3','h4','h5','h6']
                intro = ''
                plot = ''
                for i in range(len(par_and_head)):
                    if par_and_head[i].name=='p':
                        intro += par_and_head[i].get_text()
                    if par_and_head[i].name in headings_list and intro != '':
                        variabile = i
                        break   
                while variabile < len(par_and_head):
                    if par_and_head[variabile].name == 'p':
                        plot += par_and_head[variabile].get_text()
                    elif par_and_head[variabile].name in headings_list and plot != '':
                        break
                    variabile+=1
                data_category = ['Title','Intro','Plot']
                data_to_merge1 = pd.DataFrame(data_category)
                data_tip = [title,intro,plot]
                data_to_merge2 = pd.DataFrame(data_tip)
                data_tip_merged=pd.merge(data_to_merge1, data_to_merge2, left_index=True, right_index=True) 
                data_tip_merged.columns = ['Category', 'info']
                data_tip_merged=data_tip_merged.dropna(how='all')
                data_tip_merged=data_tip_merged.reset_index(drop=True)
                with open(r'C:\Users\HP\Desktop\file hw3\wiki\article_'+str(time)+'.tsv', 'wt',encoding='utf-8') as out_file:
                    tsv_writer = csv.writer(out_file, delimiter='\t')
                    tsv_writer.writerow(data_tip_merged['Category'])
                    #aggiungere row con informazioni generiche   
                    tsv_writer.writerow(data_tip_merged['info'])
                time+=1
            else:
                data_category = ['Title','Intro','Plot']
                data_to_merge1 = pd.DataFrame(data_category)
                data_tip = [title]
                data_to_merge2 = pd.DataFrame(data_tip)
                data_tip_merged=pd.merge(data_to_merge1, data_to_merge2, left_index=True, right_index=True) 
                data_tip_merged.columns = ['Category', 'info']
                data_tip_merged=data_tip_merged.dropna(how='all')
                data_tip_merged=data_tip_merged.reset_index(drop=True)
                with open(path+str(time)+'.tsv', 'wt',encoding='utf-8') as out_file:
                    
                    tsv_writer = csv.writer(out_file, delimiter='\t')
                   
                    tsv_writer.writerow(data_tip_merged['Category'])   
                    tsv_writer.writerow(data_tip_merged['info'])
                time+=1