# Import necessary libraries
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Initialize the Dash app
app = dash.Dash(__name__)

# For this example, let's use the iris dataset
df = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv')

# Define the layout of the app
app.layout = html.Div([
    html.H1("Iris Data Dashboard", style={'textAlign': 'center', 'color': '#7FDBFF'}),
    html.Div([
        html.Div([
            html.Label('Select Species'),
            dcc.Dropdown(
                id='species-dropdown',
                options=[{'label': i, 'value': i} for i in df['species'].unique()],
                value='setosa'
            ),
            html.Label('Select Feature'),
            dcc.Dropdown(
                id='features-dropdown',
                options=[{'label': i, 'value': i} for i in df.columns if i != 'species'],
                value='sepal_width'
            ),
            html.Label('Select Plot Type'),
            dcc.RadioItems(
                id='plot-type',
                options=[{'label': i, 'value': i} for i in ['Scatter', 'Histogram']],
                value='Scatter',
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '0 20'}),
        html.Div([
            html.Label('Select Number of Points'),
            dcc.Slider(
                id='num-points-slider',
                min=1,
                max=len(df),
                value=len(df),
                marks={str(i): str(i) for i in range(1, len(df)+1, 20)},
                step=None
            )
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block', 'padding': '0 20'})
    ], style={'borderBottom': 'thin lightgrey solid', 'backgroundColor': 'rgb(250, 250, 250)', 'padding': '10px 5px'}),
    html.Div([
        dcc.Graph(id='graph'),
        dcc.Graph(id='graph-all')
    ])
])

# Define a callback function that will update the graph based on the dropdown selection
@app.callback(
    [Output('graph', 'figure'),
     Output('graph-all', 'figure')],
    [Input('species-dropdown', 'value'),
     Input('features-dropdown', 'value'),
     Input('num-points-slider', 'value'),
     Input('plot-type', 'value')]
)
def update_graph(selected_species, selected_feature, num_points, plot_type):
    dff = df[df['species'] == selected_species]
    num_points = min(num_points, len(dff))  # Ensure num_points does not exceed number of rows in dff
    dff = dff.sample(num_points)
    if plot_type == 'Scatter':
        figure = px.scatter(dff, x=selected_feature, y="sepal_length", color="species")
    else:
        figure = px.histogram(dff, x=selected_feature, color="species")
    figure_all = px.scatter(df, x=selected_feature, y=df.columns[df.columns != selected_feature], color="species")
    return figure, figure_all

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)