from dash import Dash, html, dash_table, callback, Output, Input
from dash import dcc
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
from main_final import data_df


#importar data
df = data_df
first_year_available = df['FECHA'].dt.year.max()
df_deptos = pd.read_csv('deptos.csv', delimiter=';', encoding='latin-1')

# iniciar-crear la app
app = Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

app.layout = html.Div([
    html.Div([
        html.Div([        
            html.Img(src= ("assets/Artua-Wall-E-Wall-e.256.png"),
                            id='corona-image', 
                style={'width': 'auto', 
                        'height': '100px', 
                        "margin-bottom": "10px",
                        'align-items': 'right',
                        }
                        ),
                ],className= "one-third column" ), 
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

            ],id="header", className="row flex-display", style={"margin-bottom": "0px"}),

    html.Div([
        html.Div([
        html.Div([
            html.P('Choose the well',  
                    style={'color': 'white',
                           'fontSize': 22},
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
                ], className = "title_and_drop_down_list", style={"margin-bottom": "0px"}),

    html.Div([
        html.Div([
            html.P(children='Frecuencia',
                    style={'textAlign': 'center',
                        'color': 'white',
                        'fontSize': 18,
                        'margin-top': '20px'}
                    ),
            html.P(id='card-container-1-value',
                   style={'textAlign': 'center',
                       'color': '#dd1e35',
                       'fontSize': 30,
                       'margin-top': '-18px'}
                   ),
           ], className="create_container three columns",
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
            ], className="create_container three columns",
                 ),
        html.Div([
            html.P(children='Apparent power',
                    style={'textAlign': 'center',
                        'color': 'white',
                        'fontSize': 18,
                        'margin-top': '20px'}
                    ),

            html.P(id='card-container-2-value',
                   style={'textAlign': 'center',
                       'color': 'green',
                       'fontSize': 30,
                       'margin-top': '-18px'}
                   ),
            ], className="create_container three columns",
                    ),
        html.Div([
            html.P(children='Averge motor voltage',
                    style={'textAlign': 'center',
                        'color': 'white',
                        'fontSize': 14,
                        'margin-top': '10px'}
                    ),

            html.P(id='card-container-3-value',
                   style={
                       'textAlign': 'center',
                       'color': '#dd611e',
                       'fontSize': 30,
                       'margin-top': '-18px'}
                   ),
        ], className="create_container three columns",
                    ),

        html.Div([
            html.P(children='Motor current',
                    style={
                        'textAlign': 'center',
                        'color': 'white',
                        'fontSize': 18,
                        'margin-top': '20px'}
                    ),

            html.P(id='card-container-4-value',
                   style={
                       'textAlign': 'center',
                       'color': '#e55467',
                       'fontSize': 30, 
                       'margin-top': '-18px'}
                   ),
            ], className="create_container three columns",
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
                     html.P('Ultimate well power',
                   style = {'color': 'white',
                            'fontSize': 22},
                   className = 'drop_down_list_title'
                   ),
            dcc.Dropdown(id = 'select_year',
                         multi = False,
                         clearable = True,
                         disabled = False,
                         style = {'display': 'inline-block','width': '150px'},
                         value = first_year_available,
                         placeholder = 'Select year',
                         options = [{'label': year, 'value': year} for year in df['FECHA'].dt.year.unique()],
                         className = 'drop_down_list'),
                     ], className = 'title_drop_down_list'),
                     dcc.Graph(id='stack_bar_chart', figure={}, config = {'displayModeBar': False})
                ], className = "create_container1 twelve columns"),

    html.Div([ 
        html.Div([
                html.H6(children='Well location',
                    style={'textAlign': 'left',
                        'color': 'white'}
                    ),
                html.P("Select mode:", 
                       style={'textAlign': 'left',
                        'color': 'white',
                        'margin':0}
                    ),
            dcc.RadioItems(id="slct_mode",
                        inline=True,
                        options=[{'label': 'Active', 'value': 'Act'},
                                {'label': 'Inactive', 'value': 'No_act'}
                                ],
                        value= 'Act',
                        style={'textAlign': 'left',
                        'color': 'white'},
                        className='dcc_compon'
                        ),   
          dcc.Graph(id='my_dept_map', figure={})], className="create_container1 six columns"),
          html.Div([
                    dcc.Graph(id='pie_chart', figure={}),
                              ], className="create_container1 five columns"),
            ], className="row flex-display"),

    
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
     Output('card-container-4-value', 'children'),
     Output('card-container-5-value', 'children')],
    [Input(component_id='pandas-dropdown-1', component_property= 'value'),
     Input(component_id='FECHA--slider', component_property='value')])

def update_card_container(selected_well, year_range):
    #Primer filtro del df de acuerdo con el pozo seleccionado 
    filtered_df = df[df['WELL'] == selected_well]
    
    #2do. filtro del df de acuerdo con la fecha seleccionada
    filtered_df = filtered_df[(filtered_df['FECHA'].dt.year >= year_range[0]) & (filtered_df['FECHA'].dt.year <= year_range[1])]
    
    avg_frecuencia = filtered_df['FRECUENCIA'].iloc[0]
    card_content_1_value = [html.P(f"{avg_frecuencia:,.0f} Hz")]

    avg_red_kw= filtered_df['RED KW'].iloc[0]
    card_content_5_value = [html.P(f"{avg_red_kw:,.0f} kW")]

    avg_red_kva= filtered_df['RED KVA'].iloc[0]
    card_content_2_value = [html.P(f"{avg_red_kva:,.0f} kVA")]

    avg_vol_mtr_c= (filtered_df['VOL MTR C'].iloc[0] + filtered_df['VOL MTR A'].iloc[0] +filtered_df['VOL MTR B'].iloc[0])/3
    card_content_3_value = [html.P(f"{avg_vol_mtr_c:,.0f} V")]

    avg_t_motor= filtered_df['AMP MOTOR'].iloc[0]
    card_content_4_value = [html.P(f"{avg_t_motor:,.0f} A")]
    
    return card_content_1_value, card_content_2_value, card_content_3_value, card_content_4_value, card_content_5_value

@app.callback(
    [Output(component_id='data-table', component_property= 'data'),
    Output(component_id='graph', component_property= 'figure'),
    Output(component_id='output_container', component_property='children')],
    [Input(component_id='pandas-dropdown-1', component_property= 'value'),
     Input(component_id='FECHA--slider', component_property='value')])

def update_table(selected_well, year_range):
    #Primer filtro del df de acuerdo con el pozo seleccionado 
    filtered_df = df[df['WELL'] == selected_well]

    container = "The well chosen by user was: {}".format(selected_well)
    
    #2do. filtro del df de acuerdo con la fecha seleccionada
    filtered_df = filtered_df[(filtered_df['FECHA'].dt.year >= year_range[0]) & (filtered_df['FECHA'].dt.year <= year_range[1])]

    # Llamar a la función para actualizar el gráfico
    fig = update_graph_line(filtered_df, selected_well, year_range)
    
    
    return filtered_df.to_dict('records'), fig, container

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
                             mode='lines+markers',
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
                             marker=dict(size=4)
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
                             mode='lines+markers',
                             name="T Motor (F)", 
                             yaxis="y12", 
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
            titlefont=dict( color="#1f77b4"
                               ),
            tickfont=dict(color="#1f77b4"),
            ),
        yaxis2=dict(
            title="Vol Mtr A",
            overlaying="y",
            side="right",
            titlefont=dict(color="#d62728"
                        ),
            tickfont=dict(color="#d62728",
                        ),
            domain=[0.45, 0.7]
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
            domain=[0.45, 0.7],
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
            titlefont=dict(color="paleturquoise"
                        ),
            tickfont=dict(color='paleturquoise',
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
            tickfont=dict(color="#3da303"),
            domain=[0.45, 0.7]
             ),
        yaxis9=dict(
            title="Red KW",
            overlaying="y", 
            anchor="free",
            side="right",
            autoshift=True,
            titlefont=dict( color="#e56c6c"
                               ),
            tickfont=dict(color="#e56c6c"),
             domain=[0.45, 0.7]
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
            side="right",
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
            tickfont=dict(color="#d9680c"),
            domain=[0.45, 0.7]
             ),
            )
    
                    
    fig.update_layout(title=f'Graph for {selected_well} in the range of years {years_range}',
                    plot_bgcolor='#1f2c56',
                    paper_bgcolor='#1f2c56',
                    hovermode='x',
                    titlefont={'color': 'white',
                        'size': 18, },
                    legend= dict(orientation='h',
                                xanchor= 'center',
                                bgcolor ='#1f2c56',
                                font=dict(family="sans-serif",
                                          size=10,
                                          color='white')
                                   ),
                    width=1200,
                    height=400,)
    
    fig.update_xaxes(showgrid=False, showline=True, 
                     linecolor='white', spikecolor="green", spikesnap="cursor", spikemode="across",
                    side="bottom", showspikes=True,
                     tickfont=dict(
                           family='Arial',
                           size=10,))

    fig.update_yaxes(showgrid=False, showline=True, 
                     linecolor='white', mirror=True, 
                     showspikes=True, spikecolor="red", spikethickness=2, 
                     tickfont=dict(
                           family='Arial',
                           size=10,))
    
    return fig

@app.callback(
    Output(component_id='my_dept_map', component_property='figure'),
    [Input(component_id='slct_mode', component_property='value')]
)
def update_graph(option_slctd):
    color_mapping = {"Act": "orange","No_act": "grey"}

    filtered_df = df_deptos[df_deptos['ACTIVIDAD'] == option_slctd]

    fig = go.Figure(go.Scattermapbox(
        lat=filtered_df['LATITUD'],
        lon=filtered_df['LONGITUD'],
        mode='markers',
        text=filtered_df['ACTIVIDAD'],  # Esto configura el texto en la etiqueta emergente
        hovertext=filtered_df['DEPARTAMENTO'] + '<br>'  + filtered_df['ACTIVIDAD'],
        marker= dict(
            size=20,
            opacity = 0.8,
            color=[color_mapping[act] for act in filtered_df['ACTIVIDAD']],
            # symbol = 'circle-open',
            autocolorscale=False,
            cmin=0,
            ),
    ))
    fig.update_layout(coloraxis=dict(colorscale='Viridis'))

    fig.update_layout(
            mapbox=dict(
                center=dict(lat=4.0, lon=-75.5),
                style= 'carto-darkmatter',
                zoom=4, 
            ) )
    
    fig.update_layout(plot_bgcolor='#1f2c56',
                    paper_bgcolor='#1f2c56',)
        
    fig.update_layout(height=400,
                    margin={"r":0,"t":0,"l":0,"b":0},
                    )
    
    return fig

@app.callback(
    Output(component_id='stack_bar_chart', component_property='figure'),
    [Input(component_id='select_year', component_property='value')]
)
def update_fig_bar(selected_year):
    filtered_df = df[df['FECHA'].dt.year == selected_year]

    last_values_df = filtered_df.groupby('WELL').first().reset_index()

    last_values_df = last_values_df.sort_values(by='RED KW', ascending=False)
    
    fig = go.Figure()

    fig.add_trace(go.Bar(x= last_values_df['WELL'], 
                         y= last_values_df['RED KW'],
                         textposition = 'auto',
                         text= last_values_df['RED KW'], 
                         hoverinfo = 'text',
                         hovertext =
                            ('<b>Well</b>: ' + last_values_df['WELL'].astype(str) + '<br>' +
                            '<b>Red Kw</b>: ' + last_values_df['RED KW'].astype(str) + '<br>'), 
                         width = 0.8,
                         marker=dict(color='#950808'),
                         textfont = dict(
                                family = "sans-serif",
                                size = 12,
                                color = 'white'),
                         ), )
    
    fig.add_trace(go.Scatter(x=last_values_df['WELL'], 
                         y= last_values_df['RED KW'],
                        mode='lines',
                        hoverinfo = 'none', 
                        line=dict(color='orange', width=2, shape = "spline", smoothing = 1.3,),
                        ))

    fig.update_layout(
                    margin = dict(r=0,t=20,l=0,b=0),
                    height=400,
                    showlegend = False,
                    hovermode='closest', 
                    plot_bgcolor='#1f2c56',
                    paper_bgcolor='#1f2c56',
                    legend={'orientation': 'h',
                              'bgcolor': '#1f2c56',
                              'xanchor': 'center', 'x': 0.5, 'y': -0.3},
                    titlefont={
                        'color': 'white',
                        'size': 18,
                        },
                    autosize= True,
                        
                    xaxis=dict(title = '<b>Wells<b>',
                            color = 'white',
                            visible = True,
                            showline=False,
                            showgrid=False,
                            showticklabels=True,
                            linecolor='white',
                            linewidth=1,
                            tickfont=dict(family='Arial',
                                size=10,
                                color='white'
                            ),
                            tickangle=-90),
                    yaxis=dict(title = '<b>Red Kw<b>',
                            color = 'white',
                            showline = True,
                            showgrid = False,
                            showticklabels = True,
                            linecolor = 'white',
                            linewidth = 1,), 
                          )

    return fig

@app.callback(Output(component_id='pie_chart', component_property='figure'),
            [Input(component_id='select_year', component_property='value')])

def update_pie_chart(selected_year):
    filtered_df = df[df['FECHA'].dt.year == selected_year]

    last_values_df = filtered_df.groupby('WELL').first().reset_index()

    colors = ['#e55467', 'green', 'orange','#dd1e35' ]
    # group_1 = last_values_df[last_values_df['RED KW'] < 50]
    # group_2 = last_values_df[(last_values_df['RED KW'] >= 51) & (last_values_df['RED KW'] <= 200)]
    # group_3 = last_values_df[(last_values_df['RED KW'] >= 201) & (last_values_df['RED KW'] <= 500)]
    # group_4 = last_values_df[last_values_df['RED KW'] > 501]
    # labels = ['0-50', '51-200', '201-500', '500+']
    # print(group_4['RED KW'])
    last_values_df['RED KW Group'] = pd.cut(last_values_df['RED KW'], bins=[0, 50, 200, 500, float('inf')], labels=['0-50 kW', '51-200 kW', '201-500 kW', '500+ kW'])
    
    # Calcular la suma de cada grupo
    grouped_data = last_values_df.groupby('RED KW Group')['RED KW'].sum()
    
    labels = [f"{label} ({', '.join(names)})" for label, names in zip(grouped_data.index, last_values_df.groupby('RED KW Group')['WELL'].apply(list))]

    total_value = round(last_values_df['RED KW'].sum())

    fig = go.Figure()

    # fig.add_trace(go.Pie(labels= labels,
    #                      values=[group_1['RED KW'].sum(), group_2['RED KW'].sum(), group_3['RED KW'].sum(), group_4['RED KW'].sum()],
    #                      marker=dict(colors=colors),
                        #  name= [group_1['WELL'],group_2['WELL'], group_3['WELL'], group_4['WELL']], 
    fig.add_trace(go.Pie(
                        labels=labels,
                        values=grouped_data.values,
                        marker=dict(colors=colors),
                        hoverinfo='label+percent+value',
                        textinfo='value+percent',
                        textfont=dict(size=13),
                        hole=.4,
                        rotation=65
                        ))

    fig.update_layout(
                # height=500,
                plot_bgcolor='#1f2c56',
                paper_bgcolor='#1f2c56',
                hovermode='closest',
                title={
                    'text': 'Electrical performance ' + str((selected_year)),
                    'y': 0.93,
                    'x': 0.5,
                    'xanchor': 'right',
                    'yanchor': 'top'},
                titlefont={
                    'color': 'white',
                    'size': 20},
                legend={
                    'orientation': 'h',
                    'bgcolor': '#1f2c56',
                    'xanchor': 'center', 'x':0.8, 'y':-0.1,
                    'traceorder': 'normal',
                    },
                font=dict(
                    family="sans-serif",
                    size=4,
                    color='white'),
                hoverlabel=dict(font=dict(size=8),),
                annotations=[dict(text= f'Total' + '<br>' + str(total_value) +' kW', 
                                   x=0.5, y=0.5, 
                                   font_size=12, showarrow=False)],
            )

    return fig

if __name__ == '__main__':
    app.run(debug=True)