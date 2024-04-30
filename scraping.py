import os

import numpy as np
import pandas as pd
import serpapi

# From youtube video: scraping shopping tab using google api

google_api = os.environ['google_api']
client = serpapi.Client(api_key=google_api)

  
results = client.search({
  'engine': 'google_shopping',
  'q': 'phone',
  'num': '100',
})

# End of code from youtube video

# A list of all wanted attributes
arg_list = ['title',
            'extracted_price',
            'rating']

arg_list = np.array(arg_list)

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
      # Converts the extracted price to an integer
      if arg == 'extracted_price':
        product[arg] = int(product[arg])
        
      p_list.append(product[arg])
    #  If the attribute is not in the product dictionary, appends 0 to the list
    except KeyError:
      p_list.append(0)
  
  # Append the list p_list to the nested list, shopping_results, 
  # that contains a list of attributes for each product
  shopping_results.append(p_list)

# Create a data frame from the nested list and add it to a csv file
df = pd.DataFrame(shopping_results, columns = arg_list) 
header_str = ','.join(arg_list)
file = np.savetxt('scraping.csv', df, delimiter = ',', fmt = '%s', header = header_str)

