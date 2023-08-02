import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go

# Sample data (you can replace this with your data)
systolic_value = 120
diastolic_value = 80

# Initialize the Dash app
app = dash.Dash(__name__)

# Create the layout
app.layout = html.Div(
    [
        html.H1("Blood Pressure Gauge Chart"),
        html.Div(
            [
                dcc.Graph(id="blood-pressure-gauge"),
                html.Div(
                    [
                        html.Label("Systolic (mmHg)"),
                        dcc.Input(
                            id="systolic-input",
                            type="number",
                            value=systolic_value,
                        ),
                        html.Label("Diastolic (mmHg)"),
                        dcc.Input(
                            id="diastolic-input",
                            type="number",
                            value=diastolic_value,
                        ),
                    ],
                    style={"margin": "20px"},
                ),
            ],
            style={"display": "flex", "flexDirection": "row"},
        ),
    ],
    style={"textAlign": "center"},
)

# Create the callback to update the gauge chart based on user input
@app.callback(
    Output("blood-pressure-gauge", "figure"),
    [
        Input("systolic-input", "value"),
        Input("diastolic-input", "value"),
    ],
)
def update_gauge_chart(systolic, diastolic):
    # Create a gauge chart trace for systolic
    systolic_trace = go.Indicator(
        mode="gauge+number",
        value=systolic,
        title={"text": "Systolic (mmHg)"},
        domain={"x": [0, 0.5], "y": [0, 1]},
        gauge={"axis": {"range": [None, 200]}, "bar": {"color": "red"}},
    )

    # Create a gauge chart trace for diastolic
    diastolic_trace = go.Indicator(
        mode="gauge+number",
        value=diastolic,
        title={"text": "Diastolic (mmHg)"},
        domain={"x": [0.5, 1], "y": [0, 1]},
        gauge={"axis": {"range": [None, 150]}, "bar": {"color": "blue"}},
    )

    # Create the figure with both traces
    fig = go.Figure([systolic_trace, diastolic_trace])
    fig.update_layout(
        title="Blood Pressure Gauge Chart",
        grid=dict(rows=1, columns=2),
    )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True, port=8052)
