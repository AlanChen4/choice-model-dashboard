import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash


app = DjangoDash('SiteChoiceProb', add_bootstrap_links=True)

graph_style = {
    'height': '50%',
    'display': 'none',
}

app.layout = html.Div(children=[
    dcc.RadioItems(
        id='radio', 
        options=[
            {'label': 'Bubble Plot', 'value': 'bubble-plot'},
            {'label': 'Map Scatter Plot', 'value': 'map-scatter-plot'},
        ],
        value='bubble-plot',
    ),
    dcc.Graph(id='bubble-plot', figure=None, style=graph_style),
    dcc.Graph(id='map-scatter-plot', figure=None, style=graph_style),
])

@app.callback(
    Output('bubble-plot', 'style'),
    Input('radio', 'value')
)
def display_graphs(selected_value):
    if 'bubble-plot' == selected_value:
        return {'display': 'block'}
    return {'display': 'none'}


@app.callback(
    Output('map-scatter-plot', 'style'),
    Input('radio', 'value')
)
def display_graphs(selected_value):
    if 'map-scatter-plot' == selected_value:
        return {'display': 'block'}
    return {'display': 'none'}
