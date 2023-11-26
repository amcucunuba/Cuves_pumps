from dash import Dash, html, dash_table, callback, Output, Input
from dash import dcc
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from main_final import data_df


#importar data
df = data_df
df_grouped = df.groupby([df['FECHA'].dt.year, 'WELL']).agg({'RED KW': 'sum'}).reset_index()

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
            html.H2("Electric Submersible Pumps", style={"margin-bottom": "0px", 
                           'color': 'white',
                            'text-align': 'center',
                            }),
             html.H3("Colombia", style={"margin-top": "0px", 'color': 'white'}),
            ], className="two-half column", id="title"),

        html.Div([
            html.P('Last Updated: ' + str(df['FECHA'].iloc[0].strftime("%B %d, %Y")) + '  00:01 (UTC)',
                    style={'color': 'orange', "margin-bottom": "0px", 'fontSize': 10}),
                    ], className="one-third column", id='title1'),

            ],id="header", className="row flex-display", style={"margin-bottom": "10px"}),

    html.Div([
        html.Div([
        html.Div([
            html.H6('Choose the well', className='fix_label',  
                    style={'margin-bottom': '-10px',
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
            html.P(children='Frecuencia.',
                    style={'textAlign': 'center',
                        'color': 'white',
                        'fontSize': 18}
                    ),
            html.P(id='card-container-1-value',
                   style={'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 30,
                       'margin-top': '-18px'}
                   ),
           ], className="create_container three columns",
        ),

        html.Div([
            html.P(children='Red kVA',
                    style={'textAlign': 'center',
                        'color': 'white',
                        'fontSize': 18}
                    ),

            html.P(id='card-container-2-value',
                   style={'textAlign': 'center',
                       'color': '#dd1e35',
                       'fontSize': 30,
                       'margin-top': '-18px'}
                   ),
            ], className="create_container three columns",
                    ),
        html.Div([
            html.P(children='Vol MTR C',
                    style={'textAlign': 'center',
                        'color': 'white',
                        'fontSize': 18}
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
            html.P(children='%T MOTOR',
                    style={
                        'textAlign': 'center',
                        'color': 'white',
                        'fontSize': 18}
                    ),

            html.P(id='card-container-4-value',
                   style={
                       'textAlign': 'center',
                       'color': 'green',
                       'fontSize': 30, 
                       'margin-top': '-18px'}
                   ),
            ], className="create_container three columns",
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
                html.H6(children='Well location',
                    style={'textAlign': 'left',
                        'color': 'white'}
                    ),
            dcc.Dropdown(id="slct_state",
                            options=[{'label': state, 'value': state} for state in df_deptos['DEPARTAMENTO'].unique()],
                            multi=False,
                            value= df_deptos['DEPARTAMENTO'][0],
                            className='dcc_compon',),   
          dcc.Graph(id='my_dept_map', figure={})], className="create_container1 six columns"),
          html.Div([ 
            html.Div([
                     html.H6('Ultimate well power',
                   style = {'color': 'white'},
                   className = 'drop_down_list_title'
                   ),
            dcc.Dropdown(id = 'select_year',
                         multi = False,
                         clearable = True,
                         disabled = False,
                         style = {'display': True},
                          value = 'Select year',
                         placeholder = 'Select year',
                         options = [{'label': year, 'value': year} for year in df['FECHA'].dt.year.unique()],
                         className = 'drop_down_list'),
                     ], className = 'title_drop_down_list'),
                     dcc.Graph(id='stack_bar_chart', figure={}, config = {'displayModeBar': False})
                ], className = "create_container1 six columns"),

            ], className="row flex-display"),

    
    html.Div([
        html.Div([
            html.H5('Measurement Track Record', style={'margin-bottom': '0.45em', 'color': 'white'}),
                html.Div([
                    dash_table.DataTable(
                    id='data-table', 
                    style_table={'width': '100%',
                                 },
                    style_header={'textAlign': 'center',
                                'backgroundColor': 'rgb(210, 210, 210)',
                                'color': 'black',
                                'fontWeight': 'bold',
                                'font-family': 'Arial',
                                'fontSize': 12
                                },
                    style_data={'color':'black', 'backgroundColor': 'rgb(255, 255, 255)', 
                                'font-family': 'Arial',
                                'fontSize': 12},
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
    
    avg_frecuencia = filtered_df['FRECUENCIA'].iloc[0]
    card_content_1_value = [html.P(f"{avg_frecuencia:,.0f} Hz")]

    avg_red_kva= filtered_df['RED KVA'].iloc[0]
    card_content_2_value = [html.P(f"{avg_red_kva:,.0f} kVA")]

    avg_vol_mtr_c= filtered_df['VOL MTR C'].iloc[0]
    card_content_3_value = [html.P(f"{avg_vol_mtr_c:,.0f} V")]

    avg_t_motor= filtered_df['T Motor (F)'].iloc[0]
    card_content_4_value = [html.P(f"{avg_t_motor:,.0f} ºF")]
    
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
    hover_text = ('<b>Fecha</b>: %{x} <br>' +
        '<b>FRECUENCIA</b>: %{y} <br>' +
        '<b>VOL MTR A</b>: %{yaxis2} <br>' +
        '<b>KVA VSD</b>: %{yaxis3} <br>' +
        '<b>PF OUT VSD</b>: %{yaxis4} <br>' +
        '<b>PF IN VSD</b>: %{yaxis5} <br>' +
        '<b>VOL MTR B</b>: %{yaxis6} <br>' +
        '<b>VOL MTR C</b>: %{yaxis7} <br>' +
        '<b>RED KVA</b>: %{yaxis8} <br>' +
        '<b>RED KW</b>: %{yaxis9} <br>' +
        '<b>KVA SUT</b>: %{yaxis10} <br>' +
        '<b>% LOAD MTR</b>: %{yaxis11} <br>' +
        '<b>T Motor (F)</b>: %{yaxis12} <br>'),
                    
    fig.update_layout(title=f'Graph for {selected_well} in the range of years {years_range}',
                    plot_bgcolor='#1f2c56',
                    paper_bgcolor='#1f2c56',
                    hovermode='closest',
                    titlefont={'color': 'white',
                        'size': 18, },
                    # hovertemplate= hover_text,
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
                           size=10,))

    fig.update_yaxes(showgrid=False, showline=True, linecolor='white', mirror=True, tickfont=dict(
                           family='Arial',
                           size=10,))
    
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
                style= 'carto-darkmatter',
                zoom=4, 
            ) )
    
    fig.update_layout(plot_bgcolor='#1f2c56',
                    paper_bgcolor='#1f2c56',)
        
    fig.update_layout(height=500, 
                    margin={"r":50,"t":25,"l":10,"b":10},
                    )
    
    return fig
@app.callback(
    Output(component_id='stack_bar_chart', component_property='figure'),
    [Input(component_id='select_year', component_property='value')]
)
def update_fig_bar(selected_year):
    filtered_df = df[df['FECHA'].dt.year == selected_year]

    last_values_df = filtered_df.groupby('WELL').last().reset_index()

    fig = go.Figure()

    fig.add_trace(go.Bar(x=last_values_df['RED KW'], 
                         y=last_values_df['WELL'], 
                         orientation='h', 
                         textposition = 'auto',
                         text=last_values_df['RED KW'], 
                         hoverinfo = 'text',
                         hovertext =
                            '<b>Well</b>: ' + last_values_df['WELL'].astype(str) + '<br>' +
                            '<b>Red Kw</b>: ' + last_values_df['RED KW'].astype(str) + '<br>', 
                         marker=dict(color='#950808'),
                         textfont = dict(
                                family = "sans-serif",
                                size = 12,
                                color = 'white'),
                         name=f'Año {selected_year}'))

    fig.update_layout(barmode='stack', 
                    # title=f'Power of wells by {selected_year}', 
                    margin = dict(t = 28, r = 0, l = 0),
                    xaxis=dict(title = '<b>Red kW<b>',
                            showline=True,
                            showgrid=True,
                            showticklabels=True,
                            linecolor='white',
                            linewidth=1,
                            tickfont=dict(family='Arial',
                                size=10,
                                color='white'
                            )),
                    yaxis=dict(title = '<b>Wells<b>',
                            categoryorder='total descending',
                            visible = True,
                            color = 'white',
                            showline = False,
                            showgrid = False,
                            showticklabels = True,
                            linecolor = 'white',
                            linewidth = 1,), 

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
                        height=500,
                          )

    return fig

if __name__ == '__main__':
    app.run(debug=True)