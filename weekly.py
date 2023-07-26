import plotly.express as px
import dash_bootstrap_components as dbc
from utils.AndroidDat import AndroidDat
from utils.utils_class import read_dat, extract_dates
import dash
from dash import html, dcc
from dash.dependencies import Output, Input, State
import pandas as pd
from app import app

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

# # Save DataFrame to a CSV file
# dat.filtered_df.to_csv('data.csv', index=False)

# get the weeks
#
week_list = get_week_info(dat.filtered_df)
print(week_list)

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
            # [
            #     dbc.Col(
            #         [
            #             html.Button(
            #                 id="hit-button",
            #                 children="Submit",
            #                 style={"background-color": "blue", "color": "white"},
            #             )
            #         ],
            #         width=2,
            #     )
            # ],
            # className="mt-2",
        ),
        dbc.Row(
            [
                dbc.Col([dcc.Graph(id="weekly-steps", figure={})], width=4),
                
                dbc.Col(

                    # Average steps
                #
                [
                dbc.Row(html.Div(id='progress-bar')),
                dbc.Row(html.Div(id='move-progress-bar')),
                dbc.Row(html.Div(id='heart-rate')),

                
                #dbc.Row(html.Div(id='avg-weight')),
                ],
                style = {'margin-left':'7px', 'margin-top':'100px'} 

                )

            ],
            
        ),
        dbc.Row(
            [
                # dbc.Col(
                #     [
                #         html.P(
                #             id="notification",
                #             children="",
                #             style={"textAlign": "center"},
                #         )
                #     ],
                #     width=12,
                # )
            ]
        ),
    ]
)


# # callback for making the plots
#  
@app.callback(
    Output(component_id="weekly-steps", component_property="figure"),
    Output('progress-bar', 'children'),
    Output('move-progress-bar', 'children'),
    Output('heart-rate', 'children'),
    Input(component_id="week-dropdown", component_property="value"),
    #State(component_id="count-mentions", component_property="value"),
    #State(component_id="input-handle", component_property="value"),
)
def display_value(week_num):

    # long_df = px.data.medals_long()
    # scatter_fig = px.bar(long_df, x="nation", y="count", color="medal", title="Long-Form Input")

    # get the dates
    #
    start_date, end_date = extract_dates(week_num)
    print(start_date, end_date)

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
                text=f"<span style='font-size: 20px; font-weight: bold; '>Step Target Met</span><br><br>"
                    f"<span style='font-size: 30px;  font-weight: bold;'>{target_met}/{total_days}</span><br>"
                    f"<span style='font-size: 20px;  font-weight: bold; font-family: Arial;'>Days</span>",
                showarrow=False,
                font=dict(size=16),
                x=0.5,
                y=0.5
            )
        ],
        
    )


    # average step counts
    #
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

    # average move minutes
    #
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

    # heart rate
    #
    max_hr = filtered_df['Max heart rate (bpm)'].mean()
    min_hr = filtered_df['Min heart rate (bpm)'].mean()
   
    heart_rate = dbc.Container(
        [
            dbc.Row([
                dbc.Col(html.H4(f"Max/Min Heart Rate (bpm): {max_hr:.0f}/{min_hr:.0f}"), width="auto", align="left"),
            # ),
            # dbc.Row(
                # dbc.Col(
                #     dbc.Progress(value=move_min_percent, style={'height': '30px'}),
                #     className="mb-2",
               # )
                ]
            ),
        ]
    )


    return fig, progress_bar, move_progress_bar, heart_rate
