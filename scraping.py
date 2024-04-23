import os

import numpy as np
import pandas as pd
import serpapi

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
  'num': '100',
})

# A list of all wanted attributes
arg_list = ['position',
            'title', 
            'source', 
            'price',
            'extracted_price',
            'old_price',
            'delivery',
            'thumbnail',
            'rating',
            'reviews',
            'store_rating',
            'store_reviews']

# Create a nested list of all the products wanted attributes
shopping_results = []

# Iterate through the results
for product in results['shopping_results']:
  p_list = []
  # Append the wanted attributes to list p_list
  for arg in arg_list:
    # Removes commas from string objects
    # Ignores if the item does not have the attribute
    try:
      if isinstance(product[arg], str):
        product[arg] = product[arg].replace(',', '')

      # Removes .com from source to make data more uniform
      if arg == 'source':
        product[arg] = product[arg].replace('.com', '')
      p_list.append(product[arg])
    #  If the attribute is not in the product dictionary, add NA to the list
    except KeyError:
      p_list.append('NA')
  
  # Append the list p_list to the list shopping_results that contains all the products
  shopping_results.append(p_list)

# Create a data frame from the nested list and add it to a csv file
df = pd.DataFrame(shopping_results) 

header_str = ','.join(arg_list)
file = np.savetxt('scraping.csv', df, delimiter = ',', fmt = '%s', header = header_str)