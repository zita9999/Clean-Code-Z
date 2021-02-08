##################################### -PLS READ- ################################################################################################
'''
   
 - I created a Youtube video that shows you exactly how to use this bot. I recommend you watch it by going to this link: https://youtu.be/V2u8asYjFcE

 - This bot is created in Python so to use it for yourself go to any Python application and copy and paste this entire code.

'''

##################################### -User Input- ################################################################################################

#Input the URL between the commas of the location you want to look for. You need to input a city.
url = ''


##################################### -Notes- ################################################################################################
'''

 - There's a couple libraries you need to install first for this code to work.
 - 1. You have to install the BeautifulSoup library. I created a short 3-minute video on how to do this just use this link: https://www.youtube.com/watch?v=tv05NzizNtE&t=0s
 - 2. You have to install Selenium and a webdriver. I created a short 4-minute video on how to do this just use this link: https://www.youtube.com/watch?v=VYHxIUnvmpQ&t=1s
 - 3. When you have Selenium and the webdriver downloaded. Go to line 40 and paste the file path to your webdriver there.
 
'''


##################################### -Importing Necessary Libraries- ################################################################################################

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time


##################################### -Goes to the URL you input above- ##########################################################################################################

#--Summary: Opens up a Chrome browser using the driver you should have downloaded from the Selenium video above, and goes to Airbnb.com

driver = webdriver.Chrome(
        'C:/Paste Path Here/chromedriver.exe')
driver.get(url)


##################################### -Scraping the Postings- ################################################################################################

#--Summary: The code below will go through each posting and save the link, title, price, rating, and details for each listing in a dataframe

#Creates an empty dataframe where the posting information will go
df = pd.DataFrame({'Links':[''], 'Title':[''], 'Details':[''],'Price':[''],'Rating':['']})

#This loop goes through every page and grabs all the details of each posting
#Loop will only end when there are no more pages to go through
while True:
    
    #BeautifulSoup will get the HTML of the webpage on Airbnb
    soup = BeautifulSoup(driver.page_source, 'lxml')
    #Gets the HTML of all the postings on the page
    postings = soup.find_all('div', class_ ='_8ssblpx')
    len(postings)
    
    #This loop will then go through the HTML of each posting and find the link, title, price, rating, and details for each posting
    for post in postings:
        try:
            link = post.find('a', class_ = '_gjfol0').get('href')
            link_full = 'https://www.airbnb.ca' + link
            title = post.find('a', class_ = '_gjfol0').get('aria-label')
            price = post.find('span', class_ = '_krjbj').text
            try:
                rating = post.find('span',class_ = '_10fy1f8').text
            except:
                rating = 'N/A'
            try:
                details = post.find_all('div', class_ = '_kqh46o')[0].text
            except:
                details = 'N/A'
            #The link, title, price, rating, and details for each product is added to our dataframe 
            df = df.append({'Links':link_full, 'Title':title, 'Details':details,
                            'Price':price,'Rating':rating}, ignore_index = True)
        #If a product does not have any of the above the code will go around it
        except:
            pass
    
    #This chunck of code will find the next button link and go to the next page on Airbnb
    try:
        next_page = soup.find('a', {'aria-label':'Next'}).get('href')
    except:
        break
    next_page_full = 'https://www.airbnb.com'+next_page
    url = next_page_full
    driver.get(url)


##################################### -Cleaning the Dataframe- ##########################################################################################################

#--Summary: The code below just touches up the dataframe and cleans it a bit

df = df.iloc[1:,:]

def guests(x):
    x = x.split('·')[0]
    return (x.split(' ')[0])

def bedroom(x):
    x = x.split('·')[1]
    return (x.split(' ')[1])

def beds(x):
    x = x.split('·')[2]
    return (x.split(' ')[1])

def baths(x):
    try:
        x = x.split('·')[3]
        return (x.split(' ')[1])
    except:
        return ''

df['Guests'] = df['Details'].apply(guests)
df['Bedrooms'] = df['Details'].apply(bedroom)
df['Beds'] = df['Details'].apply(beds)
df['Baths'] = df['Details'].apply(baths)

df = df[['Links', 'Title', 'Guests', 'Bedrooms', 'Beds', 'Baths', 'Price', 'Rating']]
 

##################################### -Final Result- ##########################################################################################################

#Displays the final dataframe
print(df)

#To get a clearer view of this table, the code below will export it as an excel file, you just have to input the file location you want it saved
#df.to_csv('A/File/Path/amazon_table.csv')



