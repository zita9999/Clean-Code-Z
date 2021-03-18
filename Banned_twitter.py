

##################################### -PLS READ- ################################################################################################

'''

The code you see below is from my article "I Got Banned From Every Social Media App On Purpose".

The code will login into my Twitter account, navigate Twitter until it finds a trending hashtag.

The code will then keep tweeting until the account gets suspended or banned.

If you want to learn the code below and how to do cool projects like this one for yourself,
you can take my course in Web Scraping where by the end, you will understand what every line
below does.

Here's the link to it: https://www.udemy.com/course/web-scraping-in-python-with-beautifulsoup-and-selenium/?referralCode=939EB64B8E029FCBBDEB
    
The course is only $15, if you go to the link and it says anything above $100, that's just Udemy's
business model, just wait like 2 days and that price will reduce to around $10-$15.

'''


##################################### -Importing Necessary Libraries- ################################################################################################


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time


##################################### -Getting banned from Twitter- ################################################################################################


#Opens up a browser and goes to twitter login page
driver = webdriver.Chrome(
        'C:/Web Scraping course/chromedriver.exe')

driver.get('https://twitter.com/login')
time.sleep(2)

#inputs an email and password for the login details
login = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[1]/label/div/div[2]/div/input')
login.send_keys('#########')
password = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[2]/label/div/div[2]/div/input')
password.send_keys('########')
password.send_keys(Keys.ENTER)

#This code will go to a trending topic and keep posting "I LOVE WATERMELON SUGAR"
for i in range(100,200):
    driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/a/div[2]/div/div').click()
    text = driver.find_element_by_xpath('//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[3]/div/div/div/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div/div')
    text.send_keys(' I LOVE WATERMELON SUGAR!!!' +str(i)+'')
    driver.find_element_by_xpath('//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[3]/div/div/div/div[1]/div/div/div/div/div[2]/div[4]/div/div/div[2]/div[4]/div').click()
      
#This code follows a bunch of people
for i in range(1, 100):
    try:
        follow = driver.find_element_by_xpath('//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div/section/div/div/div['+str(i)+']/div/div/div/div[2]/div/div[2]').text
        if follow == 'Follow':    
            driver.find_element_by_xpath('//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div/section/div/div/div['+str(i)+']/div/div/div/div[2]/div/div[2]').click()
    except:
        pass
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


