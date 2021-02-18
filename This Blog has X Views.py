
##################################### -PLS READ- ################################################################################################

'''

The code you see below is from my article "This Blog has X Views and Y Claps".

The code will login into my Medium account, navigate Medium until it finds this article,
and then it will change the title to the amount of views and claps the article actually has.

This was all in an attempt to create a fully automated up-to-date article.

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
import time
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


##################################### -Part 1: Logging into Medium- ################################################################################################

#--Summary: This section of code will login on my account for Medium, by inputting my email address and password

#Opens up a new browser and goes to the login page of Medium
driver = webdriver.Chrome('C:/Web Scraping course/chromedriver.exe')
driver.get('https://medium.com/m/signin')

#Will click on the sign in with Facebook button
driver.find_element_by_xpath('//*[@id="susi-modal-fb-button"]/div/a').click()

#The chunk of code below will input my email address and password then press the log in button
email = driver.find_element_by_xpath('//*[@id="email"]')
email.send_keys('chris.zita@bell.net')
password = driver.find_element_by_xpath('//*[@id="pass"]')
password.send_keys('Cowboys9!')
driver.find_element_by_xpath('//*[@id="loginbutton"]').click()

#This code tells the program to wait until the home page of Medium has loaded in
element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/nav/div/div/div/div/div[2]/div/div[5]/div/button/div/img')))


##################################### -Part 2: Navigating Medium- ################################################################################################

#--Summary: This section of code will navigate through medium to find the "This Blog has X Views and Y Claps" artice

#This chunk of code clicks on my profile and goes to my stats page
driver.find_element_by_xpath('//*[@id="root"]/div/nav/div/div/div/div/div[2]/div/div[5]/div/button/div/img').click()
time.sleep(1)
driver.find_element_by_xpath('//*[@id="metabarActionsMenu"]/div/ul/li[5]/p/a').click()
time.sleep(2)
driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')


#This chunk of code goes through all my articles and finds the one with "Blog" in the title, saves the number of views it has and then goes to that stories page
soup = BeautifulSoup(driver.page_source, 'lxml')
posts = soup.find_all('tr', class_ = 'sortableTable-row js-statsTableRow')
df = pd.DataFrame({'Link':[''],'Name':[''], 'Views':['']})

for i in posts:
    link = i.find('a').get('href')
    name = i.find('a').text
    views = i.find('span', class_ = 'sortableTable-number').get('title')
    df = df.append({'Link':link,'Name':name, 'Views':views}, ignore_index = True)

def title(x):
    if 'Blog' in x:
        return 1
    else:
        return 0

df['Num'] = df['Name'].apply(title)
df2 = df[df['Num'] == 1]
views = df2.iloc[0,2]

driver.get(df2.iloc[0,0])
driver.find_element_by_xpath('//*[@id="root"]/div/div[4]/div[1]/div/div[1]/div[1]/div/div[2]/h2/a').click()
time.sleep(10)


##################################### -Part 3: Inside The Article- ################################################################################################

#--Summary: This section of code will perform all the changes inside the article and publish the newly edited story

#Finds and stores the number of claps the article has
num_claps = driver.find_element_by_xpath('//*[@id="root"]/div/div[3]/div[5]/div/div[1]/div/div[4]/div/div[1]/div[1]/span[2]/div/div[2]/div/p/button').text
num_claps = num_claps.split(' ')[0]

#Gets the username of the last person who clapped on the article
driver.find_element_by_xpath('//*[@id="root"]/div/div[3]/div[5]/div/div[1]/div/div[4]/div/div[1]/div[1]/span[2]/div/div[2]/div/p/button').click()
time.sleep(1)
last_person_clapped = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div[2]/div/div[1]/div[2]/a/h2').text
driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div/button').click()
time.sleep(1)

#Clicks the edit story button
driver.find_element_by_xpath('/html/body/div/div/div[3]/article/div/section[1]/div[1]/div/div[2]/div/div/div[2]/div/div[3]/div/div/div/button').click()
driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[1]/ul/li[3]/p/a').click()
time.sleep(3)

#Deletes the inital title
driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/main/article/div[1]/section[1]/div[2]/div[1]/h3').clear()
time.sleep(1)

#Puts the new title in place with the number of views and claps in it 
new_title = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/main/article/div[1]/section[1]/div[2]/div[1]/h3')
new_title.send_keys('This Blog Has ' +views+ ' Views and ' +num_claps+ ' Claps')
time.sleep(2)

#Changes the display name so people see can see the change
driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div[2]/div[2]/div[3]/button').click()
time.sleep(1)
driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div[3]/div[1]/ul/li[8]/button').click()
time.sleep(1)
driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div[3]/div[1]/div/div/div[1]/div[2]/p').clear()
time.sleep(2)
new_title = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div[3]/div[1]/div/div/div[1]/div[2]')
new_title.send_keys('This Blog Has ' +views+ ' Views and ' +num_claps+ ' Claps')
time.sleep(1)
driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div[3]/div[1]/div/div/div[4]/div/button').click()
time.sleep(1)
driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div[2]/div[2]/div[3]/button').click()
time.sleep(1)

#Goes to the "last person who clapped was" line and inputs the username that the code saved
driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/main/article/div[1]/section[2]/div[2]/div/h3[4]').clear()
time.sleep(1)
last_clapped = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/main/article/div[1]/section[2]/div[2]/div/h3[4]')
last_clapped.send_keys('The last person who clapped was ' + str(last_person_clapped))
last_clapped.send_keys(Keys.ENTER)
time.sleep(2)

#Saves and publishes the article
driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div[2]/div[2]/div[2]/button').click()
time.sleep(3)

driver.close()









