

##################################### -PLS READ- ################################################################################################

'''

The code you see below is from my article "I Got Banned From Every Social Media App On Purpose".

The code will login into my Instagram account, navigate Instagram and find a post to click on.

When it goes to the post it will click on who liked the post and keep following those accounts
until its gets suspended or banned.

The code will then go to each of these profiles and send a connection to them until the account gets
suspended or banned.

If you want to learn the code below and how to do cool projects like this one for yourself,
you can take my course in Web Scraping where by the end, you will understand what every line
below does.

Here's the link to it: https://www.udemy.com/course/web-scraping-in-python-with-beautifulsoup-and-selenium/?referralCode=939EB64B8E029FCBBDEB
    
The course is only $15, if you go to the link and it says anything above $100, that's just Udemy's
business model, just wait like 2 days and that price will reduce to around $10-$15.

'''


##################################### -Importing Necessary Libraries- ################################################################################################


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time


##################################### -Getting banned from Instagram- ################################################################################################


#This chunk of code loads up the instagram website
mobile_emulation = { "deviceName": "Apple iPhone 6" }
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
driver = webdriver.Chrome('C:/Web Scraping course/chromedriver.exe')
driver.get('https://www.instagram.com/')
time.sleep(3)

#This code will input my login details to enter my account
login = driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input')
login.send_keys('#######')
password = driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input')
password.send_keys('######')
password.send_keys(Keys.ENTER)
driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div/div/button').click()


#This code will go to a post and keep following people until the account gets banned or suspended
while True:
    for i in range(1, 10):
        try:           
            follow = driver.find_element_by_xpath('/html/body/div[6]/div/div/div[2]/div/div/div['+str(i)+']/div[3]/button').text           
            if follow == 'Follow':
                driver.find_element_by_xpath('/html/body/div[6]/div/div/div[2]/div/div/div['+str(i)+']/div[3]/button').click()                      
        except:
            break














