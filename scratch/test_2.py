import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go


data = [# Portfolio (inner donut)
        go.Pie(values=[20,40],
               labels=['Reds','Blues'],
               domain={'x': [0.3, 0.7], 'y': [0.3, 0.7]},
               hole=0.25,
               direction='clockwise',
               sort=False,
               marker={'colors':['#CB4335','#2E86C1']}),
        # Individual components (outer donut)
        go.Pie(values=[5,15,30,10],
               labels=['Medium Red','Light Red','Medium Blue','Light Blue'],
               domain={'x': [0.2, 0.8], 'y': [0.2, 0.8]},
               hole=0.45,
               direction='clockwise',
               sort=False,
               marker={'colors':['#EC7063','#F1948A','#5DADE2','#85C1E9']},
               showlegend=False),

        # Individual components (outer donut)
        go.Pie(values=[25,15,30,10],
               labels=['Medium Red','Light Red','Medium Blue','Light Blue'],
               domain={'x': [0.1, 0.9], 'y': [0.1, 0.9]},
               hole=0.8,
               direction='clockwise',
               sort=False,
               marker={'colors':['#EC7063','#F1948A','#5DADE2','#85C1E9']},
               showlegend=False),
                     
               
               ]

# Run Dash app
app = dash.Dash()
app.layout = html.Div(dcc.Graph(figure=go.Figure(data=data, layout={'title':'Nested Pie Chart'})))

if __name__ == '__main__':
    app.run_server(debug=True, port=8052)