import plotly.express as px
import dash_bootstrap_components as dbc
import dash
from dash import html, dcc
from dash.dependencies import Output, Input
from utils.utils_class import read_dat, extract_dates
import pandas as pd
from app import app

# global variables
#
fname = "https://raw.githubusercontent.com/nabila-shawki/multi-tab-healthdata/main/data/week_4.csv"
start_date = pd.to_datetime('2023-06-05')
end_date = pd.to_datetime('2023-07-30')
dates = pd.date_range(start='2023-06-05', end='2023-07-30', freq='D')
target_count = 2000 # steps
target_move = 20 # minutes

# get the filtered dat
#
dat = read_dat(fname, start_date, end_date, target_count)
print(dat.filtered_df.shape)

# the datepicker
#
dates = dcc.DatePickerRange(
        id='date-picker',
        min_date_allowed=min(dates),
        max_date_allowed=max(dates),
        initial_visible_month=min(dates),
        start_date=str(min(dates)),
        end_date=str(max(dates)),
        persistence=True,
        persisted_props=['start_date', 'end_date'],
        persistence_type='session'

    ),

# create a layout
#
range_layout = dbc.Container(
    [
        # the calendar
        #
        dbc.Row([
                dbc.Col(
                    html.H4("Select Dates"),
                    width="auto",
                    
                    className="text_left"
                ),
                dbc.Col(
                    dates,
                    width="auto",
                    className="text_left"
                ),
 
                # dbc.Col(
                #     html.H4("End Date"),
                #     width="auto",
                    
                #     className="text_left"
                # ),
                # dbc.Col(
                #     end_date,
                #     width="auto",
                # ),
            ],
            justify="left",
            align="center"
            #className="g-0",
        ),

        # The Pie chart for step target
        #     
        dbc.Row([
            dbc.Col(
                dcc.Graph(                    
                    id='pie-chart',
                    responsive=True
                ),
                width={"size": 4},
            ),

            dbc.Col(
                
                # Average steps
                #
                [
                dbc.Row(html.Div(id='range-progress-bar')),
                dbc.Row(html.Div(id='range-move-progress-bar')),

                # # Average move minutes
                # #
                # dbc.Row([
                #     dbc.Col(html.H4("Average Movement Duration"), width="2"),

                # ]),

                # # Average maximum heart rate
                # #
                # dbc.Row([
                #     dbc.Col(html.H4("Average Heart Rate"), width="2"),
                # ]),
                ]
            ),
        ],
            justify="left",
            align = "middle",
            className="mb-4",
        ),


    ],
    fluid=True,
)


@app.callback(
    # dash.dependencies.Output('pie-chart', 'figure'),
    # [dash.dependencies.Input('start-date-picker', 'date'),
    #  dash.dependencies.Input('end-date-picker', 'date')]
    Output('pie-chart', 'figure'),
    Output('range-progress-bar', 'children'),
    Output('range-move-progress-bar', 'children'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date')  
)
def update_pie_chart(start_date, end_date):

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    if end_date < start_date:
        raise dash.exceptions.PreventUpdate

    df = dat.filtered_df
    filtered_df = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]
    #print(filtered_df)
    value_counts = filtered_df['Target Met'].value_counts()
    value_counts = value_counts.sort_index(ascending=False)
    total_days = len(filtered_df.index)
    target_met = total_days - value_counts[0]

    print(total_days, target_met)
    fig = px.pie(
        value_counts,
        values=value_counts.values,
        names=value_counts.index,
        hole=0.7,
        color=value_counts.index,
        color_discrete_map={  0: '#cccccc', 1: '#2E86C1'},
        labels={'label': 'Value'},
         
        
    )
    # hiding legend in pyplot express.
    fig.update_traces(showlegend=False,
                      textinfo='none',
                      sort=False,
                      hoverinfo="skip",
                      hovertemplate=None,
                      )

    fig.update_layout(
        autosize=True,
        margin=dict(t=20, b=20, l=20, r=20),
        showlegend=False,
        annotations=[
            dict(
                #text= f"<span style='font-size: 30px; color: #5DADE2; font-weight: bold; font-family: Arial;'>{target_met}/{total_days}</span><br>",
                text=f"<span style='font-size: 20px; color: #5DADE2; font-weight: bold; font-family: Arial;'>Step Target Met</span><br><br>"
                    f"<span style='font-size: 30px; color: #5DADE2; font-weight: bold; font-family: Arial;'>{target_met}/{total_days}</span><br>"
                    f"<span style='font-size: 20px; color: #5DADE2; font-weight: bold; font-family: Arial;'>Days</span>",
                showarrow=False,
                font=dict(size=16),
                x=0.5,
                y=0.5
            )
        ],
        
    )

    # Progress bar
    step_count_avg = filtered_df['Step count'].mean()
    progress_percent = (step_count_avg / target_count) * 100
    progress_bar = dbc.Container(
        [
            dbc.Row([
                dbc.Col(html.H4(f"Avg. Step Count: {step_count_avg:.0f}/{target_count}"), width="auto", align="left"),
            # ),
            # dbc.Row(
                dbc.Col(
                    dbc.Progress(value=progress_percent, style={'height': '30px'}),
                    className="mb-2",
                )]
            ),
        ]
    )

    # Progress bar
    move_min_avg = filtered_df['Move Minutes count'].mean()
    move_min_percent = (move_min_avg / target_move) * 100
    move_progress_bar = dbc.Container(
        [
            dbc.Row([
                dbc.Col(html.H4(f"Avg. Movement Duration: {move_min_avg:.0f}/{target_move}"), width="auto", align="left"),
            # ),
            # dbc.Row(
                dbc.Col(
                    dbc.Progress(value=move_min_percent, style={'height': '30px'}),
                    className="mb-2",
                )]
            ),
        ]
    )
    return fig, progress_bar, move_progress_bar

# # layout of second (trends) tab ******************************************
# range_layout = html.Div([
#     dbc.Row([
#         dbc.Col([
#             html.H2("More Twitter analysis to come...")
#         ], width=12)
#     ]),
#     dbc.Row([
#         dbc.Col([
#             dcc.Graph(id='scatter', figure={})
#         ], width=6),
#         dbc.Col([
#             dcc.Graph(id='scatter2', figure={})
#         ], width=6)
#     ])
# ])