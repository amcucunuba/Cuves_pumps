from dash import *
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash import dash_table 
from dash import callback
from dash import Output
from dash import Input
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
from  l_well_data import well_data_layout, data_df

df = data_df

def register_well_data_callbacks(app):
    @app.callback(
    Output('card-container-1-value', 'children'),
    Output('card-container-2-value', 'children'),
    Output('card-container-3-value', 'children'),
    Output('card-container-4-value', 'children'),
    Output('card-container-5-value', 'children'),
    Output('data-table', 'data'),
    Output('graph', 'figure'),
    Output('output_container','children'),
    Input('pandas-dropdown-1','value'),
    Input('FECHA--slider', 'value')
     )
# Información de las fichas 
    def update_card_container(selected_well, year_range):
        #Primer filtro del df de acuerdo con el pozo seleccionado 
        filtered_df = df[df['WELL'] == selected_well]
        
        #2do. filtro del df de acuerdo con la fecha seleccionada
        filtered_df = filtered_df[(filtered_df['FECHA'].dt.year >= year_range[0]) & (filtered_df['FECHA'].dt.year <= year_range[1])]
        
        avg_frecuencia = float(filtered_df['FRECUENCIA'].iloc[0])
        card_content_1_value = [html.P(f"{avg_frecuencia:,.0f} Hz")]

        avg_red_kw= filtered_df['RED KW'].iloc[0]
        card_content_5_value = [html.P(f"{avg_red_kw:,.0f} kW")]

        avg_red_kva= filtered_df['RED KVA'].iloc[0]
        card_content_2_value = [html.P(f"{avg_red_kva:,.0f} kVA")]

        avg_vol_mtr_c= (filtered_df['VOL MTR C'].iloc[0] + filtered_df['VOL MTR A'].iloc[0] +filtered_df['VOL MTR B'].iloc[0])/3
        card_content_3_value = [html.P(f"{avg_vol_mtr_c:,.0f} V")]

        avg_t_motor= filtered_df['AMP MOTOR'].iloc[0]
        card_content_4_value = [html.P(f"{avg_t_motor:,.0f} A")]
        #Tabla con datos del pozo 
        
        container = f"The well chosen by the user was: {selected_well}"

        filtered_df = filtered_df[
            (filtered_df['FECHA'].dt.year >= year_range[0]) & (filtered_df['FECHA'].dt.year <= year_range[1])
        ]

        # Llamar a la función para actualizar el gráfico
        fig = update_graph_line(filtered_df, selected_well, year_range)

        return (
            card_content_1_value,
            card_content_2_value,
            card_content_3_value,
            card_content_4_value,
            card_content_5_value,
            filtered_df.to_dict('records'),
            fig, container
        )

    def update_graph_line(filtered_df, selected_well, year_range):
        # Filtrar el df de acuerdo al pozo seleccionado
        filtered_df = filtered_df[
            (filtered_df['FECHA'].dt.year >= year_range[0]) & (filtered_df['FECHA'].dt.year <= year_range[1])
        ]
        # Filtro de fecha, min y max de acuerdo al pozo, para ajustar en el título de la gráfica
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
                        height=500,)
        
        fig.update_xaxes(showgrid=False, showline=True, 
                        linecolor='white', spikecolor="green", spikesnap="cursor", spikemode="across", spikethickness=1,
                        side="bottom", showspikes=True,
                        tickfont=dict(
                            family='Arial',
                            size=10,))

        fig.update_yaxes(showgrid=False, showline=True, 
                        linecolor='white', mirror=True, 
                        showspikes=True, spikecolor="red", spikethickness=1, 
                        tickfont=dict(
                            family='Arial',
                            size=10,))
        
        return fig