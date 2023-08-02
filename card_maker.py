import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
import dash
from dash import html, dcc
from dash.dependencies import Output, Input
from utils.utils_class import read_dat, extract_dates
import pandas as pd
import numpy as np
from app import app

def make_weight_card(cur_week, prev_week):
    
    change = cur_week.health_dat["Average weight"] - prev_week.health_dat["Average weight"]
    
    color = "danger" if change < 0 else "success"
    icon = "bi bi-arrow-down" if change < 0 else "bi bi-arrow-up"

    return dbc.Card(
        html.Div(
            [
                html.H4(
                    [
                        html.I(className="bi bi-person"), "Average Weight"
                    ]
                ),
                html.H4(f"{round(cur_week.health_dat['Average weight'], 2)} lb"),
                html.H5(
                    [html.I(className=icon), f"{round(change, 2)} lb"],
                    className=f"text-{color}",
                ),
            ],
            className=f"border-{color} border-start border-5",
        ),
        className="text-center text-nowrap my-2 p-2",
    )

def make_heart_card(cur_week):
    
    color = "success"

    return dbc.Card(
        html.Div(
            [
                html.H4(
                    [
                        html.I(className="bi bi-person"), f"Heart Rate (BPM)"
                    ]
                ),
                html.H4( f"Max: {int(cur_week.health_dat['Max heart rate'])}, Min: {int(cur_week.health_dat['Min heart rate'])}, Avg: {int(cur_week.health_dat['Average heart rate'])}"),
                # html.H5( f"Min: {int(cur_week.health_dat['Min heart rate'])}"),
                # html.H5( f"Avg: {int(cur_week.health_dat['Average heart rate'])}"),
            ],
            className=f"border-{color} border-start border-5",
        ),
        className="text-center my-2 p-2",
    )

def make_calories_card(cur_week, prev_week):
    
    cur_cal = cur_week.health_dat["Average calories"]
    prev_cal = prev_week.health_dat["Average calories"]

    if np.isnan(cur_cal):
        cur_cal = 0
    if np.isnan(prev_cal):
        prev_cal = 0

    change = cur_cal - prev_cal
    
    color = "danger" if change < 0 else "success"
    icon = "bi bi-arrow-down" if change < 0 else "bi bi-arrow-up"

    return dbc.Card(
        html.Div(
            [
                html.H4(
                    
                       [html.I(className="bi bi-person"), "Average calories burned"]
                    
                ),
                html.H4(f"{round(cur_cal, 2)} kcal"),
                html.H5(
                    [html.I(className=icon), f"{round(change, 2)} kcal"],
                    className=f"text-{color}",
                ),
            ],
            className=f"border-{color} border-start border-5",
        ),
        className="text-center text-nowrap my-2 p-2",
    )

def make_bp_card(cur_week):
        
    color =  "success"
    icon = "bi bi-arrow-up"

    return dbc.Card(
        html.Div(
            [
                html.H4(
                    [
                        html.I(className="bi bi-person"),"Blood Pressure (mmHg)"
                    ]
                ),
                html.H4(f"{int(cur_week.health_dat['Average BP systolic'])}/{int(cur_week.health_dat['Average BP diastolic'])}"),

            ],
            className=f"border-{color} border-start border-5",
        ),
        className="text-center text-nowrap my-2 p-2",
    )

def make_step_card(cur_week, prev_week):
    
    change = cur_week.activity_metric["Average step count"] - prev_week.activity_metric["Average step count"]
    
    color = "danger" if change < 0 else "success"
    icon = "bi bi-arrow-down" if change < 0 else "bi bi-arrow-up"

    #print(cur_week.week_data["Date"], cur_week.week_data["Step count"])

    fig = px.bar(cur_week.week_data, x="Date", y="Step count", color="Step count",
                 color_continuous_scale=['rgba(114, 89, 52, 1)', 'rgba(255, 179, 70, 1)'])

    # Disable hover data
    #fig.update_traces(hoverinfo='skip')

    # Set the bar colors with a color scheme
    fig.update_layout(colorway=["#1f77b4"])

    # Set a transparent background
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')

    # Set the height and width of the bar chart
    fig.update_layout(height=300, width=320)

    # Hide x and y labels
    fig.update_layout(xaxis_title="", yaxis_title="")
    fig.update_layout(coloraxis_showscale=False)
    fig.update_layout(yaxis_range=[0,4000])

    return dbc.Card(
        html.Div(
            [
                html.H4(
                    [
                        html.I(className="bi bi-smartwatch"), "Avg Step Count"
                    ],
                    style={"color": "rgba(255, 179, 70, 1)"}
                ),
                html.H4([f"{int(cur_week.activity_metric['Average step count'])} / 2000"],
                        style={"color": "rgba(255, 179, 70, 1)"}),
                html.H5(
                    [html.I(className=icon), f"{int(change)}"],
                    className=f"text-{color}",
                ),

               dcc.Graph(figure=fig)
            ],
            className=f"border-{color} border-start border-5",
        ),
        className="text-center text-nowrap my-2 p-2",
    )

