import plotly.express as px
import dash_bootstrap_components as dbc
from utils.AndroidDat import AndroidDat, WeeklyMetricsAnalyzer
from utils.utils_class import read_dat, extract_dates
import dash
from dash import html, dcc
from dash.dependencies import Output, Input, State
import pandas as pd
import numpy as np
from app import app
from card_maker import *

# Function to generate the week information
def get_week_info(df):
    week_info = []
    for week in df['Week #'].unique():
        start = df[df['Week #'] == week]['Date'].min().strftime('%Y-%m-%d')
        end = df[df['Week #'] == week]['Date'].max().strftime('%Y-%m-%d')
        week_str = f"Week {week}: {start} - {end}"
        week_info.append(week_str)
    return week_info

# global variables
#
fname = "https://raw.githubusercontent.com/nabila-shawki/multi-tab-healthdata/main/data/week_9.csv"
start_date = pd.to_datetime('2023-06-05')
end_date = pd.to_datetime('2023-07-23')
dates = pd.date_range(start='2023-06-05', end='2023-07-23', freq='D')
target_count = 2000 # steps
target_move = 20 # minutes

# get the filtered dat
#
dat = read_dat(fname, start_date, end_date, target_count)
print(dat.filtered_df.shape)

# # Save DataFrame to a CSV file
#dat.filtered_df.to_csv('data.csv', index=False)

# get the weeks
#
week_list = get_week_info(dat.filtered_df)
print(week_list)

weekly_metrics = {}

# get the weekly metrics
#
for week_num in week_list:
    start_date, end_date = extract_dates(week_num)

    # Create an instance of WeeklyMetricsAnalyzer
    #
    analyzer = WeeklyMetricsAnalyzer(dat.filtered_df)
    analyzer.extract_metrics(start_date, end_date)

    weekly_metrics[week_num] = analyzer


weekly_layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Select a week"),
                        dcc.Dropdown(
                            id="week-dropdown",
                            multi=False,
                            value=week_list[0],
                            # options=[
                            #     {"label": "10", "value": 10},
                            #     {"label": "20", "value": 20},
                            #     {"label": "30", "value": 30},
                            # ],
                            options=[{'label': week_str, 'value': week_str} for week_str in week_list],  

                            clearable=False,
                            persistence=True,
                            persistence_type='session',
                            ),
                    ],
                    width=4,
                ),
            ],
            className="mt-4",
            align="left",
        ),
        

        dbc.Row(            
                    # Health metrics title
                    #     
                html.H3("Physical Activity Overview"), 
                            style={'margin-top':'25px', 'justify-content':'center'},
                align = "center",
                className="mt-4",
        ),

        dbc.Row(
            [
                # Weight
                #
                dbc.Col([
                    html.Div(id="activity_metrics")
                ]),

            ]

        ),

        dbc.Row(            
                    # Health metrics title
                    #     
                html.H3("Health Overview"), 
                            style={'margin-top':'25px',  'justify-content':'center'},
                align = "center",
                className="mt-4",
        ),

        dbc.Row(
            [
                # Weight
                #
                dbc.Col([
                    html.Div(id="health_metrics")
                ]),

            ]

        ),

        dbc.Row(
            [
                # Weight
                #
                #html.Div(id="steps")
                

            ]

        ),
        
    ]
)


# # callback for making the plots
#  
@app.callback(
    
    Output('health_metrics', 'children'),
    Output('activity_metrics', 'children'),
    #Output('step_metrics', 'children'),
    # Output('heart-rate', 'children'),
    Input(component_id="week-dropdown", component_property="value"),
    #State(component_id="count-mentions", component_property="value"),
    #State(component_id="input-handle", component_property="value"),
)
def display_value(week_num):

    # get the current week's metrics
    #
    cur_week = weekly_metrics[week_num]

    # get the previous week's metrics
    #
    prev_week = week_list.index(week_num) - 1

    if prev_week >= 0:
            prev_week = weekly_metrics[week_list[prev_week]] 
    else:
        prev_week = cur_week
    
    print(cur_week, prev_week)

    # create the cards
    #
    weight_card = make_weight_card(cur_week, prev_week)
    heart_card = make_heart_card(cur_week)
    cal_card = make_calories_card(cur_week, prev_week)
    bp_card = make_bp_card(cur_week)
    step_card = make_step_card(cur_week, prev_week)
    active_card = make_active_min_card(cur_week, prev_week)
    speed_card = make_speed_card(cur_week, prev_week)
    distance_card = make_distance_card(cur_week, prev_week)
    total_target_card = make_target_card(cur_week, prev_week)
    pie_card = make_pie_card(cur_week)

    # health cards
    #
    health_1 = [weight_card, cal_card]
    health_2 = [ heart_card, bp_card]
    activity_1 = [total_target_card,step_card, active_card,pie_card]
    activity_2 = [distance_card, speed_card]
        
    # make the card layout
    health_layout = [
        #dbc.Row([dbc.Col(card, md=3) for card in cards]),
        dbc.Row(dbc.CardGroup(health_1)),
        dbc.Row(dbc.CardGroup(health_2)),
    ]

        # make the card layout
    activity_layout = [
        #dbc.Row([dbc.Col(card, md=3) for card in cards]),

            dbc.Row(
                [
                    dbc.Col([
                        dbc.Row(dbc.CardGroup(activity_1)),
                        dbc.Row(dbc.CardGroup(activity_2)),
                    ], 
                width='auto'),
            #     dbc.Col(nested_pie_chart(cur_week), 
            #     style={"width": "50%", "height": "50%"},
            #  )
             ],
            justify='center',  # Align the columns at the center
            align='center',   # Align the rows at the center
            ),
            

    ]

    

    return health_layout, activity_layout #, step_layout


