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
from config_info import *
import requests
from goose3 import Goose
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

gn = GoogleNews(lang = 'en', country = 'IN')
nlp = spacy.load('en_core_web_lg')


# function to fetch article from google news
def get_titles(search_string,from_date,to_date):
    """ function to fetch article links from google news"""
    #print('*Fetching URLs*')
    stories=[]
    search=gn.search(search_string, from_date, to_date)
    newsitems=search['entries']
    # print(newsitems)
    for item in newsitems:
        story={
            'published': item.published,
            'title': item.title,
            'link': item.link,
            'searchcriteria': search_string,
            'source':item['source']['href']
           # 'pub':item['source']['title']
        }
        stories.append(story)
    return stories

# function to extract hot words from a text using nlp
def get_hotwords(text, top_n=10, min_length=4):
    """ function to extract hot words from a text using NLP"""
    result = []
    pos_tag = ['PROPN', 'ADJ', 'NOUN']
    doc = nlp(text.lower())
    
    # Create a list to store tokens
    tokens = [token.text for token in doc 
              if token.text not in nlp.Defaults.stop_words and 
              token.text not in punctuation and 
              token.pos_ in pos_tag and 
              len(token.text) >= min_length]
    
    # Count the frequency of each token
    token_freq = Counter(tokens)
    
    # Get the most common tokens
    most_common_tokens = token_freq.most_common(top_n)
    
    # Extract the tokens from the tuples
    result = [token for token, freq in most_common_tokens]
    
    return result



# function to fetch articles from verified links 
"""def fetch_article(df_news):
   
    article_list=[]
    for i in df_news.to_dict(orient='records'):
        try:
            url=i['link']
            source=i['source']
            pub=source.split('//')[1]
            article = Article(url)
            article.download()
            article.parse()
            authors=article.authors
            # atext=re.sub('(Also watch|Also read).*$','',article.text)
            # atext=article.text
            sleep(randint(10,60))
            atext=fetch_article_body(url)
            print(atext[:200])
            atitle=i['title']
            article.nlp()
            hotwords = set(get_hotwords(atext))
            keywords1 = ', '.join(sorted(hotwords))
            words_list = keywords1.split(',')
            selected_words = random.sample(words_list, 20)
            keywords = ','.join(selected_words)
            # keywords=article.keywords #finds significant keywords
            persons=person_tagger(atext)
            persons_cleaned=[]
            for person in persons:
                if len(nltk.word_tokenize(person))>1:
                    persons_cleaned.append(person.upper())        
            article = {'publish_date': i['published'],
                    'publisher': regexp.match(url).group(1).upper(),
                    'pub':pub,
                    'title': atitle,
                    'article': atext.replace('\n',''),
                    'persons': persons_cleaned,
                    'keywords': keywords,            
                    'link': url,
                    'source':source,
                    'searchcriteria': i['searchcriteria']
                    }
            # print(article)
            # print('-------------------------')
            article_list.append(article)
            # print(article_list)
        except Exception as e:
            pass
    # print(article_list)
    return article_list"""


# function to extract location names from a text using NLP
def locations(text):
    """ function to extract location names from text using NLP"""
    locations = []
    doc = nlp(text)
    locations.extend(ent.text for ent in doc.ents if ent.label_ in ['LOC'])
    set_location = list((locations))
    return set_location


# function to rename LEAs
def rename_leas(names):
    """ function to rename LEA's to presdefined names"""
    #print('*Renaming LEA abbreviations*')
    updated_list=[]
    for i in names:
        if i in rename_lea.keys():
            updated_list.append(rename_lea[i])
        else:
            updated_list.append(i)
    return list(set(updated_list))  


# function to identify person names from atext using NLP
def person_tagger(txt):
    """ function to extract person names from a text using NLP"""
    #print('*Tagging Persons*')
    doc=nlp(txt)
    entity=[]
    person_list=[re.sub(r'[^A-Za-z\s]+', '',entity.text.lower().replace('\n','')) for entity in doc.ents if entity.label_=='PERSON']
    person_list=set(person_list)
    return person_list


# function to remove duplicate titles using fuzzy matching 
def remove_duplicates(df_dups):
    """ function to remove duplicate titles using fuzzy matching"""
    #print('*Removing Duplicates*')
    title_list=list(set(df_dups['title'].to_list()))
    df_dups['cluster_no']=''
    c=1
    processed=[]
    for title in title_list:
        if title not in processed:
            matches=[]
            b=[i for i in title_list if i!=title and i not in processed]
            matches_list=process.extractBests(title, b ,scorer=fuzz.token_sort_ratio,score_cutoff=65)
            if len(matches_list)>=1:
                for i in matches_list:
                    matches.append(i[0])
                matches.append(title)
                #print(c, matches)
                for i in matches:
                    df_dups.loc[df_dups['title']==i,'cluster_no']=c
                c=c+1
                for i in matches:
                    processed.append(i)
            else:
                df_dups.loc[df_dups['title']==title,'cluster_no']=c
                processed.append(title)
                c=c+1
    df_dups['article_length']=df_dups['article'].apply(lambda x: len(nltk.word_tokenize(x)))
    df_dups=df_dups.sort_values(['cluster_no', 'article_length'],ascending=[True,False]).drop_duplicates(['cluster_no'], keep='first')
    df_dups=df_dups[df_dups['article_length']>40].drop(['cluster_no','article_length'],axis=1)
    return df_dups

# Function to get redirected URL using Selenium
def get_redirected_url_with_selenium(url1):
    """Function to get redirected URL"""
    # Set up Chrome options to run in headless mode (no UI)
    options = Options()
    options.headless = True

    # Initialize the WebDriver (ensure you have the appropriate driver installed)
    driver = webdriver.Chrome(options=options)

    # Open the URL
    driver.get(url1)
    
    # Wait for the page to load
    time.sleep(10)
    
    # Get the final redirected URL
    final_url = driver.current_url

    # Close the browser
    driver.quit()

    return final_url

# Function to extract article content using Goose
def extract_article_content(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    g = Goose()
    
    # Fetch the raw HTML with requests
    response = requests.get(url, headers=headers)
    
    # If request is successful (status code 200), extract content
    if response.status_code == 200:
        article = g.extract(raw_html=response.text)
        return article.cleaned_text
    else:
        return f"Error: {response.status_code}"
    

def get_keywords_from_article(article, num_keywords=5):
    # Initialize TfidfVectorizer (remove common stop words)
    vectorizer = TfidfVectorizer(stop_words='english', max_features=num_keywords)
    
    # Fit and transform the article
    tfidf_matrix = vectorizer.fit_transform([article])
    
    # Get the words (terms) corresponding to the features
    feature_names = np.array(vectorizer.get_feature_names_out())
    
    # Get the sorted scores (importance) for each word
    sorted_indices = np.argsort(tfidf_matrix.toarray()).flatten()[::-1]
    
    # Get the top 'num_keywords' important words
    keywords = feature_names[sorted_indices][:num_keywords]
    
    # Join the keywords into a string, separated by commas
    return ', '.join(keywords)



