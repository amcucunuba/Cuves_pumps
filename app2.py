from dash import Dash, html, dash_table, callback, Output, Input
from dash import dcc
import pandas as pd
import datetime
import plotly.express as px
from main_final import data_df

#importar data
df = data_df
# iniciar-crear la app
app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.Img(src='https://us.123rf.com/450wm/grgroup/grgroup1611/grgroup161100278/64919022-ic%C3%B4ne-de-la-tour-de-l-usine-de-p%C3%A9trole-sur-fond-blanc-illustration-vectorielle.jpg?ver=6',  
            width="90", height="70", 
            style = {'float':'right', 
                     'background-repeat': 'repeat',
                      'background-size': 'contain',
                            },),
        html.H1("CURVES PUMPS COLOMBIA", 
                style= {'textAlign': 'center',
                    'color': '#ffffff', 
                    'background-color': '#07083b',
                    'padding': '10px',
                   }),
    ]),
    
    html.Div(children=[
        html.Label(html.H2('Choisir le well'), style= {'margin-bottom': '0.67em'}),
        html.Hr(), 
        dcc.Dropdown(options=[{'label': well, 'value': well} for well in df['WELL'].unique()], 
                     id= 'pandas-dropdown-1', value= df['WELL'][0]),
        html.Div(id= 'pandas-output-container-1'),
        ]),

    html.Hr(),
    html.Div(
    dcc.Graph(id='graph'),
        # dcc.Slider(
        #     df['FECHA'].min(),
        #     df['FECHA'].max(),
        #     step=None,
        #     id='FECHA--slider',
        #     value=df['FECHA'].max(),
        #     marks={float(fecha): fecha for fecha in df['FECHA'].unique()},
        # ),
    ),

    html.Div(
     dash_table.DataTable(
            id='data-table', 
            style_header={'textAlign': 'center',
            'backgroundColor': '#d2d2d2',
            'color': 'black',
            'fontWeight': 'bold'},

            style_data= {'color':'black', 'backgroundColor': '#ffffff'},
            style_data_conditional=[{
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(220, 220, 220)',}],
            columns=[{'name':'WELL', 'id':'WELL'}, {'name':'FECHA', 'id':'FECHA'} , {'name':'FRECUENCIA', 'id':'FRECUENCIA'},
                     {'name': 'PF IN VSD','id':'PF IN VSD'}, {'name':'PF OUT VSD','id':'PF OUT VSD' }, 
                     {'name': 'VOL MTR A','id':'VOL MTR A' }, {'name': 'VOL MTR B','id': 'VOL MTR B'},
                     {'name': 'VOL MTR C','id':'VOL MTR C' }, {'name':'RED KVA' ,'id':'RED KVA' }, 
                     {'name': 'RED KW','id':'RED KW' }, {'name': 'KVA VSD' ,'id':'KVA VSD' },
                     {'name': 'KVA SUT','id': 'KVA SUT'}, {'name': 'AMP MOTOR' ,'id':'AMP MOTOR'}, 
                     {'name': '% LOAD MTR','id':'% LOAD MTR'}, {'name': 'PIP (psi)','id':'PIP (psi)'},
                     {'name': 'T Motor (F)', 'id':'T Motor (F)'}
                     ], 
                     
            ),
        ),
])
@app.callback(
    Output(component_id='data-table', component_property= 'data'),
    Output(component_id='graph', component_property= 'figure'),
    [Input(component_id='pandas-dropdown-1', component_property= 'value')]
)
def update_table(selected_well):
    filtered_df = df[df['WELL'] == selected_well]
    return filtered_df.to_dict('records'), update_graph_line(selected_well)

def update_graph_line(selected_well):
    fig = px.line(df[df['WELL'] == selected_well],  x="FRECUENCIA", y="VOL MTR C")
    return fig
# puedo cambiar el html de salida asignando un numero de 4 cifras, sin comas ni puntos
if __name__ == '__main__':
    app.run(debug=True)

