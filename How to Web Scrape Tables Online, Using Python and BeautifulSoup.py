
#---How to Web Scrape Tables Online, Using Python and BeautifulSoup---


##################################### -Importing Necessary Libraries- #############################################

#You have to install the BeautifulSoup library first to import these
#Check out the the beginning of my article here to see how to install BeautifulSoup: https://medium.com/analytics-vidhya/how-to-web-scrape-tables-online-using-python-and-beautifulsoup-36d5bafeb982
import requests
from bs4 import BeautifulSoup
import pandas as pd


##################################### -Grabs The HTML From The Website- #############################################

#Input the URL of the web page you want to scrape the table off of
url = 'https://www.nfl.com/standings/league/2020/reg/'
#Asks the server we can copy the HTML
page = requests.get(url)
#Parses the HTML of the webpage and copies it into Python
soup = BeautifulSoup(page.text, 'lxml')


##################################### -Find The Table- #############################################

#Find the appropriate tag and class for the table you want to scrape
table_data = soup.find('table', class_ = "d3-o-table d3-o-table--row-striping d3-o-table--detailed d3-o-standings--detailed d3-o-table--sortable {sortlist: [[4,1]], sortinitialorder: 'desc'}")


##################################### -Headers- #############################################

#This chunk of code gets all the headers of the Table and puts them into an empty dataframe
headers = []
for i in table_data.find_all('th'):
    title = i.text.strip()
    headers.append(title)
df = pd.DataFrame(columns = headers)

##################################### -Body of Table- #############################################

#The for loop goes through each row of the table and adds the row into our dataframe in python
for j in table_data.find_all('tr')[1:]:
        row_data = j.find_all('td')
        row = [tr.text.strip() for tr in row_data]
        length = len(df)
        df.loc[length] = row





