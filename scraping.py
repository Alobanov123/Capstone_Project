import os

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

# From youtube video: scraping shopping tab using google api

google_api = os.environ['google_api']
client = serpapi.Client(api_key=google_api)

results = client.search({
  'engine': 'google_shopping',
  'q': 'headphones',
})

print(find_min_product(results, price_dict))


