

##################################### -PLS READ- ################################################################################################

'''

The code you see below is from my article "I Got Banned From Every Social Media App On Purpose".

The code will login into my LinkedIn account, navigate LinkedIn until it finds a group I'm apart of.
After it selects a group a list of profiles come up from others in the group.

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
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time


##################################### -Getting Banned from LinkedIn- ################################################################################################


#Opens up a browser and goes to LinkedIn login page
driver = webdriver.Chrome(
        'C:/Web Scraping course/chromedriver.exe')
driver.get('https://www.linkedin.com/login')

#inputs an email and password for the login details
login = driver.find_element_by_xpath('//*[@id="username"]')
login.send_keys('#########')
password = driver.find_element_by_xpath('//*[@id="password"]')
password.send_keys('#########')
driver.find_element_by_xpath('/html/body/main/section[1]/div[2]/form/button').click()
driver.find_element_by_xpath('/html/body/div[7]/div[3]/div/div/div/aside[1]/div[2]/div/div[1]/ul/li[1]/a/div/li-icon').click()
driver.find_element_by_xpath('/html/body/div[7]/div[3]/div/div[2]/aside[2]/div[1]/div[1]/section/footer/a/button').click()

#This code scrolls and collects the urls of a bunch of people profiles
for i in range(1, 15):
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep(1)   
soup = BeautifulSoup(driver.page_source, 'lxml')
profiles = soup.find_all('div', class_ = 'groups-members-list__typeahead-result relative artdeco-typeahead__result ember-view')
len(profiles)

#This code will go through all the links the code above got and go to people's profiles and then keep connecting with them
profile_links = []
for i in profiles:
    link = i.find('a', {'data-control-name':'view_profile'}).get('href')
    link_full = 'https://www.linkedin.com'+link
    profile_links.append(link_full)
counter = 0
for i in profile_links[121:]:
    driver.get(i)
    time.sleep(30)
    counter+=1
    if counter == 100:
        break
    try:
        more_button = driver.find_element_by_xpath('/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[1]/section/div[2]/div[1]/div[2]/div/div/div[2]/div/button').click()
        time.sleep(1)
        connect = driver.find_element_by_xpath('/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[1]/section/div[2]/div[1]/div[2]/div/div/div[2]/div/div/div/ul/li[4]/div/div/span[1]').click()
        time.sleep(1)
        send = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[2]').click()

    except:
        try:
            x = driver.find_element_by_xpath('/html/body/div[4]/div/div/button').click()
            time.sleep(1)
            connect_button = driver.find_element_by_xpath('/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[1]/section/div[2]/div[1]/div[2]/div/div/div[1]/div/button').click()
            time.sleep(1)
            send = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[2]').click()
        except:
            pass


