
#---5 Most Asked Questions During a Data Scientist Interview at Facebook---

#--NOTE: To use this code you have to have/make a Glassdoor account and sign in or the site won't let you grab it's data

##################################### -Importing Necessary Libraries- ################################################################################################

# There's a couple libraries you need to import first for this code to work.
# 1. You have to install the BeautifulSoup library. Check out the the beginning of my article here to see how to install BeautifulSoup: https://medium.com/analytics-vidhya/how-to-web-scrape-tables-online-using-python-and-beautifulsoup-36d5bafeb982
# 2. You have to install selenium and a webdriver. I created a short 4-minute video on how to do this just use this link: https://www.youtube.com/watch?v=VYHxIUnvmpQ&t=1s
# 3. Lastly you have to install the nltk library. To do this open up your anaconda prompt and type: pip install nltk

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import pandas as pd
import nltk
from nltk.stem import WordNetLemmatizer
import matplotlib.pyplot as plt
import numpy as np


##################################### -Going to Glassdoor- ##########################################################################################################

#Opens up a Chrome browser using the driver you should have downloaded from the Selenium video above, and goes to Glassdoor for Data Scientist interviews at Facebook
driver = webdriver.Chrome('C:/Web Scraping course/chromedriver.exe')
driver.get('https://www.glassdoor.ca/Interview/Facebook-Data-Scientist-Interview-Questions-EI_IE40772.0,8_KO9,23.htm')


##################################### -Going to Glassdoor- ##########################################################################################################

#--Summary: This chunk of code will go through and collect all the interview questions in each post and put them in a list

#Creates the list where the interview questions will go
questions = []

#While Loop
while True:
    #BeautifulSoup will get the HTML of the webpage on Glassdoor
    soup = BeautifulSoup(driver.page_source,'lxml')
    #Postings contain only the HTML of each posting on Glassdoor
    postings = soup.find_all('div', class_ = 'cell reviewBodyCell')
    #This loop will then go through the HTML of each posting and find the interview questions and add them to the questions list
    for post in postings:
        try:        
            q = post.find('div', class_ = 'interviewQuestions').text
            questions.append(q)
        #If a posting does not have interview questions the code will go around it
        except:
            pass
    
    #Gets the HTML of the next button that goes to the next page    
    next_page = soup.find('li', class_ = 'next')
    #From that HTML we get the url of the next page and go to it. When there's no next page to go to that is when the loop will break
    try:
        url = next_page.find('a').get('href')
    except:
        break
    full_url = 'https://www.glassdoor.com' + url
    driver.get(full_url)
    time.sleep(2)

#This adds all the questions together to be one long string
text = ''
for i in questions:
    text = text+'. ' +i


##################################### -Natural Language Processing- ##############################################################################################

#--Summary: This chunk of code will remove unnecessary words from the interview questions we scraped

#The function below performs a bit of Natural Language Processing
#What it's doing is that it's only keeping nouns, adjectives, adverbs, and verbs because were not interested in words like "the"
#It's also converting all the words to lower case becuase it's easier to deal with
#It's only keeping words with length greater then 2, and also removing words with a digit in them

def my_tokenizer(s):
    s = nltk.tag.pos_tag(s.split())
    s = [word for word, tag in s if tag == 'NN' or tag == 'JJ' or tag == 'RB' or tag == 'VB']
    s = ' '.join(s)
    s = s.lower()
    tokens = nltk.tokenize.word_tokenize(s)
    tokens = [t for t in tokens if len(t) >2]
    tokens = [t for t in tokens if not any(c.isdigit() for c in t)]
    return tokens

text1 = my_tokenizer(text)


##################################### -Word Dictionary- ##########################################################################################################

#--Summary: This chunk of code will go through the words that weren't removed in the last section and count how many times a word appears 
#           The count is documented in a dictionary with each word and how many times it appeared.          

#Createsan empty dictionary
word_index_map ={}

#This loop goes through all the words we scrpaed and did not get rid of
for word in text1:
    #If the word isn't already in the dictionary, it adds it in with a value of 1
    if word not in word_index_map:
        word_index_map[word] = 1
    #If the word is already in the dictionary is simply just adds 1 to it's count
    else:
        value = word_index_map.get(word)
        value += 1
        word_index_map[word] = value


##################################### -Questions With A Specific Word In It- #######################################################################################

#This code will return all the questions that have a specific word in it in a list.
count = []
for i in questions:
    if 'word' in i:
        count.append(i)

    

