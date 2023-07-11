import plotly.express as px
from utils.AndroidDat import AndroidDat
from utils.utils_class import read_dat
import dash_bootstrap_components as dbc
import dash
from dash import html, dcc
from dash.dependencies import Output, Input
import pandas as pd
from datetime import datetime as dt
from app import app

# get the filtered dat
#
fname = "https://raw.githubusercontent.com/nabila-shawki/multi-tab-healthdata/main/data/week_4.csv"
start_date = pd.to_datetime('2023-06-05')
end_date = pd.to_datetime('2023-07-30')
dates = pd.date_range(start='2023-06-05', end='2023-07-30', freq='D')
target_count = 2000 # steps
target_move = 20 # minutes
dat = read_dat(fname, start_date, end_date, target_count)
print(dat.filtered_df.shape)



daily_layout = html.Div([
    dbc.Row([
    dcc.DatePickerSingle(
        id='date-picker',
        min_date_allowed=dt(2023, 6, 5),
        max_date_allowed=dt(2023, 7, 30),
        initial_visible_month=dt(2023, 6, 5),
        date=dt(2023, 6, 5).date()
    ),
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

