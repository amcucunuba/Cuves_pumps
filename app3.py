import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Img(src=app.get_asset_url(''),
                     id='corona-image',
                     style={})
                ],className="one-third column",
            ),
        html.Div([
                 html.Div([
                    html.H3("HOLA", style={"margin-bottom": "0px", 'color': 'white'}),
                    html.H5("Esto es un ensayo", style={"margin-top": "0px", 'color': 'white'}),
            ])
        ], className="one-half column", id="title"),

        html.Div([
            html.H6(
                    style={'color': 'orange'}),

        ], className="one-third column", id='title1'),

    ], id="header", className="row flex-display", style={"margin-bottom": "25px"}),

    html.Div([
        html.Div([
            html.H6(children='Comencemos',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

            html.P(f"hola",
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 40}
                   ),

            html.P('new:  ' + f"mi nombre es "
                   + 'angela',
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 15,
                       'margin-top': '-18px'}
                   )], className="card_container three columns",
        ),

        html.Div([
            html.H6(children='Vivo en Paris',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

            html.P(f"soy nutri",
                   style={
                       'textAlign': 'center',
                       'color': '#dd1e35',
                       'fontSize': 40}
                   ),

            html.P('y nounou',
                   style={
                       'textAlign': 'center',
                       'color': '#dd1e35',
                       'fontSize': 15,
                       'margin-top': '-18px'}
                   )], className="card_container three columns",
        ),

        html.Div([
            html.H6(children='También',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

            html.P(f"hija",
                   style={
                       'textAlign': 'center',
                       'color': 'green',
                       'fontSize': 40}
                   ),

            html.P('casi esposa',
                   style={
                       'textAlign': 'center',
                       'color': 'green',
                       'fontSize': 15,
                       'margin-top': '-18px'}
                   )], className="card_container three columns",
        ),

        html.Div([
            html.H6(children='Me gusta el ejercicio',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

            html.P(f" y soy colombiana",
                   style={
                       'textAlign': 'center',
                       'color': '#e55467',
                       'fontSize': 40}
                   ),

            html.P('decendiente de los muiscas',
                   style={
                       'textAlign': 'center',
                       'color': '#e55467',
                       'fontSize': 15,
                       'margin-top': '-18px'}
                   )], className="card_container three columns")

    ], className="row flex-display"),
])

if __name__ == '__main__':
    app.run(debug=True)
    