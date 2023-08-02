import plotly.express as px
from utils.AndroidDat import AndroidDat
from utils.utils_class import read_dat, read_daily_dat
import dash_bootstrap_components as dbc
import dash
from dash import html, dcc
from dash.dependencies import Output, Input
import pandas as pd
from datetime import datetime as dt
from app import app

# daily data
#
daily_csv = "https://raw.githubusercontent.com/nabila-shawki/multi-tab-healthdata/main/data/{}.csv"

# get the filtered dat
#
fname = "https://raw.githubusercontent.com/nabila-shawki/multi-tab-healthdata/main/data/week_9.csv"
start_date = pd.to_datetime('2023-06-05')
end_date = pd.to_datetime('2023-07-23')
dates = pd.date_range(start='2023-06-05', end='2023-07-23', freq='D')
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
        date=dt(2023, 6, 5).date(),
        persistence=True,
        persisted_props=['date'],
        persistence_type='session'
    ),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='step-bar', figure={})
        ], width=6),
        # dbc.Col([
        #     dcc.Graph(id='scatter2', figure={})
        # ], width=6)

        #html.Div(id='output-container')
    ])
])

@app.callback(
    Output('step-bar', 'figure'),
    [Input('date-picker', 'date')]
)
def update_output(date):

    # summary data
    #
    df = dat.filtered_df

    # get the data for the selected day only
    #
    selected_date = pd.to_datetime(date)
    selected_row = df.loc[df['Date'] == selected_date]

    # get the csv for the selected day
    #
    cur_date = daily_csv.format(date)
    day_df_obj = read_daily_dat(cur_date) #pd.read_csv(cur_date)
    day_df = day_df_obj.filtered_df
    
    day_df['Start time'] = pd.to_datetime(day_df['Start time'], format='%H:%M:%S.%f%z')
    
    day_df['End time'] = pd.to_datetime(day_df['End time'], format='%H:%M:%S.%f%z')
    #day_df['End datetime'] = pd.to_datetime(date.astype(str) + ' ' + day_df['End time'].astype(str))

    print(day_df)
    # Create a new column for the hourly interval
    day_df['Hourly interval'] = day_df['Start time'].dt.floor('H')

    # Group the data by hourly interval and calculate the mean for each column
    averaged_data = day_df.groupby('Hourly interval').mean()
    print(averaged_data) 
    # Remove unnecessary columns
    #averaged_data = averaged_data.drop(columns=['Start time', 'End time'])

    # Reset the index
    averaged_data = averaged_data.reset_index()

    # Update the data attribute with the averaged data
    day_df = averaged_data
    day_df['Hourly interval'] = day_df['Hourly interval'].dt.time

    fig = px.bar(day_df, x='Hourly interval', y='Step count')

    return fig
