##################################### -PLS READ- ################################################################################################
'''
   
 - I created a Youtube video that shows you exactly how to use this bot. I recommend you watch it by going to this link: https://youtu.be/v-Y1Eox3nf4

 - This bot is created in Python so to use it for yourself, go to any Python application and copy and paste this entire code.
 
 - If you want to learn how to create these type of bots for yourself you can take my course in web scraping to learn how. Here's the link: https://www.udemy.com/course/web-scraping-in-python-with-beautifulsoup-and-selenium/?referralCode=939EB64B8E029FCBBDEB

'''

##################################### -User Input- ################################################################################################

#Input the URL between the commas of the body type of car you picked.
url = ''


##################################### -Notes- ################################################################################################
'''

 - There's a couple libraries you need to install first for this code to work.
 - 1. You have to install the BeautifulSoup library. I created a short 3-minute video on how to do this just use this link: https://www.youtube.com/watch?v=tv05NzizNtE&t=0s

'''

##################################### -Importing Necessary Libraries- ################################################################################################

import requests
from bs4 import BeautifulSoup
import pandas as pd


##################################### -Gets the HTML from Carpages- ##########################################################################################################

#--Summary: The code below copies the HTML from Carpages into Python

#Imports the HTML into python
page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')


##################################### -Scraping the Car Postings- ##########################################################################################################

#--Summary: The code below will go through each car posting and save the link, name, price, and color for each car in a dataframe

#Creates an empty dataframe where the car information will go
df = pd.DataFrame({'Link':[''], 'Name':[''], 'Price':[''],'Distance':[''], 'Color':['']})
counter = 0

while counter <= 10:    
    #Gets the HTML of all the postings on the page
    postings = soup.find_all('div', class_ = 'media soft push-none rule')

    #This loop will then go through the HTML of each car posting and find the link, name, price, and color for each car
    for post in postings:
        link = post.find('a', class_ = 'media__img media__img--thumb').get('href')
        link_full = 'https://www.carpages.ca' +link
        name = post.find('h4', class_ = 'hN').text.strip()
        price = post.find('strong', class_ = 'delta').text.strip()
        distance = post.find_all('div', class_='grey l-column l-column--small-6 l-column--medium-4')[0].text
        color = post.find_all('div', class_ = 'grey l-column l-column--small-6 l-column--medium-4')[1].text.strip()
        #The link, name, price, and color for each car and is added to our dataframe 
        df = df.append({'Link':link_full, 'Name':name, 'Price':price,'Distance':distance, 'Color':color}, ignore_index = True)
    
    #This chunck of code will loop through all the pages on Carpages until there are no more pages left with car postings
    try:
        next_page = soup.find_all('a', class_ = 'nextprev')[1].get('href')
    except:
        next_page = soup.find('a', class_ = 'nextprev').get('href')
    page = requests.get(next_page)
    soup = BeautifulSoup(page.text, 'lxml')
    counter +=1


##################################### -Cleaning the Dataframe- ##########################################################################################################

#--Summary: The code below just touches up the dataframe and cleans it a bit

df = df.iloc[1:,:]


##################################### -Final Result- ##########################################################################################################

#Displays the final dataframe
print(df)

#To get a clearer view of this table, the code below will export it as an excel file, you just have to input the file location you want it saved
#df.to_csv('A/File/Path/amazon_table.csv')



