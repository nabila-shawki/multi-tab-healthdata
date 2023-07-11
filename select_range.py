import plotly.express as px
import dash_bootstrap_components as dbc
import dash
from dash import html, dcc
from dash.dependencies import Output, Input
import pandas as pd
from app import app


# layout of second (trends) tab ******************************************
range_layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.H2("More Twitter analysis to come...")
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='scatter', figure={})
        ], width=6),
        dbc.Col([
            dcc.Graph(id='scatter2', figure={})
        ], width=6)
    ])
])