
#---Downloading Google Images, Using Python (2021)---


##################################### -Importing Necessary Libraries- #############################################

#You have to install selenium first to import these libraries
#I created a short 4-minute video on how to do this just use this link: https://www.youtube.com/watch?v=VYHxIUnvmpQ&t=1s
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


##################################### -Going Through The Google Images Home Page- #############################################

#Opens up a Chrome browser using the driver you should have downloaded and goes to Google.com
driver = webdriver.Chrome('C:/File_Path/chromedriver.exe')
driver.get('https://www.google.ca/imghp?hl=en&tab=ri&authuser=0&ogbl')

#Locates where the search box
box = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')
#Inputs what you want to search for into the search box
box.send_keys('put what you want to search for here (ex: giraffe)')
#Presses enter to search up what you inputted
box.send_keys(Keys.ENTER)


##################################### -Scrolls All The Way To The Bottom Of The Page- #############################################

#Finds the height of the current page
last_height = driver.execute_script('return document.body.scrollHeight')


while True:
    #Tells the page to scroll all the way to the bottom
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    #Stops the program for 2 seconds
    time.sleep(2)
    #Returns the height of the page after the driver scrolls down
    new_height = driver.execute_script('return document.body.scrollHeight')
    #This part will click the "see more photos button when it pops up"
    try:
        driver.find_element_by_xpath('//*[@id="islmp"]/div/div/div/div/div[5]/input').click()
        time.sleep(2)
    except:
        pass
    #If the returned height is the same as the one found on line 28 the loop stops cause it means we couldn't scroll anymore
    if new_height == last_height:
        break
    last_height = new_height

    
##################################### -Downloads The Images- #############################################    
    
#The for loop will loop through the first 100 photos and take screenshots of them.
#Those screenshots are then saved into the file you specify
for i in range(1, 100):
    try:
        driver.find_element_by_xpath('//*[@id="islrg"]/div[1]/div['+str(i)+']/a[1]/div[1]/img').screenshot('C:\File path where you will save the image\image.png')
    except:
        pass
   
