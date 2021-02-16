##################################### -PLS READ- ################################################################################################
'''
   
 - I created a Youtube video that shows you exactly how to use this bot. I recommend you watch it by going to this link: https://youtu.be/GHt5y6IgJ0I

 - This bot is created in Python so to use it for yourself, go to any Python application and copy and paste this entire code.
 
 - - If you want to learn how to create these type of bots for yourself you can take my course in web scraping to learn how. Here's the link: https://www.udemy.com/course/web-scraping-in-python-with-beautifulsoup-and-selenium/?referralCode=939EB64B8E029FCBBDEB

'''

##################################### -Notes- ################################################################################################
'''

 - There's a couple libraries you need to install first for this code to work.
 - 1. You have to install the BeautifulSoup library. I created a short 3-minute video on how to do this just use this link: https://www.youtube.com/watch?v=tv05NzizNtE&t=0s
 - 2. You have to install selenium and a webdriver. I created a short 4-minute video on how to do this just use this link: https://www.youtube.com/watch?v=VYHxIUnvmpQ&t=1s
 - 3. When you have Selenium and the webdriver downloaded. Go to line 34 and paste the file path to your webdriver there.

'''

##################################### -Importing Necessary Libraries- ################################################################################################

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium.webdriver.common.keys import Keys


##################################### -Goes to Nike.com- ##########################################################################################################

#--Summary: Opens up a Chrome browser using the driver you should have downloaded from the Selenium video above, and goes to Nike.com

driver = webdriver.Chrome(
        'C:/Paste Path Here/chromedriver.exe')

driver.get('https://www.nike.com/ca/w/sale-3yaep')


##################################### -Scrolls Down the Webpage- ##########################################################################################################

#--Summary: The code below will keep scrolling down the page loading in hundreds of products, so they can be scraped

#Will keep scrolling down the webpage until it cannot scroll no more
last_height = driver.execute_script('return document.body.scrollHeight')
while True:
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(3)
    new_height = driver.execute_script('return document.body.scrollHeight')
    if new_height == last_height:
        break
    last_height = new_height


##################################### -Scraping the Products- ##########################################################################################################

#--Summary: The code below will go through each product posting and save the link, name, subtitle, full price, and sale price for each product in a dataframe
 
#BeautifulSoup will get the HTML of the webpage on Nike 
soup = BeautifulSoup(driver.page_source, 'lxml')

#Grabs the HTML of each product
product_card = soup.find_all('div', class_ = 'product-card__body')

#Creates an empty dataframe where the product information will go
df = pd.DataFrame({'Link':[''], 'Name':[''], 'Subtitle':[''], 'Price':[''], 'Sale Price':['']})

#This loop will then go through the HTML of each posting and find the link, name, subtitle, full price, and sale price for each product
for product in product_card:
    try:
        link = product.find('a', class_ = 'product-card__link-overlay').get('href')
        name = product.find('div', class_ = 'product-card__title').text
        subtitle = product.find('div', class_ = 'product-card__subtitle').text
        full_price = product.find('div', class_ = 'product-price css-1h0t5hy').text
        sale_price = product.find('div', class_ = 'product-price is--current-price css-s56yt7').text
        #The link, name, subtitle, full price, and sale price for each product is added to our dataframe 
        df = df.append({'Link':link, 'Name':name, 'Subtitle':subtitle, 'Price':full_price, 'Sale Price':sale_price},
                       ignore_index = True)
    except:
        pass


##################################### -Cleaning the Dataframe- ##########################################################################################################

#--Summary: The code below just touches up the dataframe and cleans it a bit

df = df.iloc[1:,:]
def dollar_sign(x):
    try:
        x = x[1:]
        return float(x)
    except:
        pass
df['Price'] = df['Price'].apply(dollar_sign)
df['Sale Price'] = df['Sale Price'].apply(dollar_sign)
df['Discount Percentage'] = (((df['Price'] - df['Sale Price'])/df['Price'])*100).round(2)


##################################### -Final Result- ##########################################################################################################

#Displays the final dataframe
print(df)

#To get a clearer view of this table, the code below will export it as an excel file, you just have to input the file location you want it saved
#df.to_csv('A/File/Path/amazon_table.csv')




