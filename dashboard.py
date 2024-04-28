# reference https://github.com/plotly/tutorial-code/blob/main/Videos/matplotlib-dashboard.py

# https://stackoverflow.com/questions/59001244/python-dash-app-updating-with-new-dataframe
from dash import Dash, Input, Output, dcc, html
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

import os
import pandas as pd
import numpy as np
import serpapi

import plotly.express as px
import matplotlib

matplotlib.use('agg')
import base64
from io import BytesIO

import matplotlib.pyplot as plt

google_api = os.environ['google_api']
client = serpapi.Client(api_key=google_api)

df = pd.read_csv('scraping.csv')

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container([
    html.H1("Shopping Tool", className='mb-2', style={'textAlign':'center'}),

    dbc.Row([
      dcc.Input(
          id='query',
          type= 'text',
          placeholder="Enter a product you would like to search",
          required=True,
          debounce=True
      )
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='category',
                value='price',
                clearable=False,
              options=[{'label': col, 'value': col} for col in df.columns[1:]]
            )
        ], width=4)
    ]),

    dbc.Row([
        dbc.Col([
            html.Img(id='bar-graph-matplotlib')
        ], width=12)
    ]),

    dbc.Row([
      dag.AgGrid(
        id='grid',
        rowData=df.to_dict('records'),
        columnDefs=[{"field": i} for i in df.columns],
        columnSize="sizeToFit")
    ]),

    dbc.Row([
      dcc.Graph(id='bar-graph-plotly', figure={}),
    ])
])

# Populate table with data
@app.callback(
  Output('grid','rowData'),
  Input('query','value'),
)

def query_csv(query):
  results = client.search({
    'engine': 'google_shopping',
    'q': query,
    'num': '100',
  })

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

        # Removes .com from source to make data more uniform
        if arg == 'source':
          product[arg] = product[arg].replace('.com', '')
        p_list.append(product[arg])
      #  If the attribute is not in the product dictionary, add NA to the list
      except KeyError:
        p_list.append(0)

    # Append the list p_list to the list shopping_results that contains all the products
    shopping_results.append(p_list)

  # Create a data frame from the nested list and add it to a csv file
  df = pd.DataFrame(shopping_results, columns=arg_list)
  header_str = ','.join(arg_list)
  file = np.savetxt('scraping.csv', df, delimiter = ',', fmt = '%s', header = header_str)
  dff = pd.read_csv('scraping.csv')
  # fill the table with data
  return dff.to_dict('records')

# Create interactivity between dropdown component and graph
@app.callback(
  Output(component_id='bar-graph-matplotlib', component_property='src'),
  Output('bar-graph-plotly', 'figure'),
  Output('grid', 'defaultColDef'),
  Input('category', 'value'),
  Input('grid', 'rowData'),
)

def plot_data(selected_cat, data):
  
   # Build the matplotlib figure
  
   fig = plt.figure(figsize=(14, 5))
   df = pd.DataFrame(data)
   num_bins = 10
   plt.hist(df[selected_cat], bins=num_bins, edgecolor='black')
   plt.ylabel('Number of Items')

   # Save it to a temporary buffer.
   buf = BytesIO()
   fig.savefig(buf, format="png")
   # Embed the result in the html output.
   fig_data = base64.b64encode(buf.getbuffer()).decode("ascii")
   fig_hist_matplotlib = f'data:image/png;base64,{fig_data}'

   # Build the Plotly figure
   fig_box_plotly = px.box(df, x=selected_cat, labels = {'Value': 'Value', 'Count': 'Number of Items'})

   my_cellStyle = {
       "styleConditions": [
           {
               "condition": f"params.colDef.field == '{selected_cat}'",
               "style": {"backgroundColor": "#d3d3d3"},
           },
           {   "condition": f"params.colDef.field != '{selected_cat}'",
               "style": {"color": "black"}
           },
       ]
   }

   return fig_hist_matplotlib, fig_box_plotly, {'cellStyle': my_cellStyle}


if __name__ == '__main__':
   app.run(debug=False)