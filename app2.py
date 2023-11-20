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
app = Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

app.layout = html.Div([
    html.Div([
        html.Div([        
            html.Img(src= ("assets/Artua-Wall-E-Wall-e.256.png"),
                className= "one-third column", 
                id='corona-image', 
                style={'width': 'auto', 
                        'height': '100px', 
                        "margin-bottom": "10px",
                        }
                        ),
                ]), 
        html.Div([
            html.H2("Electric Submersible Pumps", style={"margin-bottom": "0px", 
                           'color': 'white',
                            'text-align': 'center',
                            }),
             html.H3("Colombia", style={"margin-top": "0px", 'color': 'white'}),
            ], className="two-half column", id="title"),

        html.Div([
            html.P('Last Updated: ' + str(df['FECHA'].iloc[0].strftime("%B %d, %Y")) + '  00:01 (UTC)',
                    style={'color': 'orange', "margin-bottom": "0px",}),
                    ], className="one-third column", id='title1'),

            ],id="header", className="row flex-display", style={"margin-bottom": "10px"}),

    html.Div([
        html.Div([
        html.Div([
            html.H6('Choose the well', className='fix_label',  
                    style={'margin-bottom': '0px',
                           'textAlign': 'left',
                           'color': 'white'},
                    ), 
            dcc.Dropdown(options=[{'label': well, 'value': well} for well in df['WELL'].unique()], 
                        id='pandas-dropdown-1', 
                        value=df['WELL'][0], 
                        className= 'dcc_compon')
                        ], className ='adjust_drop_down_lists',
                        ),
        ], className = "card_container twelve columns"),
            html.Div(id='pandas-output-container-1'),
                ], className = "row flex-display", id="cross-filter-options"),

    html.Div([
        html.Div([
            html.H6(children='Promedio Frecuencia.',
                    style={'textAlign': 'center',
                        'color': 'white'}
                    ),
            html.P(id='card-container-1-value',
                   style={'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 40}
                   ),
            html.P('Para el pozo seleccionado',
                   style={'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 15,
                       'margin-top': '-18px'}
                   )], className="card_container four columns",
        ),

        html.Div([
            html.H6(children='Promedio no. 2, RED KVA',
                    style={'textAlign': 'center',
                        'color': 'white'}
                    ),

            html.P(id='card-container-2-value',
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
                   )], className="card_container four columns",
                    ),
        html.Div([
            html.H6(children='Promedio no. 3',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

            html.P(id='card-container-3-value',
                   style={
                       'textAlign': 'center',
                       'color': '#dd611e',
                       'fontSize': 40}
                   ),

            html.P('y nounou',
                   style={
                       'textAlign': 'center',
                       'color': '#dd611e',
                       'fontSize': 15,
                       'margin-top': '-18px'}
                   )], className="card_container four columns",
                    ),

        html.Div([
            html.H6(children='Promedio %T MOTOR',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

            html.P(id='card-container-4-value',
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
                   )], className="card_container four columns",
                 ),
               ],className="row flex-display", style={"margin-bottom": "5px"}),

    html.Div([    
        html.Div([
            dcc.Graph(id='graph', className="create_container twelve columns"),
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
                html.H6(children='Ubicacion de pozos',
                    style={'textAlign': 'left',
                        'color': 'white'}
                    ),
            dcc.Dropdown(id="slct_state",
                            options=[{'label': state, 'value': state} for state in df_deptos['DEPARTAMENTO'].unique()],
                            multi=False,
                            value= df_deptos['DEPARTAMENTO'][0],
                            className='dcc_compon',),   
          dcc.Graph(id='my_dept_map', figure={})], className="create_container1 six columns"),
            ], className="row flex-display"),

    html.Div([
        html.Div([
            html.H5('Measurement Track Record', style={'margin-bottom': '0.45em', 'color': 'white'}),
                html.Div([
                    dash_table.DataTable(
                    id='data-table', 
                    style_table={'width': '100%'},
                    style_header={'textAlign': 'center',
                                'backgroundColor': 'rgb(210, 210, 210)',
                                'color': 'black',
                                'fontWeight': 'bold'},
                    style_data={'color':'black', 'backgroundColor': 'rgb(255, 255, 255)'},
                    style_data_conditional=[{'if': {'row_index': 'odd'},
                                        'backgroundColor': 'rgb(220, 220, 220)',
                                        }],
                    columns=[{'name':'WELL', 'id':'WELL'}, {'name':'FECHA', 'id':'FECHA'}, {'name':'FRECUENCIA', 'id':'FRECUENCIA'},
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
                        ],className = "row flex-display",),

    ], id="mainContainer",
    style={"display": "flex", "flex-direction": "column"})
@app.callback(
    [Output('card-container-1-value', 'children'),
     Output('card-container-2-value', 'children'),
     Output('card-container-3-value', 'children'),
     Output('card-container-4-value', 'children')],
    [Input(component_id='pandas-dropdown-1', component_property= 'value'),
     Input(component_id='FECHA--slider', component_property='value')])

def update_card_container(selected_well, year_range):
    #Primer filtro del df de acuerdo con el pozo seleccionado 
    filtered_df = df[df['WELL'] == selected_well]
    
    #2do. filtro del df de acuerdo con la fecha seleccionada
    filtered_df = filtered_df[(filtered_df['FECHA'].dt.year >= year_range[0]) & (filtered_df['FECHA'].dt.year <= year_range[1])]
    
    avg_frecuencia = filtered_df['FRECUENCIA'].mean()
    card_content_1_value = [html.P(f"{avg_frecuencia:,.0f}")]

    avg_red_kva= filtered_df['RED KVA'].mean()
    card_content_2_value = [html.P(f"{avg_red_kva:,.0f}")]

    avg_vol_mtr_c= filtered_df['VOL MTR C'].mean()
    card_content_3_value = [html.P(f"{avg_vol_mtr_c:,.0f}")]

    avg_t_motor= filtered_df['T Motor (F)'].mean()
    card_content_4_value = [html.P(f"{avg_t_motor:,.0f}")]
    
    # Llamar a la función para actualizar el dato   
    return card_content_1_value, card_content_2_value, card_content_3_value, card_content_4_value


@app.callback(
    [Output(component_id='data-table', component_property= 'data'),
    Output(component_id='graph', component_property= 'figure')],
    [Input(component_id='pandas-dropdown-1', component_property= 'value'),
     Input(component_id='FECHA--slider', component_property='value')])

def update_table(selected_well, year_range):
    #Primer filtro del df de acuerdo con el pozo seleccionado 
    filtered_df = df[df['WELL'] == selected_well]
    
    #2do. filtro del df de acuerdo con la fecha seleccionada
    filtered_df = filtered_df[(filtered_df['FECHA'].dt.year >= year_range[0]) & (filtered_df['FECHA'].dt.year <= year_range[1])]
    
    avg_frecuencia = filtered_df['FRECUENCIA'].mean()
    # card_content_1_value = [html.P(f"Promedio Frecuencia: {avg_frecuencia:,.0f}")]
    
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
                             marker=dict(size=4),
                             ))

    fig.add_trace(go.Scatter(x=filtered_df['FECHA'], 
                             y=filtered_df['KVA VSD'], 
                             name="KVA VSD", 
                             yaxis="y3", 
                             marker=dict(size=4),
                             ))
    
    fig.add_trace(go.Scatter(x=filtered_df['FECHA'], 
                             mode='lines+markers',
                             y=filtered_df['PF OUT VSD'], 
                             name="PF OUT VSD", 
                             yaxis="y4", 
                             marker=dict(size=4),
                             ))

    fig.add_trace(go.Scatter(x=filtered_df['FECHA'], 
                             y=filtered_df['PF IN VSD'], 
                             name="PF IN VSD", 
                             yaxis="y5", 
                             mode='lines+markers',
                             marker=dict(size=4),
                             ))

    fig.add_trace(go.Scatter(x=filtered_df['FECHA'], 
                             y=filtered_df['VOL MTR B'], 
                             name="VOL MTR B", 
                             yaxis="y6", 
                             mode='lines+markers',
                             marker=dict(size=4),
                             ))
    
    fig.add_trace(go.Scatter(x=filtered_df['FECHA'], 
                             y=filtered_df['VOL MTR C'], 
                             name="VOL MTR C", 
                             yaxis="y7", 
                             mode='lines+markers',
                             marker=dict(size=4),
                             ))
    
    fig.add_trace(go.Scatter(x=filtered_df['FECHA'], 
                             y=filtered_df['RED KVA'], 
                             name="RED KVA", 
                             yaxis="y8", 
                             mode='lines+markers',
                             marker=dict(size=4),
                             ))
    
    fig.add_trace(go.Scatter(x=filtered_df['FECHA'], 
                             y=filtered_df['RED KW'], 
                             name="RED KW", 
                             yaxis="y9", 
                             mode='lines+markers',
                             marker=dict(size=4),
                             ))

    fig.add_trace(go.Scatter(x=filtered_df['FECHA'], 
                             y=filtered_df['KVA SUT'], 
                             name="KVA SUT", 
                             yaxis="y10", 
                             mode='lines+markers',
                             marker=dict(size=4),
                             ))
    fig.add_trace(go.Scatter(x=filtered_df['FECHA'], 
                             y=filtered_df['% LOAD MTR'], 
                             name="% LOAD MTR", 
                             yaxis="y11", 
                             mode='lines+markers',
                             marker=dict(size=4),
                             ))
    fig.add_trace(go.Scatter(x=filtered_df['FECHA'], 
                             y=filtered_df['T Motor (F)'], 
                             name="T Motor (F)", 
                             yaxis="y12", 
                             mode='lines+markers',
                             marker=dict(size=4),
                             ))

    fig.update_layout(
        xaxis=dict(title='Date',
                    color='white',
                     linecolor='white',
                   tickfont=dict(
                            family='Arial',
                            size=12,
                            color='white'
                        )),

        yaxis=dict(
            title='Frecuencia',
            titlefont=dict( color="#ed01d2"
                               ),
            tickfont=dict(color="#ed01d2"),
            ),
        yaxis2=dict(
            title="Vol Mtr A",
            overlaying="y",
            side="right",
            titlefont=dict(color="#ca2323"
                        ),
            tickfont=dict(color="#ca2323",
                        )
            ),
        yaxis3=dict(
            title="KVA VSD",
            overlaying="y", 
            anchor="free",
            autoshift=True,
            titlefont=dict(color="#05aa68"
                        ),
            tickfont=dict(color="#05aa68",
                        ),
            domain=[0.15, 0.4],
             ),
        yaxis4=dict(
            title="PF Out VSD",
            overlaying="y", 
            anchor="free",
            side="right",
            autoshift=True,
            titlefont=dict(color="#7A45D1"
                        ),
            tickfont=dict(color="#7A45D1"),
            domain=[0.45, 0.7],
             ),
        yaxis5=dict(
            title="PF In VSD",
            overlaying="y", 
            anchor="free",
            side="left",
            autoshift=True,
            titlefont=dict(color="#f06e17"
                        ),
            tickfont=dict(color="#f06e17",
                        ),
            domain=[0.15, 0.4]
             ),
        yaxis6=dict(
            title="Vol Mtr B",
            overlaying="y", 
            anchor="free",
            side="right",
            autoshift=True,
            titlefont=dict(color="#30C9C7"
                        ),
            tickfont=dict(color="#30C9C7",
                        ),
            domain=[0.45, 0.7],
             ),
        yaxis7=dict(
            title="Vol Mtr C",
            overlaying="y", 
            anchor="free",
            side="left",
            autoshift=True,
            titlefont=dict( color="#b41f65"
                               ),
            tickfont=dict(color="#b41f65"),
            domain=[0.45, 0.7]
            ),
        yaxis8=dict(
            title="Red KVA",
            overlaying="y", 
            anchor="free",
            side="right",
            autoshift=True,
            titlefont=dict( color="#3da303"
                               ),
            tickfont=dict(color="#3da303")
             ),
        yaxis9=dict(
            title="Red KW",
            overlaying="y", 
            anchor="free",
            side="left",
            autoshift=True,
            titlefont=dict( color="#e56c6c"
                               ),
            tickfont=dict(color="#e56c6c")
             ),
        yaxis10=dict(
            title="KVA SUT",
            overlaying="y", 
            anchor="free",
            autoshift=True,
            side="right",
            titlefont=dict( color="#f9dd04"
                               ),
            tickfont=dict(color="#f9dd04"),
            domain=[0.5, 0.75]
            ),
        yaxis11=dict(
            title="% LOAD MTR",
            overlaying="y", 
            anchor="free",
            side="left",
            autoshift=True,
            titlefont=dict( color="#cd9ee1"
                               ),
            tickfont=dict(color="#cd9ee1"),
            domain=[0.5, 0.75],
             ),
        yaxis12=dict(
            title="T Motor (F)",
            overlaying="y", 
            anchor="free",
            side="right",
            autoshift=True,
            titlefont=dict( color="#d9680c"
                               ),
            tickfont=dict(color="#d9680c")
             ),
            )

    fig.update_layout(title=f'Graph for {selected_well} in the range of years {years_range}',
                    plot_bgcolor='#1f2c56',
                    paper_bgcolor='#1f2c56',
                    hovermode='closest',
                    titlefont={'color': 'white',
                        'size': 20, },
                    legend= dict(orientation='h',
                                xanchor= 'center',
                                bgcolor ='#1f2c56',
                                font=dict(family="sans-serif",
                                          size=10,
                                          color='white')
                                   ),
                    width=1200,
                    height=420,)
    
    fig.update_xaxes(showgrid=False, showline=True, linecolor='grey', tickfont=dict(
                           family='Arial',
                           size=12,))

    fig.update_yaxes(showgrid=False, showline=True, linecolor='white', mirror=True, tickfont=dict(
                           family='Arial',
                           size=12,))
    
    return fig

@app.callback(
#     #[Output(component_id='output_container', component_property='children'),
    Output(component_id='my_dept_map', component_property='figure'),
    [Input(component_id='slct_state', component_property='value')]
)
def update_graph(option_slctd):
    # container = "The year chosen by user was: {}".format(option_slctd)
    
    color_mapping = {"Act": "orange","No_act": "grey"}

    fig = go.Figure(go.Scattermapbox(
        lat=df_deptos['LATITUD'],
        lon=df_deptos['LONGITUD'],
        mode='markers',
        text=df_deptos['DEPARTAMENTO'],  # Esto configura el texto en la etiqueta emergente
        hovertext=df_deptos['DEPARTAMENTO'] + '<br>'  + df_deptos['ACTIVIDAD'],
        marker= dict(
            size=20,
            opacity = 0.8,
            color=[color_mapping[act] for act in df_deptos['ACTIVIDAD']],
            # symbol = 'circle-open',
            autocolorscale=False,
            cmin=0,
                        ),
    ))
    fig.update_layout(coloraxis=dict(colorscale='Viridis'))

    fig.update_layout(
            mapbox=dict(
                center=dict(lat=4.0, lon=-74.0),
                style= 'carto-positron',
                zoom=4, 
            ) )
    
    fig.update_layout(legend= dict(x=3,  # Ajusta la posición en el eje X
                                y=3,   # Ajusta la posición en el eje Y
                                ),)
        
    fig.update_layout(height=400, 
                    margin={"r":50,"t":25,"l":10,"b":10},
                    )
    
    return fig

if __name__ == '__main__':
    app.run(debug=True)