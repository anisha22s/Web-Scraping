# -*- coding: utf-8 -*-
"""DDR HW3.ipynb


"""

import pandas as pd
import numpy as np
import re
from IPython.display import HTML
import time
from bs4 import BeautifulSoup
import requests


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0',
    'HTTP_CONNECTION':"keep-alive",
    'HTTP_ACCEPT':'*/*',
    'HTTP_ACCEPT_ENCODING':'gzip, deflate',
    'HTTP_HOST':'MyVeryOwnHost'}

url = "https://www.barnesandnoble.com/b/books/_/N-1fZ29Z8q8?Nrpp=40&page=1"
r = requests.get(url, headers = headers)
soup = BeautifulSoup(r.text, 'lxml')

###This was not required in the submission but just adding here as it helped answer the question in Part1
element = soup.select("div h3.product-info-title a")

#printing titles
for x in element:
    print(x.text)

#printing links
for example in element:
        print(example.get("href"))

import re


##Using the URL identified above and writing code that loads the first page with 40 items per page of “B&N Top 100”.

url= "https://www.barnesandnoble.com/b/books/_/N-1fZ29Z8q8?Nrpp=40&page=1"
#GET request to the url .
page = requests.get(url,headers=headers).text
soup = BeautifulSoup(page, 'lxml') #parse html

from urllib.parse import urlsplit


#creating a list of each book’s product page URL. This list should be of length 40.

#empty list to store links
link = []

#loop through the list and append links to the list
for i in soup.select("div.product-shelf-title"):
  href = i.a['href']
  link.append(href)

#by investigating the website, the links printed from the inspect does not contant the main page address address, but only the portion after that
#we will need to concatenate 'https://www.barnesandnoble.com' before each link

conc = 'https://www.barnesandnoble.com'
for i in range(len(link)):
    link[i]=conc+link[i]

print(link)
len(link)

headers2={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36'}


for url in range(len(link)): 
    response = requests.get(link[url], headers = headers)
    filename = 'BNTOP100_{}.html'.format(url+1) #naming files based on search result number
    with open(filename, "w") as file: #writing data into the file
        file.write(response.text)
    time.sleep(5) #Each page request will be followed by 5sec pause

""" a separate piece of code that loops through the pages you downloaded above, opens and parses them into a Python or Java xxxxsoup-object. Next, access the “Overview” section of the page and print the first 100 characters of the overview text to screen."""

#4. d)
for i in range(0,40): #we will create a for loop to loop through all 40 pages and get url
    with open (f'BNTOP100_{i+1}.html') as fp: #access locally saved html files in the formal 'BNTOP100_{result number}.html'
        soup2 = BeautifulSoup(fp, 'lxml') #bs object to parse
        ele = soup2.find_all('div', class_= 'overview-cntnt') #tags and class for overview
        chr100 = ''
        for c in ele:
            first100 = chr100 + c.text.strip('\n') #get the first hunderd character and change the line
        print(first100[0:100])
