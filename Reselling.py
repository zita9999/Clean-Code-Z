
#--Code from my Medium article: How to Make Money on the Side Reselling the Smart Way Using Code

#check it out here: 

##################################### -PLS READ- ################################################################################################
'''

 - This is a summary of what the code does below:

        The code below will go to Hudsons bay sales page, and scrape product details for the first 30 pages.
        It will put all this data into a dataframe than return the product with the largest % discount.
        The code will then go to Amazon.com and search up said product scraping the prices of all the products that were returned.
        The average price of all these products will then be calculated

 - This code is created in Python so to use it for yourself, go to any Python application and copy and paste this entire code.
 
 - If you want to learn how to create this code for yourself you can take my course in web scraping to learn how. Here's the link: https://www.udemy.com/course/web-scraping-in-python-with-beautifulsoup-and-selenium/?referralCode=939EB64B8E029FCBBDEB

'''

##################################### -Notes- ################################################################################################
'''

 - There's a couple libraries you need to install first for this code to work.
 - 1. You have to install the BeautifulSoup library. I created a short 3-minute video on how to do this just use this link: https://www.youtube.com/watch?v=tv05NzizNtE&t=0s
 - 2. You have to install selenium and a webdriver. I created a short 4-minute video on how to do this just use this link: https://www.youtube.com/watch?v=VYHxIUnvmpQ&t=1s
 - 3. When you have Selenium and the webdriver downloaded. Go to line 51 and paste the file path to your webdriver there.

'''

##################################### -Importing Necessary Libraries- ################################################################################################


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from numpy import random


##################################### -Goes to Hudsons Bay Website- ##########################################################################################################

#--Summary: This chunk of code will go to Hudsons Bay sales page and collect the product details of thousands of products

driver = webdriver.Chrome('C:/Paste Path Here/chromedriver.exe')
driver.get('https://www.thebay.com/c/sale-1?start=384&sz=24')

#Creates an empty dataframe where the product information will go
df = pd.DataFrame({'Link':[''], 'Name':[''], 'Full Price':[''], 'Sale Price':['']})

counter = 93
#This for loop will go through the first 30 pages of products. You can cgange it by changing the 30 number below
for i in range(1,30):
    #loops through the different sales pages on thebay.com
    driver.get('https://www.thebay.com/c/home/clearance1?start='+str(counter)+'&sz=24')

    #BeautifulSoup will get the HTML of the webpage on 
    soup = BeautifulSoup(driver.page_source, 'lxml')
    #Postings contain only the HTML of each product posting on the Hudsons bay page
    postings = soup.find_all('div', class_ = 'col-6 col-sm-4 col-xl-3')
    
    #This loop will then go through the HTML of each product posting and find the link, name, full price, rating, and sale price for each product
    for post in postings:
        try:
            link = post.find('a').get('href')
            link_full = 'https://www.thebay.com'+link
            name = post.find('a', class_ ='link').text
            full_price = post.find('span', class_ = 'formatted_price bfx-price bfx-list-price').get('data-unformatted-price')
            sale = post.find('span', class_ ='formatted_sale_price formatted_price js-final-sale-price bfx-price bfx-sale-price').get('data-unformatted-price')
            df = df.append({'Link':link_full, 'Name':name, 'Full Price':full_price, 'Sale Price':sale}, ignore_index = True)
        except:
            pass    
    counter = counter +96

#The code below just touches up the dataframe and cleans it a bit
df2 = df.loc[1:,:]
df2['Full Price'] = df2['Full Price'].apply(float)
df2['Sale Price'] = df2['Sale Price'].apply(float)
df2['Discount'] = ((df2['Full Price'] - df2['Sale Price'])/df2['Full Price'])*100
df2 = df2.sort_values(by = ['Discount'], ascending = False)
df2.reset_index(inplace = True)

#This variable gets the product with the largest % discount
product = df2.loc[0, 'Name']


##################################### -Search Box- ##########################################################################################################

#--Summary: This chunk of code will find the search box on the amazon home page and input the the product with the largest discount

driver.get('https://www.amazon.com/')
input_box = driver.find_element_by_xpath('/html/body/div[1]/header/div/div[1]/div[2]/div/form/div[2]/div[1]/input')
input_box.send_keys(product)
input_box.send_keys(Keys.ENTER)
time.sleep(2)


##################################### -Scraping of Products- ##########################################################################################################

#--Summary: The code below will go through each product posting and save the link, name, price, rating, and number of ratings for each product in a dataframe

#Creates an empty dataframe where the product information will go
df = pd.DataFrame({'Link':[''],'Name':[''], 'Price':[''], 'Rating':[''],'# of Ratings':['']})

while True:
    #BeautifulSoup will get the HTML of the webpage on Amazon
    soup = BeautifulSoup(driver.page_source, 'lxml')
    #Postings contain only the HTML of each product posting on the Amazon page
    postings = soup.find_all('div',{'data-component-type':'s-search-result'})

    #This loop will then go through the HTML of each posting and find the link, name, price, rating, and number of ratings for each product
    for post in postings:
        try:
            link = post.find('a', class_ = 'a-link-normal s-no-outline').get('href')
            link_full = 'https://www.amazon.ca'+ link
            try:
                name = post.find('span', class_ = 'a-size-medium a-color-base a-text-normal').text
            except:
                name = post.find('span', class_ = 'a-size-base-plus a-color-base a-text-normal').text
            rating = post.find('span', class_ = 'a-icon-alt').text
            price = post.find('span', class_ = 'a-offscreen').text
            num_rating = post.find('span', class_ ='a-size-base').text
            #The link, name, price, rating, and number of ratings for each product is added to our dataframe 
            df = df.append({'Link':link_full,'Name':name, 'Price':price, 'Rating':rating, '# of Ratings':num_rating,
                            }, ignore_index = True)
        #If a product does not have any of the above the code will go around it
        except:
            pass
    #This chunck of code will loop through all the pages on Amazon until there are no more pages left with products
    li = soup.find('li', class_ = 'a-last')
    try:
        next_page = li.find('a').get('href')
    except:
        break
    next_page_full = 'https://www.amazon.com'+next_page
    url = next_page_full
    driver.get(url)
    time.sleep(2)


##################################### -Cleaning the Dataframe- ##########################################################################################################

#--Summary: The code below just touches up the dataframe and cleans it a bit

df = df.iloc[1:,:]
def comma(x):
    return x.replace(',','')
df['# of Ratings'] = df['# of Ratings'].apply(comma)
df['Price'] = df['Price'].apply(comma)

def integer(x):
    try:
        num = int(x)
        return num
    except:
        return 0       
df['# of Ratings'] = df['# of Ratings'].apply(integer)
   
def dollar_sign(x):
    try:
        x = x[1:]
        return float(x)
    except:
        pass
df['Price'] = df['Price'].apply(dollar_sign)

df = df[df['# of Ratings'] > 20]
           
#This will output the average price/market price for the product searched
df['Price'].mean()



