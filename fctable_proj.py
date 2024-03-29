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


 

"""

we will write code that automatically logs into the website fctables.com Links to an external site.
Then we will verify that we have successfully logged in:  use the cookies you received during log in and write code to access https://www.fctables.com/tipster/my_bets/ Links to an external site..  Check whether the word “Wolfsburg” appears on the page.  Don’t look for your username to confirm that you are logged in (it won’t work) and use this page’s content instead.
"""

#referred to Professor's Flightware.py syntax from canvas to recreate this code
def 2A():
      URL = "https://www.fctables.com/user/login/"
      page1 = requests.get(URL)
      doc1 = BeautifulSoup(page1.content, 'html.parser')
              
      inputs = doc1.select("div.panel-body button[name=login_action]")[0]; #extracted from dev tool elements
      name = inputs.get("value")
      print(name) 
                
      time.sleep(5) #pause between two requests.

      #An open session carries the cookies and allows you to make post requests
      session_requests = requests.session()
      res = session_requests.post(URL, 
                                      data = {
                                            "login_username" : "anishasamant", # my username here
                                            "login_password" : "anisha2297", # my password here
                                            "login_action" : name,
                                            "user_remeber": 1})
                                  
      #get cookies
      cookies = session_requests.cookies.get_dict()
2A()

#2.2 B continued here
# remain in session
def main2():   
    page2 = session_requests.get("https://www.fctables.com/tipster/my_bets/",  cookies=cookies) #accessing bets website

    doc2 = BeautifulSoup(page2.content, 'html.parser')
main2()
print(cookies)
print(bool(doc2.findAll(text = "Wolfsburg 0-0 vs Bayern Munich"))) # Find for this text
