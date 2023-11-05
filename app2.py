from dash import Dash, html, dash_table, callback, Output, Input
from dash import dcc
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from main_final import data_df

#importar data
df = data_df
df_deptos = pd.read_csv('deptos.csv', delimiter=';', encoding='latin-1')


# iniciar-crear la app
app = Dash(__name__)

banner_style = {
    'background-color':'#07083b',
    'padding': '10px',
    'color': 'white',
    'display': 'flex',
    'align-items': 'center', 
    'textAlign': 'rigth',
    'color': '#ffffff', 
    'height': '60px',
    'justify-content': 'space-between',  # Para alinear la imagen a la derecha
    'justify-items': 'center',
    }

# Estilo de la imagen
image_style = {'width': '90px',
    'height': '70px',}

app.layout = html.Div([
    html.Div([
        html.H1("Electric Submersible Pumps Colombia", 
                style= {'margin': '0'}
               ),        
            html.Img(src='https://us.123rf.com/450wm/grgroup/grgroup1611/grgroup161100278/64919022-ic%C3%B4ne-de-la-tour-de-l-usine-de-p%C3%A9trole-sur-fond-blanc-illustration-vectorielle.jpg?ver=6',
            style= image_style,
                ),
            ],      
            style=banner_style),
    
    html.Div([
        dcc.Tabs([
            dcc.Tab(label='Predictive', children=[
                html.Div([
                    html.Label(html.H2('Choose the well'), style={'margin-bottom': '0.67em'}),
                    html.Hr(), 
                    dcc.Dropdown(options=[{'label': well, 'value': well} for well in df['WELL'].unique()], 
                                id='pandas-dropdown-1', value=df['WELL'][0]),
                    html.Div(id='pandas-output-container-1'),
                ]),
                html.Hr(),
                dcc.Graph(id='graph'),
                dcc.RangeSlider(
                    max=df['FECHA'].max().year,
                    step=None,
                    id='FECHA--slider',
                    marks={str(year): str(year) for year in range(df['FECHA'].min().year, df['FECHA'].max().year + 1)},
                    value=[df['FECHA'].min().year, df['FECHA'].max().year],
                    min=df['FECHA'].min().year,
                ),
                html.Div([
                    html.Label(html.H2('Historial de mediciones'), style={'margin-bottom': '0.45em'}),
                ]),
                dash_table.DataTable(
                    id='data-table', 
                    style_header={'textAlign': 'center',
                                'backgroundColor': '#d2d2d2',
                                'color': 'black',
                                'fontWeight': 'bold'},
                    style_data={'color':'black', 'backgroundColor': '#ffffff'},
                    style_data_conditional=[{
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(220, 220, 220)',
                    }],
                    columns=[{'name':'WELL', 'id':'WELL'}, {'name':'FECHA', 'id':'FECHA'}, {'name':'FRECUENCIA', 'id':'FRECUENCIA'},
                            {'name': 'PF IN VSD','id':'PF IN VSD'}, {'name':'PF OUT VSD','id':'PF OUT VSD'}, 
                            {'name': 'VOL MTR A','id':'VOL MTR A'}, {'name': 'VOL MTR B','id': 'VOL MTR B'},
                            {'name': 'VOL MTR C','id':'VOL MTR C'}, {'name':'RED KVA' ,'id':'RED KVA'}, 
                            {'name': 'RED KW','id':'RED KW'}, {'name': 'KVA VSD' ,'id':'KVA VSD'},
                            {'name': 'KVA SUT','id': 'KVA SUT'}, {'name': 'AMP MOTOR' ,'id':'AMP MOTOR'}, 
                            {'name': '% LOAD MTR','id':'% LOAD MTR'}, {'name': 'PIP (psi)','id':'PIP (psi)'},
                            {'name': 'T Motor (F)', 'id':'T Motor (F)'},
                    ],
                ),
            ]),
        dcc.Tab(label='Maps',  
                style = {
                    'borderBottom': '1px solid #c21010',
                    'padding': '5px',
                    'backgroundColor': '#119DFF',
                    'fontWeight': 'bold',
                    'font-size': '30px',
                    },
                children=[
            html.Div([
                html.Div([
                    html.H4('Ubicacion de pozos'),
                ]),
                dcc.Dropdown(id="slct_state",
                            options=[{'label': state, 'value': state} for state in df_deptos['DEPARTAMENTO'].unique()],
                            multi=False,
                            value= df_deptos['DEPARTAMENTO'][0],
                            ),

                html.Div(id='output_container', children=[]),
                html.Br(),

                dcc.Graph(id='my_dept_map', figure={})
                
                ]),
            ]),
        ]),
    ]),

])

@app.callback(
    Output(component_id='data-table', component_property= 'data'),
    Output(component_id='graph', component_property= 'figure'),
    [Input(component_id='pandas-dropdown-1', component_property= 'value'),
     Input(component_id='FECHA--slider', component_property='value')]
)
def update_table(selected_well, year_range):
    #Primer filtro del df de acuerdo con el pozo seleccionado 
    filtered_df = df[df['WELL'] == selected_well]
    
    #2do. filtro del df de acuerdo con la fecha seleccionada
    filtered_df = filtered_df[(filtered_df['FECHA'].dt.year >= year_range[0]) & (filtered_df['FECHA'].dt.year <= year_range[1])]
    
    # Llamar a la función para actualizar el gráfico
    fig = update_graph_line(filtered_df, selected_well, year_range)
    return filtered_df.to_dict('records'), fig

