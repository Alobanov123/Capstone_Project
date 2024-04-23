import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, dcc, html

import plotly.express as px
import pandas as pd

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

df = pd.read_csv('scraping.csv')

app.layout = dbc.Container([
  html.H1("Budgeting and Shopping Tool", className='mb-2', style={'textAlign':'center'}),

  dbc.Row([
    dbc.Col([
      dcc.Markdown('# Enter a product you would like to search'),
      my_query := dcc.Input(
        value='Type Text')
    ], width=6),


    dbc.Col([
      dcc.Dropdown(
        id='category',
        value='price',
        clearable=False,
        options=[{'label': df.columns[i], 'value': df.columns[i]} for i in [3, 8]]
      )
    ])
  ]),

  dbc.Row([]),

  dbc.Row([])
])


@app.callback(
    Input(my_input, component_property='value')
)

def update_graph(el_texto):
  return el_texto


if __name__ == '__main__':
   app.run_server(debug=True)
