# -*- coding: utf-8 -*-
"""NEW Anisha Indiv Proj.ipynb


"""

import pandas as pd
import numpy as np
import re
from IPython.display import HTML
import time
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlsplit

"""a) use the URL identified above and write code that loads eBay's search result page containing sold "amazon gift card". Save the result to file. Give the file the filename "amazon_gift_card_01.htm"."""



url = "https://www.ebay.com/sch/i.html?_fsrp=1&rt=nc&_nkw=amazon+gift+card&_sacat=0&LH_Sold=1"

headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0',
            'HTTP_CONNECTION':"keep-alive",
            'HTTP_ACCEPT':'*/*',
            'HTTP_ACCEPT_ENCODING':'gzip, deflate',
            'HTTP_HOST':'MyVeryOwnHost'}

r = requests.get(url, headers = headers) #GET request to the url .
pgcontent = r.content
soup = BeautifulSoup(r.text, 'lxml') #parse 

# Save result to a file
with open("Amazon_gift_card_01.htm", "w") as file:
    file.write(str(soup))
            
        
           


"""b) take your code in (a) and write a loop that will download the first 10 pages of search results. Save each of these pages to "amazon_gift_card_XX.htm" (XX = page number). IMPORTANT: each page request needs to be followed by a 10 second pause.  Please remember, you want your program to mimic your behavior as a human and help you make good purchasing decisions."""


for page in range(1, 11): #loop through first 10 pages
    url2 = url + "&_pgn=" + str(page) #as seen in question 1.1 f), aadding variable  that identifies page number
    response = requests.get(url2, headers = headers) #GET request to the url .
    soup2 = BeautifulSoup(response.content, "lxml")
    with open("amazon_gift_Card_"+str(page)+".html", "w") as file: #saving in specified format
        file.write(str(soup2))
    time.sleep(10) #Each page request will be followed by 10sec pause


"""c) write code that loops through the pages you downloaded in (b), opens and parses them to a Python or Java xxxxsoup-object."""


# loops through the pages downloaded
for i in range(1, 11):
    with open(f"amazon_gift_Card_{i}.html", "r") as file:
        content = file.read() #open

    soup = BeautifulSoup(content, 'lxml') #parses to a BS object


"""d) using your code in (c) and your answer to 1 (g), identify and print to screen the title, price, and shipping price of each item."""

  
for i in range(1, 11):
    with open(f"amazon_gift_Card_{i}.html", "r") as file:
        content = file.read() #open

    soup = BeautifulSoup(content, 'lxml')
        
        # Find all the items on the page
    items = soup.find_all("div", class_="s-item__wrapper")
        
    for index, item in enumerate(items):
        if index == 0: # the first itme for each page shows an invalid ('Shop on eBay). we will get rid of it
            continue
        # Loop through each item and extract the title, price, and shipping price     
        title = item.find("span", role="heading")
        price = item.find("span", class_="s-item__price")
        shippingprice = item.find("span", class_="s-item__shipping s-item__logisticsCost")

        if title:
            t = title.text
            print("Title:",t)
                
        if price:
            p = price.text
            print("Price:",p)
              
        if shippingprice:
            shipping = shippingprice.text
            print("Shipping:",shipping)
            
        else:
            print("Shipping tag not found.") #if clauses for wherever shipping details are missing 



     
#Recreating the previous code but this time appending to a list
# loops through the pages downloaded
mylist = [] 
for i in range(1, 11):
    with open(f"amazon_gift_Card_{i}.html", "r") as file:
        content = file.read() #open

    soup = BeautifulSoup(content, 'lxml') #parses to a BS object
          
    # Find all the items on the page
    items = soup.find_all("div", class_="s-item__wrapper")
          
      
    # Loop through each item and extract the title, price, and shipping price
    for index, item in enumerate(items):
        if index == 0: # Skip the first item for each page
            continue

          
        title = item.find("span", role="heading")
        price = item.find("span", class_="s-item__price")
        shippingprice = item.find("span", class_="s-item__shipping s-item__logisticsCost")
              

        result = {} #create an empty dictionary to store title, price and ship

        if title:
        result['Title'] = title.text
        else:
        result['Title'] = "Title not found" #one instance where title is coming blank, to overcome that we will write this statement
              
        if price:   
        result['Price'] = price.text
        else:
        result['Price'] = "Price not found"
            
        if shippingprice:
        result['ShippingPice'] = shippingprice.text
        else:
        result['ShippingPice'] = "ShippingPice not found" #if clauses for wherever shipping details are missing 


        mylist.append(result)
print(mylist)


"""e) using RegEx, identify and print to screen gift cards that sold above face value. e., use RegEx to extract the value of a gift card from its title when possible (doesn’t need to work on all titles, > 90% success rate if sufficient). Next compare a gift card’s value to its price + shipping (free shipping should be treated as 0).  If value < price + shipping, then a gift card sells above face value."""

       
#extracting numbers from Titles to get the face value. some titles have multiple values. we will pick the first item

new_list = []
for d in mylist:
          
    facevalue = re.findall(r'\$(\d+)', d['Title'])  #extracting the amount from title
    if len(facevalue) != 0: #we will only consider for those where we were able to extract the face value, aka, where amount was present in title
    facevalue = facevalue[0] #extract first amount for cases where there are mutiple
    else:
    facevalue = 0

    price = re.findall(r'\d+', d['Price'])

    if len(price) != 0:
    price = price[0]
    else:
    price = 0

    shipprice = re.findall(r'\d+', d['ShippingPice']) 

    if len(shipprice) != 0:
    shipprice = shipprice[0]
    else:
    shipprice = 0
          

    if int(facevalue) < (int(price) + int(shipprice)) and facevalue != 0: #We will not consider those where face value was not extracted from title
    new_list.append(d)

print(new_list) #list of items where face value is smaller than the selling + shipping price


"""f) What fraction of Amazon gift cards sells above face value? Why do you think this is the case?"""

print(len(new_list)/len(mylist))

print("34.8% of cards sell above face value. This could be because of the added shipping price. Also to highlight the limitations of this approach- need to consider that this number is not exactly correct as we have extracted Face value from the titles and some titles did not have face value so we have not considered those in the previous question.")