def make_active_min_card(cur_week, prev_week):
    
    change = cur_week.activity_metric["Average activity time"] - prev_week.activity_metric["Average activity time"]
    
    color = "danger" if change < 0 else "success"
    icon = "bi bi-arrow-down" if change < 0 else "bi bi-arrow-up"

    
    fig = px.bar(cur_week.week_data, x="Date", y="Move Minutes count", color="Move Minutes count",
                 color_continuous_scale=['rgba(77, 50, 98, 1)', 'rgba(163, 122, 194, 0.8)'])

    # Disable hover data
    #fig.update_traces(hoverinfo='skip')

    # Set the bar colors with a color scheme
    fig.update_layout(colorway=["#1f77b4"])

    # Set a transparent background
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')

    # Set the height and width of the bar chart
    fig.update_layout(height=300, width=320)

    # Hide x and y labels
    fig.update_layout(xaxis_title="", yaxis_title="")
    fig.update_layout(coloraxis_showscale=False)
    fig.update_layout(yaxis_range=[0,40])

    return dbc.Card(
        html.Div(
            [
                html.H4(
                    [
                        html.I(className="bi bi-smartwatch"), "Avg Activity time"
                    ],
                     style={"color": "rgba(163, 122, 194, 0.8)"}
                ),
                html.H4([f"{round(cur_week.activity_metric['Average activity time'], 2)} / 20 min"],
                        style={"color": "rgba(163, 122, 194, 0.8)"}),
                html.H5(
                    [html.I(className=icon), f"{round(change, 2)} min"],
                    className=f"text-{color}",
                ),
                dcc.Graph(figure=fig)
            ],
            className=f"border-{color} border-start border-5",
        ),
        className="text-center text-nowrap my-2 p-2",
    )

def make_speed_card(cur_week, prev_week):
    
    change = cur_week.activity_metric["Average speed"] - prev_week.activity_metric["Average speed"]
    
    color = "danger" if change < 0 else "success"
    icon = "bi bi-arrow-down" if change < 0 else "bi bi-arrow-up"

    return dbc.Card(
        html.Div(
            [
                html.H4(
                    [
                        html.I(className="bi bi-smartwatch"), "Average Speed"
                    ]
                ),
                html.H4(f"{round(cur_week.activity_metric['Average speed'], 2)} mph"),
                html.H5(
                    [html.I(className=icon), f"{round(change, 2)} mph"],
                    className=f"text-{color}",
                ),
            ],
            className=f"border-{color} border-start border-5",
        ),
        className="text-center text-nowrap my-2 p-2",
    )

def make_distance_card(cur_week, prev_week):
    
    change = cur_week.activity_metric["Average distance"] - prev_week.activity_metric["Average distance"]
    
    color = "danger" if change < 0 else "success"
    icon = "bi bi-arrow-down" if change < 0 else "bi bi-arrow-up"

    return dbc.Card(
        html.Div(
            [
                html.H4(
                    [
                        html.I(className="bi bi-smartwatch"), "Average distance"
                    ]
                ),
                html.H4(f"{round(cur_week.activity_metric['Average distance'], 2)} miles"),
                html.H5(
                    [html.I(className=icon), f"{round(change, 2)} miles"],
                    className=f"text-{color}",
                ),
            ],
            className=f"border-{color} border-start border-5",
        ),
        className="text-center text-nowrap my-2 p-2",
    )

def make_target_card(cur_week, prev_week):
    
    change = cur_week.activity_metric["Days met target"] - prev_week.activity_metric["Days met target"]
    
    color = "danger" if change < 0 else "success"
    icon = "bi bi-arrow-down" if change < 0 else "bi bi-arrow-up"

    return dbc.Card(
        html.Div(
            [
                html.H4(
                    [
                        html.I(className="bi bi-smartwatch"), "Step Target Met"
                    ], 
                    style={"color": "rgba(15, 125, 229, 0.8)"}
                ),
                html.H4([f"{round(cur_week.activity_metric['Days met target'], 2)} / 7 days"],
                          style={"color": "rgba(15, 125, 229, 0.8)"}
                          ),
                html.H5(
                    [html.I(className=icon), f"{round(change, 2)} Days"],
                    className=f"text-{color}",
                ),

                
            ],
            className=f"border-{color} border-start border-5",

            
        ),
        className="text-center text-nowrap my-2 p-2",
    )

