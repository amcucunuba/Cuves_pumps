from dash import *
import dash_bootstrap_components as dbc
from dash import dash_table 
from dash import callback
from dash.dependencies import Input, Output
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp

from ml_logic.main_final import data_df
from ml_logic.l_general_data import general_data_layout
from ml_logic.l_well_data import well_data_layout
from ml_logic.general_data_callbacks import register_general_data_callbacks
from ml_logic.well_data_callbacks import register_well_data_callbacks

#import data
df = data_df
first_year_available = df['FECHA'].dt.year.max()
tabs_styles = {
    "flex-direction": "row",
}
tab_style = {
    "padding": "2vh",
    "color": '#AEAEAE',
    "fontSize": '1.5vw',
    "backgroundColor": '#1f2c56',
    'border-bottom': '1px white solid',

}

tab_selected_style = {
    "fontSize": '1.5vw',
    "color": '#F4F4F4',
    "padding": "2vh",
    'fontWeight': 'bold',
    "backgroundColor": '#566573',
    'border-top': '1px white solid',
    'border-left': '1px white solid',
    'border-right': '1px white solid',
    'border-radius': '0px 0px 0px 0px',
}

tab_selected_style1 = {
    "fontSize": '1.5vw',
    "color": '#F4F4F4',
    "padding": "2vh",
    'fontWeight': 'bold',
    "backgroundColor": '#566573',
    'border-top': '1px white solid',
    'border-left': '1px white solid',
    'border-right': '1px white solid',
    'border-radius': '0px 0px 0px 0px',
}

tabs_layouts = {
    'tab1': general_data_layout,
    'tab2': well_data_layout,
}

# iniciar-crear la app
app: Dash = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}], 
                      suppress_callback_exceptions=True, 
                      external_stylesheets=[dbc.themes.BOOTSTRAP] )
server = app.server
# Definir el layout de la app
app.layout = html.Div([
    html.Div([
        html.Div([        
            html.Img(src=("assets/Artua-Wall-E-Wall-e.256.png"),
                      id='corona-image', 
                      style={'width': 'auto', 
                             'height': '90px', 
                             "margin-bottom": "10px",
                             'align-items': 'right',
                             }
                     ),
            ], className="one-third column"), 
        html.Div([
            html.H3("Electric Submersible Pumps", style={"margin-bottom": "0px", 
                                                          'color': 'white',
                                                          'text-align': 'center',
                                                          }),
            html.H3("Colombia", style={"margin-top": "0px", 'color': 'white'}),
            ], className="one-third column", id="title"),

        html.Div([
            html.P('Last Updated:   ' + str(df['FECHA'].iloc[0].strftime("%B %d, %Y")) + 
                   '  00:01 (UTC)',
                   style={'color': 'orange', "margin-bottom": "5px", 'fontSize': 10}),
                   ], className="one-third column", id='title1'),

            ], id="header", className="row flex-display", style={"margin-bottom": "0px"}),

    html.Div([
        dcc.Tabs(id='tabs', value='tab1', children=[
            dcc.Tab(label='General data', 
                    value='tab1', 
                    style = tab_style,
                    selected_style = tab_selected_style,), 
            dcc.Tab(label="Well's data", 
                    value='tab2', 
                    style = tab_style,
                    selected_style = tab_selected_style,),
        ], style = tabs_styles,),
        html.Div(id='tabs-content'),
    ]),
])

# Registro de los callbacks
register_general_data_callbacks(app)
register_well_data_callbacks(app)

# Callback principal para actualizar el contenido de las tabs
@app.callback(
    Output('tabs-content', 'children'),
    [Input('tabs', 'value')]
)
def update_tab_content(selected_tab):
    return tabs_layouts[selected_tab]

# Ejecutar la aplicación si este script es el principal
if __name__ == '__main__':
    app.run_server(debug=True, port=8080, use_reloader=False)