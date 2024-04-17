import os
import pandas as pd
import serpapi
import numpy as np

# Create a list that orders the results by price

def sort_by_price(results):
  my_list = []
  for product in results['shopping_results']:
    price = product['price'].replace('$', '')
    price = float(price.replace(',', ''))
    my_list.append(price)
  my_list.sort()
  return(my_list)

# Function that returns the product with the lowest price

def find_min_product(results, dict):
  my_products = []
  price = sort_by_price(results)[0]
  print(price)
  for product in dict:
    if dict[product] == price:
      my_products.append(product)
  return(my_products)

# Creates a dictionary of the product names and prices

def create_dict(results):
  price_dict = {}
  for product in results['shopping_results']:
    price = product['price']
    price = price.replace('$', '')
    price = price.replace(',', '')
    price = float(price)
    price_dict[product['title']] = price
  return(price_dict)


# user_input = input("Enter a search term: ")

# From youtube video: scraping shopping tab using google api

google_api = os.environ['google_api']
client = serpapi.Client(api_key=google_api)

results = client.search({
  'engine': 'google_shopping',
  'q': 'phone',
  'num': 100,
})

shopping_results = results['shopping_results']
df = pd.DataFrame.from_records(shopping_results) 
file = np.savetxt('scraping.csv', df, delimiter=',', fmt='%s')


'''
for product in results['shopping_results']:
  product_dict = {
    'title': product['title'],
    'source': product['source'],
    'price': product['extracted_price'],    
    'image': product['thumbnail'],
    'rating': product['rating'],
    'reviews': product['reviews'],
    'store_rating': product['store_rating'],
    'store_reviews': product['store_reviews'],
    'second_hand_condition': product['second_hand_condition'],
    'link': product['link'],
    'product_comparisons': product['serpapi_product_api_comparisons'],
    }
  json_list.append(product_dict)

# print(json_list)

'''

