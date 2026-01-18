from News_Scrapper.functions import *
import pandas as pd
from pygooglenews import GoogleNews
import pandas as pd
pd.set_option('display.max_colwidth', None)
from newspaper import Article
import nltk
import time
from tqdm import tqdm
from urllib.parse import urlparse, parse_qs
from datetime import datetime,date
from fuzzywuzzy import fuzz,process
from random import randint
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import json
from bs4 import BeautifulSoup
import spacy
import re
from string import punctuation
from collections import Counter
import warnings
import tqdm
warnings.filterwarnings("ignore")
import datetime
from dateutil import parser
from datetime import datetime as dt
from datetime import timedelta as td
from random import randint
from time import sleep
import random
import News_Scrapper.config_info as info
from goose3 import Goose
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
nltk.download('punkt_tab')

#importing config
name = info.month_for_scraping
from_ = info.start_date
to_ = info.end_date
crime_list = info.crime_list
lea_regex = info.lea_regex
rename_lea = info.rename_lea
news_providers = info.news_providers
rss_dict = info.rss_dict
date_dict={'name': [name],'from_':[from_],'to_':[to_],'status':[''],'completed_on':['']}
date_range=pd.DataFrame.from_dict(date_dict)

gn = GoogleNews(lang = 'en', country = 'IN')
nlp = spacy.load('en_core_web_lg')




# function to fetch news feed 
def fetch_news_feed(date_range, from_, to_, rss_dict):
    """ function to fetch RSS Feed from google news for topics defined in rss_dict"""
    for month_row in date_range.to_dict(orient='records'):
        if month_row['status'] != 'Done':
            print('Fetching News for Month:', month_row['name'])
            
            from_ = pd.to_datetime(from_).strftime('%Y-%m-%d')
            to_ = pd.to_datetime(to_).strftime('%Y-%m-%d')
            
            print(f"Fetching news from {from_} to {to_}")
            
            df_news = pd.DataFrame()
            
            # Fetching news for each topic
            for topic in tqdm.tqdm(rss_dict):
                delay = round(random.randint(180, 360), 2)
                print(f"Sleeping for {round(delay/60, 1)} minutes")
                time.sleep(delay / 60)  # Sleep for random delay in minutes
                
                try:
                    # Try fetching news data and ensure dates are passed in the correct format
                    print(from_)
                    print(to_)
                    print(topic)
                    news_data = get_titles(topic, from_, to_)
                    df_news = pd.concat([df_news, pd.DataFrame.from_records(news_data)], ignore_index=True)
                except Exception as e:
                    print(f"Error fetching news for {topic} from  {from_} to {to_}: {e}")
    print(f"{df_news.shape[0]} records Fetched")
    return df_news
    
def get_updated_url(df):
    """ function to get updated url for rss feed"""
    # Loop through the DataFrame using iterrows to get both index and row
    for idx, row in df.iterrows():
        url1 = row['link']
        try:
            # Get the redirected URL
            updated_url = get_redirected_url_with_selenium(url1)
            
            # Update the 'updated_link' column for the current row
            df.at[idx, 'updated_link'] = updated_url
            

            
        except Exception as e:
            print(f"Error with URL {url1}: {e}")
            df.at[idx, 'updated_link'] = None  # If there's an error, store None

    return df

def article_content(df):
    """ function to fech article content from verified urls"""
    # Loop through each URL in the 'updated_link' column and extract content
    for idx, row in df.iterrows():
        url = row['updated_link']
        try:
            # Extract article content
            article_content = extract_article_content(url)
            df.at[idx, 'article_content'] = article_content  # Add content to the DataFrame
        except Exception as e:
            print(f"Error processing {url}: {e}")
            df.at[idx, 'article_content'] = None  # If an error occurs, add None for the content

    return df

def extract_article_keywords(df_check):
    # Loop through each row and generate keywords for the 'Article' column
    for idx, row in df_check.iterrows():
        article = row['article']
        
        # Ensure the article is not NaN before processing
        if isinstance(article, str):
            keywords = get_keywords_from_article(article, num_keywords=5)
            df_check.at[idx, 'Keywords'] = keywords
        else:
            df_check.at[idx, 'Keywords'] = None
    return df_check



    
if __name__=='__main__':

    print("fetching news feed")
    df = fetch_news_feed(date_range, from_, to_, rss_dict)
    df.to_csv(f'./processing/feed_{name}.csv')
    df = pd.read_csv(f'./processing/feed_{name}.csv')

    df2 = get_updated_url(df)
    # Final save after all iterations are done (if not done in real-time in loop)
    df2.to_csv(f'./processing/updated_feed_{name}.csv', index=False)

    df2 = pd.read_csv("./processing/updated_feed_April_May_2025.csv")
    df3 = article_content(df2)
    df3.to_csv(f'./processing/updated_content_feed_{name}.csv', index=False)
    print("Done Fetching Article Content!!")

    df_news=pd.read_csv(f'./processing/updated_content_feed_{name}.csv')
    df_news = df_news.dropna(subset=['article_content'])
    df_news.rename(columns={'article_content': 'article'}, inplace=True)
    df_news=remove_duplicates(df_news)
    df_final = df_news.copy()


    regexp_quantum=re.compile('((?: Rs|₹|\$)(?:.| )?[0-9]+[0-9.,]*[a-z]?(?: |-)(?:lacs|crores|million|lakh|billion|crore|cr)? ?(?:rupees|rupee|dollars|dollar)?)',re.IGNORECASE)
    df_final['quantum']=df_final['article'].apply(lambda x: regexp_quantum.findall(str(x),re.IGNORECASE))+df_final['title'].apply(lambda x: regexp_quantum.findall(str(x),re.IGNORECASE))
    df_final['quantum']=df_final['quantum'].apply(lambda x: list(set([i.replace('₹','Rs ').replace('-','').strip() for i in x ])))
    df_final['lea']=df_final['article'].apply(lambda x: list(set([i.group().replace('(','').replace(')','').strip() for i in re.finditer(lea_regex, str(x).upper())])))
    df_final['lea']=df_final['lea'].apply(rename_leas)
    df_final.dropna(subset=['article'],inplace=True)
    df_final.dropna(subset=['title'],inplace=True)
    df_final.drop_duplicates(subset=['title'],inplace=True)
    df_final=df_final[df_final['title'].apply(lambda x: len(str(x).split()))>4]
    df_final=df_final[df_final['article'].apply(lambda x: len(str(x).split()))>45]
    df_final=df_final[~df_final['title'].str.contains('^Nia |(.| )?Nia |^Ed |(.| )?Ed |^ed-|(.| )?ed-')]
    df_final=df_final[~df_final['article'].str.contains('^Nia |(.| )?Nia |^Ed |(.| )?Ed |^ed-|(.| )?ed-')]
    df_final['crimes']=df_final['article'].apply(lambda x: [crime for crime in crime_list if crime in x.lower()])+df_final['title'].apply(lambda x: [crime for crime in crime_list if crime in x.lower()])
    df_final['crimes']=df_final['crimes'].apply(lambda x: list(set(x)))
    df_final['person']=df_final['article'].apply(person_tagger)

    df_final['locations'] = df_final['article'].apply(locations)

    df_final = extract_article_keywords(df_final)
    df_final.to_csv(f'./output/final_adverse_media_{name}.csv')
    print(f"Done final output saved at ./output/final_adverse_media_{name}.csv !!")




    


    
                













