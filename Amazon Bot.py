##################################### -PLS READ- ################################################################################################
'''
   
 - I created a Youtube video that shows you exactly how to use this bot. I recommend you watch it by going to this link: https://youtu.be/k4uWLu1XkwQ

 - This bot is created in Python so to use it for yourself, go to any Python application and copy and paste this entire code.
 
 - - If you want to learn how to create these type of bots for yourself you can take my course in web scraping to learn how. Here's the link: https://www.udemy.com/course/web-scraping-in-python-with-beautifulsoup-and-selenium/?referralCode=939EB64B8E029FCBBDEB

'''

##################################### -User Input- ################################################################################################

#Input the product you want to search for in between the commans belows
product = ''


##################################### -Notes- ################################################################################################
'''

 - There's a couple libraries you need to install first for this code to work.
 - 1. You have to install the BeautifulSoup library. I created a short 3-minute video on how to do this just use this link: https://www.youtube.com/watch?v=tv05NzizNtE&t=0s
 - 2. You have to install selenium and a webdriver. I created a short 4-minute video on how to do this just use this link: https://www.youtube.com/watch?v=VYHxIUnvmpQ&t=1s
 - 3. When you have Selenium and the webdriver downloaded. Go to line 40 and paste the file path to your webdriver there.

'''

##################################### -Importing Necessary Libraries- ################################################################################################

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium.webdriver.common.keys import Keys


##################################### -Goes to Amazon.com- ##########################################################################################################

#--Summary: Opens up a Chrome browser using the driver you should have downloaded from the Selenium video above, and goes to Amazon.com

driver = webdriver.Chrome(
        'C:/Paste Path Here/chromedriver.exe')

driver.get('https://www.amazon.com/')


##################################### -Search Box- ##########################################################################################################

#--Summary: This chunk of code will find the search box on the amazon home page and input the the product you specified above

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


##################################### -Final Result- ##########################################################################################################

#Displays the final dataframe with all the product information from every product that amazon had for the product you input above
print(df)

#To get a clearer view of this table, the code below will export it as an excel file, you just have to input the file location you want ti saved
#df.to_csv('A/File/Path/amazon_table.csv')

