def update_graph_line(filtered_df, selected_well, year_range):
    #Filtar el dfde acuerdo al pozo seleccionado
    filtered_df = filtered_df[(filtered_df['FECHA'].dt.year >= year_range[0]) & (filtered_df['FECHA'].dt.year <= year_range[1])]
    #Filtro de fecha, min y max de acuerdo al pozo, para ajustar en el titulo de la gráfica
    years_range = (filtered_df['FECHA'].min().year, filtered_df['FECHA'].max().year)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=filtered_df['FECHA'], 
                             y=filtered_df['FRECUENCIA'],
                             name="FRECUENCIA", 
                             mode='lines+markers',
                             marker=dict(size=4),
                             ))
    
    fig.add_trace(go.Scatter(x=filtered_df['FECHA'], 
                             y=filtered_df['VOL MTR A'], 
                             name="VOL MTR A", 
                             yaxis="y2", 
                             mode='lines+markers',
                             ))

    fig.add_trace(go.Scatter(x=filtered_df['FECHA'], 
                             y=filtered_df['KVA VSD'], 
                             name="KVA VSD", 
                             yaxis="y3", 
                             mode='lines+markers',
                             ))
    
    fig.add_trace(go.Scatter(x=filtered_df['FECHA'], 
                             y=filtered_df['PF OUT VSD'], 
                             name="PF OUT VSD", 
                             yaxis="y4", 
                             mode='lines+markers',
                             ))

    fig.add_trace(go.Scatter(x=filtered_df['FECHA'], 
                             y=filtered_df['PF IN VSD'], 
                             name="PF IN VSD", 
                             yaxis="y5", 
                             mode='lines+markers',
                             ))

    fig.add_trace(go.Scatter(x=filtered_df['FECHA'], 
                             y=filtered_df['VOL MTR B'], 
                             name="VOL MTR B", 
                             yaxis="y6", 
                             mode='lines+markers',
                             ))
    
    fig.add_trace(go.Scatter(x=filtered_df['FECHA'], 
                             y=filtered_df['VOL MTR C'], 
                             name="VOL MTR C", 
                             yaxis="y7", 
                             mode='lines+markers',
                             ))
    
    fig.add_trace(go.Scatter(x=filtered_df['FECHA'], 
                             y=filtered_df['RED KVA'], 
                             name="RED KVA", 
                             yaxis="y8", 
                             mode='lines+markers',
                             ))
    
    fig.add_trace(go.Scatter(x=filtered_df['FECHA'], 
                             y=filtered_df['RED KW'], 
                             name="RED KW", 
                             yaxis="y9", 
                             mode='lines+markers',
                             ))

    fig.add_trace(go.Scatter(x=filtered_df['FECHA'], 
                             y=filtered_df['KVA SUT'], 
                             name="KVA SUT", 
                             yaxis="y10", 
                             mode='lines+markers',
                             ))

    fig.update_layout(title=f'Graph for {selected_well} in the range of years {years_range}',
        xaxis_title='FECHA',
        yaxis_title='Valores',
        yaxis2=dict(
            title="yaxis2 title",
            overlaying="y",
            side="right",
             ),
        yaxis3=dict(
            title="yaxis3 title",
            overlaying="y", 
            anchor="free",
            autoshift=True,
             ),
        yaxis4=dict(
            title="yaxis4 title",
            overlaying="y", 
            anchor="free",
            side="right",
             ),
        yaxis5=dict(
            title="yaxis5 title",
            overlaying="y", 
            anchor="free",
            autoshift=True,
             ),
        yaxis6=dict(
            title="yaxis6 title",
            overlaying="y", 
            anchor="free",
            autoshift=True,
             ),
        yaxis7=dict(
            title="yaxis7 title",
            overlaying="y", 
            anchor="free",
            autoshift=True,
             ),
        yaxis8=dict(
            title="yaxis8 title",
            overlaying="y", 
            anchor="free",
            autoshift=True,
             ),
        yaxis9=dict(
            title="yaxis9 title",
            overlaying="y", 
            anchor="free",
            autoshift=True,
             ),
        yaxis10=dict(
            title="yaxis10 title",
            overlaying="y", 
            anchor="free",
            autoshift=True,
             ),
        template= 'ggplot2',
        )
    return fig

@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_dept_map', component_property='figure')],
    [Input(component_id='slct_state', component_property='value')]
)
def update_graph(option_slctd):
    container = "The year chosen by user was: {}".format(option_slctd)
    
    color_mapping = {
    "Act": "green",
    "No_act": "red",}

    fig = go.Figure(go.Scattermapbox(
        lat=df_deptos['LATITUD'],
        lon=df_deptos['LONGITUD'],
        mode='markers',
        text=df_deptos['DEPARTAMENTO'],  # Esto configura el texto en la etiqueta emergente
        hovertext=df_deptos['DEPARTAMENTO'] + '<br>'  + df_deptos['ACTIVIDAD'],
        marker= go.scattermapbox.Marker(
            size=9,
            color=[color_mapping[act] for act in df_deptos['ACTIVIDAD']]
        ),
    ))
    
    fig.update_layout(
            mapbox=dict(
            center=dict(lat=4.0, lon=-74.0),
            style= 'open-street-map',
            zoom=4.5,
            ),
        legend= dict(x=3,  # Ajusta la posición en el eje X
                y=3,   # Ajusta la posición en el eje Y
    ),

    )
        
    fig.update_layout(height=600, 
                    margin={"r":25,"t":25,"l":10,"b":10}
                      )
    

    return container, fig

if __name__ == '__main__':
    app.run(debug=True, )

