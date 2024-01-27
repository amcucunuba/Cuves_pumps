from dash import Dash, html, dash_table, callback, Output, Input
from dash import dcc
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
from main_final import data_df

df = data_df
first_year_available = df['FECHA'].dt.year.max()
app = Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],suppress_callback_exceptions=True)

well_data_layout = html.Div([
    html.H2("Well's data", style={'color': 'white','margin-top': '10px',}),
    html.Div([
            html.Div([
            html.Div([
                html.P('Choose the well         .',  
                        style={'color': 'white',
                            'fontSize': 22,
                            'margin-top': '20px'},
                            className = 'drop_down_list_title'
                        ), 
                dcc.Dropdown(options=[{'label': well, 'value': well} for well in df['WELL'].unique()], 
                            id='pandas-dropdown-1', 
                            value=df['WELL'][0], 
                            style = {'display': 'inline-block',
                                    "margin-bottom": "15px"},
                            className= 'drop_down_list'),], 
                            className = 'title_drop_down_list'),
                        ]),
                html.Div(id='pandas-output-container-1'),
                    ], className = "title_and_drop_down_list", style={"margin-bottom": "10px"}), 
    html.Div([
        html.Div([
            html.P(id='card-container-1-value',
                    style={'textAlign': 'center',
                        'color': '#dd1e35',
                        'fontSize': 30,
                        'margin-top': '20px'
                        }
                    ),
            html.P(children='Frecuencia',
                        style={'textAlign': 'center',
                            'color': 'white',
                            'fontSize': 18,
                            'margin-top': '-18px'
                            }
                        ),
            ], className="create_container two columns",
            ),
            html.Div([
                    html.P(id='card-container-5-value',
                    style={
                        'textAlign': 'center',
                        'color': 'orange',
                        'fontSize': 30, 
                        'margin-top': '20px'}
                    ),
                    html.P(children='Active power',
                        style={'margin-top': '-18px',
                            'textAlign': 'center',
                            'color': 'white',
                            'fontSize': 18}
                        ),
                ], className="create_container two columns",
                    ),
            html.Div([
                html.P(id='card-container-2-value',
                    style={'textAlign': 'center',
                        'color': 'green',
                        'fontSize': 30,
                            'margin-top': '20px'}
                        ),
                html.P(children='Apparent power',
                        style={'textAlign': 'center',
                            'color': 'white',
                            'fontSize': 18,
                        'margin-top': '-18px'}
                    ),
                ], className="create_container two columns",
                        ),
            html.Div([
                html.P(id='card-container-3-value',
                    style={
                        'textAlign': 'center',
                        'color': '#dd611e',
                        'fontSize': 30,
                            'margin-top': '20px'}
                        ),
                html.P(children='Averge motor voltage',
                        style={'textAlign': 'center',
                            'color': 'white',
                            'fontSize': 14,
                        'margin-top': '-18px'}
                    ),
            ], className="create_container two columns",
                        ),

            html.Div([
                html.P(id='card-container-4-value',
                    style={
                        'textAlign': 'center',
                        'color': '#e55467',
                        'fontSize': 30, 
                            'margin-top': '20px'}
                        ),
                html.P(children='Motor current',
                        style={
                            'textAlign': 'center',
                            'color': 'white',
                            'fontSize': 18,
                        'margin-top': '-18px'}
                    ),
                ], className="create_container two columns",
                    ),
                ],className="row flex-display", style={"margin-bottom": "5px"}),
    html.Div([    
            html.Div([
                dcc.Graph(id='graph', className="create_container1 twelve columns"),
                ], className="row flex-display" ),
            html.Div([
                dcc.RangeSlider(
                        max=df['FECHA'].max().year,
                        step=None,
                        id='FECHA--slider',
                        marks={str(year): str(year) for year in range(df['FECHA'].min().year, df['FECHA'].max().year + 1)},
                        value=[df['FECHA'].min().year, df['FECHA'].max().year],
                        min=df['FECHA'].min().year,
                        className="create_container1 twelve columns",
                        ),
                    ], className="row flex-display" ),
                    ]),
    html.Div([
            html.Div([
                html.H5('Measurement track record ', 
                        style={'margin-bottom': 0, 
                            'color': 'white'}),
                html.P(id='output_container', children=[], 
                        style={'margin-bottom': 0, 
                                'color': 'white'}),
                    html.Div([
                        dash_table.DataTable(
                        id='data-table', 
                        style_table={'width': '100%',
                                    },
                        style_header={'textAlign': 'center',
                                    'backgroundColor': 'rgb(10, 10, 10)',
                                    'color': 'white',
                                    'fontWeight': 'bold',
                                    'font-family': 'Arial',
                                    'fontSize': 12
                                    },
                        style_data={'backgroundColor': 'rgb(50, 50, 50)',
                                    'color': 'white', 
                                    'font-family': 'Arial',
                                    'fontSize': 12},
                        style_data_conditional=[{'if': {'row_index': 'odd'},
                                            'backgroundColor': 'rgb(80, 80, 80)',
                                            }],
                        columns=[{'name':'WELL', 'id':'WELL'},
                                {'name': 'FECHA', 'id': 'FECHA', 'type': 'datetime'},
                                {'name':'FRECUENCIA', 'id':'FRECUENCIA'},
                                {'name': 'PF IN VSD','id':'PF IN VSD'}, {'name':'PF OUT VSD','id':'PF OUT VSD'}, 
                                {'name': 'VOL MTR A','id':'VOL MTR A'}, {'name': 'VOL MTR B','id': 'VOL MTR B'},
                                {'name': 'VOL MTR C','id':'VOL MTR C'}, {'name':'RED KVA' ,'id':'RED KVA'}, 
                                {'name': 'RED KW','id':'RED KW'}, {'name': 'KVA VSD' ,'id':'KVA VSD'},
                                {'name': 'KVA SUT','id': 'KVA SUT'}, {'name': 'AMP MOTOR' ,'id':'AMP MOTOR'}, 
                                {'name': '% LOAD MTR','id':'% LOAD MTR'}, {'name': 'PIP (psi)','id':'PIP (psi)'},
                                {'name': 'T Motor (F)', 'id':'T Motor (F)'
                                }],  
                                )
                ], className='table_style'),
                            ], className="create_container1 twelve columns"),
                            ],className = "row flex-display",)
 ])