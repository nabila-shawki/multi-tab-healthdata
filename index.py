import dash_bootstrap_components as dbc
import dash
from dash import html, dcc
from dash.dependencies import Output, Input, State
from app import app

# Connect to the layout and callbacks of each tab
from daily import daily_layout
from weekly import weekly_layout
from select_range import range_layout


# our app's Tabs *********************************************************
app_tabs = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="Weekly", tab_id="tab-weekly", labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
                dbc.Tab(label="Daily", tab_id="tab-daily", labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
                dbc.Tab(label="Select Range", tab_id="tab-range", labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
            ],
            id="tabs",
            active_tab="tab-weekly",
        ),
    ], className="mt-3"
)

app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("The Remote Monitoring Dashboard",
                            style={"textAlign": "center"}), width=12)),
    html.Hr(),
    dbc.Row([
        dbc.Col(html.H4("Participant: RM-01")),
        dbc.Col(html.H4("Birth Year: 1964")),
    ],
    className="mb-3"
    ),
    html.Hr(),
    dbc.Row(dbc.Col(app_tabs, width=12), className="mb-3"),
    html.Div(id='content', children=[])

])

@app.callback(
    Output("content", "children"),
    [Input("tabs", "active_tab")]
)
def switch_tab(tab_chosen):
    if tab_chosen == "tab-weekly":
        return weekly_layout
    elif tab_chosen == "tab-daily":
        return daily_layout
    elif tab_chosen == "tab-range":
        return range_layout
    return html.P("This shouldn't be displayed for now...")



if __name__=='__main__':
    app.run_server(debug=True)
