# import modules
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Start of Code from Geeksforgeeks
try:
  from googlesearch import search
except ImportError: 
  print("No module named 'google' found")

# to search
query = "Funny Monkey Compilation"

for j in search(query, tld="co.in", num=10, stop=10, pause=2):
  print(j)

# Retrieve html data of url website (ex: airpods shopping tab)
URL = "https://www.google.com/search?sca_esv=7534dc616f2a754b&sxsrf=ACQVn09YZGZDVpgj4buptO8u5MZCstAQ5Q:1711987061809&q=airpods&tbm=shop&source=lnms&prmd=sivnmbtz&ved=1t:200715&ictx=111&biw=1536&bih=695&dpr=1.25"
#page = requests.get(URL)


#soup = BeautifulSoup(page.content, "html.parser")
#results = soup.find(id="main")
#price_elements= results.find_all("div", class_="a8pemb OFFNJ")
# End of Code from Geeksforgeeks
