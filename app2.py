from dash import Dash, html, dash_table, callback, Output, Input
from dash import dcc
import pandas as pd
from datetime import datetime
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
        html.H1("Electric Submersible Pumps Colombia", 
                style= {'textAlign': 'center',
                    'color': '#ffffff', 
                    'background-color': '#07083b',
                    'padding': '10px',
                   }),
    ]),
    
    html.Div(children=[
        html.Label(html.H2('Choose the well'), style= {'margin-bottom': '0.67em'}),
        html.Hr(), 
        dcc.Dropdown(options=[{'label': well, 'value': well} for well in df['WELL'].unique()], 
                     id= 'pandas-dropdown-1', value= df['WELL'][0]),
        html.Div(id= 'pandas-output-container-1'),
        ]),

    html.Hr(),
    html.Div([
    dcc.Graph(id='graph'),
        dcc.RangeSlider(
            min= df['FECHA'].min().year,
            max= df['FECHA'].max().year,
            step= None,
            id='FECHA--slider',
            marks={str(year): str(year) for year in range(df['FECHA'].min().year, df['FECHA'].max().year + 1)},
            value=[df['FECHA'].min().year, df['FECHA'].max().year],
        ),
    ]),

    html.Div(children=[
        html.Label(html.H2('Historial de mediciones'), style= {'margin-bottom': '0.45em'})
    ]),

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
    [Input(component_id='pandas-dropdown-1', component_property= 'value'),
     Input(component_id='FECHA--slider', component_property='value')]
)
def update_table(selected_well, year_range):
    filtered_df = df[df['WELL'] == selected_well]
    filtered_df = filtered_df[(filtered_df['FECHA'].dt.year >= year_range[0]) & (filtered_df['FECHA'].dt.year <= year_range[1])]
    
    # Llamar a la función para actualizar el gráfico
    fig = update_graph_line(filtered_df, selected_well, year_range)
    return filtered_df.to_dict('records'), fig

def update_graph_line(filtered_df, selected_well, year_range):
    # lista_variables_y = ['FRECUENCIA', 'AMP MOTOR', 'KVA VSD' ],
    fig = px.line(filtered_df, x='FECHA', y='AMP MOTOR', 
                  title=f'Graph for {selected_well} in the range of years {year_range[0]} - {year_range[1]}')
    return fig

if __name__ == '__main__':
    app.run(debug=True)