def make_pie_card(cur_week):
    
    change = nested_pie_chart(cur_week)    

    return dbc.Card(
        nested_pie_chart(cur_week)
    )


def nested_pie_chart(cur_week):

    # steps percentage
    #
    target_met = cur_week.activity_metric["Percentage of days met target"]
    not_met = 100 - target_met

    # average steps
    #
    steps = cur_week.activity_metric["Average step count"]
    step_percentage = steps / 2000 * 100
    step_neg = 100 - step_percentage

    if step_neg < 0:
        step_neg = 0

    # average activity
    #
    active = cur_week.activity_metric["Average activity time"]
    active_percentage = active / 20 * 100
    active_neg = 100 - active

    if active_neg < 0:
        active_neg = 0

    # Create subplots with 1 row and 1 column
    fig = make_subplots(rows=1, cols=1)

    fig.add_trace(
        go.Pie(values=[active_percentage, active_neg],
               #labels=['Reds','Blues'],
               domain={'x': [0.3, 0.7], 'y': [0.3, 0.7]},
               hole=0.25,
               direction='clockwise',
               sort=False,
               showlegend=False,
               textinfo='none',
               hoverinfo='none',
               marker={'colors':['rgba(163, 122, 194, 0.8)', 'rgba(77, 50, 98, 1)']}), #['#2756f2','#172657']
    )
        # Individual components (outer donut)
    fig.add_trace(
        go.Pie(values=[step_percentage, step_neg],
               #labels=['Medium Red','Light Red','Medium Blue','Light Blue'],
               domain={'x': [0.2, 0.8], 'y': [0.2, 0.8]},
  
               hole=0.5,
               direction='clockwise',
               sort=False,
               textinfo='none',
               hoverinfo='none',
               marker={'colors':['rgba(255, 179, 70, 1)','rgba(114, 89, 52, 1)']},
               showlegend=False),
    )

    fig.add_trace(
        # Individual components (outer donut)
        go.Pie(values=[target_met, not_met],
               #labels=['Medium Red','Light Red','Medium Blue','Light Blue'],
               domain={'x': [0.1, 0.9], 'y': [0.1, 0.9]},
              
               hole=0.75,
               direction='clockwise',
               sort=False,
               textinfo='none',
               hoverinfo='none',
               marker={'colors':['rgba(15, 125, 229, 0.8)','rgba(36, 69, 101, 0.8)']},
               showlegend=False),                    
               
    )

    fig.update_layout(
        margin=dict(t=0, l=0, r=0, b=0),
        height=350,
        width=350,
        #title_text="Nested Pie Charts",
    )

    return html.Div(dcc.Graph(figure=fig))
    

     
    # data = [# Portfolio (inner donut)
    #     go.Pie(values=[20,40],
    #            labels=['Reds','Blues'],
    #            domain={'x': [0.3, 0.7], 'y': [0.3, 0.7]},
    #            hole=0.25,
    #            direction='clockwise',
    #            sort=False,
    #            showlegend=False,
    #            textinfo='none',
    #            hoverinfo='none',
    #            marker={'colors':['#CB4335','#2E86C1']}),
    #     # Individual components (outer donut)
    #     go.Pie(values=[5,15,30,10],
    #            labels=['Medium Red','Light Red','Medium Blue','Light Blue'],
    #            domain={'x': [0.2, 0.8], 'y': [0.2, 0.8]},
    #            hole=0.5,
    #            direction='clockwise',
    #            sort=False,
    #            textinfo='none',
    #            hoverinfo='none',
    #            marker={'colors':['#EC7063','#F1948A','#5DADE2','#85C1E9']},
    #            showlegend=False),

    #     # Individual components (outer donut)
    #     go.Pie(values=[25,15,30,10],
    #            labels=['Medium Red','Light Red','Medium Blue','Light Blue'],
    #            domain={'x': [0.1, 0.9], 'y': [0.1, 0.9]},
    #            hole=0.75,
    #            direction='clockwise',
    #            sort=False,
    #            textinfo='none',
    #            hoverinfo='none',
    #            marker={'colors':['#EC7063','#F1948A','#5DADE2','#85C1E9']},
    #            showlegend=False),                    
               
    #            ]
    # return html.Div(dcc.Graph(figure=go.Figure(data=data)))
    