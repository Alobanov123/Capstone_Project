# reference https://github.com/plotly/tutorial-code/blob/main/Videos/matplotlib-dashboard.py
from dash import Dash, html, dcc, Input, Output  
import plotly.express as px
import dash_ag_grid as dag
import dash_bootstrap_components as dbc  
import pandas as pd     

import matplotlib     
matplotlib.use('agg')
import matplotlib.pyplot as plt
import base64
from io import BytesIO

df = pd.read_csv('https://replit.com/@alobanov/CapstoneProject#scraping.csv')

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container([
    html.H1("Budgeting and Shopping Tool", className='mb-2', style={'textAlign':'center'}),

    dbc.Row([
      dcc.Input(
          id='query',
          type= 'text',
          placeholder="Enter a product you would like to search",
          required=True,
      )
    ]),
  
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='category',
                value='Price',
                clearable=False,
                options=df.columns[1:])
        ], width=4)
    ]),

    dbc.Row([
        dbc.Col([
            html.Img(id='bar-graph-matplotlib')
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='bar-graph-plotly', figure={})
        ], width=12, md=6),
        dbc.Col([
            dag.AgGrid(
                id='grid',
                rowData=df.to_dict("records"),
                columnDefs=[{"field": i} for i in df.columns],
                columnSize="sizeToFit",
            )
        ], width=12, md=6),
    ], className='mt-4'),

])

# Create interactivity between dropdown component and graph
@app.callback(
    Output(component_id='text', component_property='children'),
    Input(component_id='text', component_property='value')
  '''
    Output(component_id='bar-graph-matplotlib', component_property='src'),
    Output('bar-graph-plotly', 'figure'),
    Output('grid', 'defaultColDef'),
    Input('category', 'value'),
  '''
)

def plot_data(selected_yaxis):

    # Build the matplotlib figure
    fig = plt.figure(figsize=(14, 5))
    plt.bar(df['Item'], df[selected_yaxis])
    plt.ylabel(selected_yaxis)
    plt.xticks(rotation=30)

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    fig_data = base64.b64encode(buf.getbuffer()).decode("ascii")
    fig_bar_matplotlib = f'data:image/png;base64,{fig_data}'

    # Build the Plotly figure
    fig_bar_plotly = px.bar(df, x='Item', y=selected_yaxis).update_xaxes(tickangle=330)

    my_cellStyle = {
        "styleConditions": [
            {
                "condition": f"params.colDef.field == '{selected_yaxis}'",
                "style": {"backgroundColor": "#d3d3d3"},
            },
            {   "condition": f"params.colDef.field != '{selected_yaxis}'",
                "style": {"color": "black"}
            },
        ]
    }

    return fig_bar_matplotlib, fig_bar_plotly, {'cellStyle': my_cellStyle}


if __name__ == '__main__':
   app.run(debug=True)