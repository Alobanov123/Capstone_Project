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

# A list of all wanted attributes
arg_list = ['position',
            'title', 
            'source', 
            'price',
            'extracted_price',
            'delivery',
            'thumbnail',
            'rating',
            'reviews',
            'store_rating',
            'store_reviews',
            'serp_product_api_comparisons']

# Create a dataframe from the results
shopping_results = []

# Iterate through the results
for product in results['shopping_results']:
  p_list = []
  # Append the wanted attributes to list p_list
  for arg in arg_list:
    # If the attribute is not in the product dictionary, add NA to the list
    if product[arg] == None:
      p_list.append(np.nan)
    else:
      p_list.append(product[arg])
  # Append the list p_list to the list shopping_results that contains all the products
  shopping_results.append(p_list)


