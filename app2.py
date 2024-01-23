from dash import Dash, html, dash_table, callback, Output, Input
from dash import dcc
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
from main_final import data_df
from l_general_data import general_data_layout
from l_well_data import well_data_layout
from general_data_callbacks import register_general_data_callbacks
from well_data_callbacks import register_well_data_callbacks
#importar data
df = data_df
first_year_available = df['FECHA'].dt.year.max()
tabs_layouts = {
    'tab1': general_data_layout,
    'tab2': well_data_layout,
}

# iniciar-crear la app
app = Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}], suppress_callback_exceptions=True)

# Definir el layout de la app
app.layout = html.Div([
    html.Div([
        html.Div([        
            html.Img(src=("assets/Artua-Wall-E-Wall-e.256.png"),
                      id='corona-image', 
                      style={'width': 'auto', 
                             'height': '100px', 
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
            ], className="two-half column", id="title"),

        html.Div([
            html.P('Last Updated: ' + str(df['FECHA'].iloc[0].strftime("%B %d, %Y")) + '  00:01 (UTC)',
                   style={'color': 'orange', "margin-bottom": "0px", 'fontSize': 10}),
                   ], className="one-third column", id='title1'),

            ], id="header", className="row flex-display", style={"margin-bottom": "0px"}),

    html.Div([
        dcc.Tabs(id='tabs', value='tab1', children=[
            dcc.Tab(label='Datos Generales', value='tab1'),
            dcc.Tab(label='Datos del Pozo', value='tab2'),
        ]),
        html.Div(id='tabs-content'),
    ])
])
html.Div(id='general-data-content')
html.Div(id='some-input', style={'display': 'none'})
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
    app.run(debug=True)