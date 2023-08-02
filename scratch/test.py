
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc

# Sample data
import pandas as pd
import numpy as np

np.random.seed(42)
data = pd.DataFrame({
    'X': np.random.rand(50),
    'Y': np.random.rand(50)
})

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Create the layout
app.layout = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H4("Responsive Plotly Express Graph", className="card-title"),
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(id="scatter-plot"),
                                md=8,
                                xs=12
                            ),
                            dbc.Col(
                                # dbc.FormGroup(
                                     [
                                        dbc.Label("Select Marker Size"),
                                        dcc.Slider(
                                            id="marker-size-slider",
                                            min=5,
                                            max=15,
                                            step=1,
                                            value=10,
                                            marks={i: str(i) for i in range(5, 16)},
                                        ),
                                    ],
                                #),
                                md=4,
                                xs=12,
                            ),
                        ],
                        align="center",
                    ),
                ]
            ),
            className="mb-4",
        )
    ],
    className="container mt-4",
)

# Create the callback to update the graph based on the slider input
@app.callback(
    Output("scatter-plot", "figure"),
    [Input("marker-size-slider", "value")]
)
def update_graph(marker_size):
    print(marker_size)
    # Update the scatter plot with the new marker size
    data = pd.DataFrame({
    'X': np.random.rand(50),
    'Y': np.random.rand(50)
    })
    fig = px.scatter(
        data,
        x='X',
        y='Y',
        title='Responsive Scatter Plot',
        labels={'X': 'X-axis', 'Y': 'Y-axis'},
        size_max=marker_size,
    )
    return fig

if __name__ == "__main__":
    app.run_server(debug=True, port=8051)
