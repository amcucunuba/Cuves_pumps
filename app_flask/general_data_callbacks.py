from dash import *
import dash_html_components as html
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
from l_general_data import data_df, general_data_layout, df_deptos

df = data_df
first_year_available = df['FECHA'].dt.year.max()
df_deptos = df_deptos

app = Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],suppress_callback_exceptions=True)

def register_general_data_callbacks(app):
    @app.callback(
        Output('visitas-chart', 'figure'),
        Output('stack_bar_chart', 'figure'),
        Output('my_dept_map', 'figure'),
        Input('fecha_slider', 'value'), 
        Input('select_year', 'value'),
        Input('option_slctd', 'value'),
    )

    def update_all_figures(fecha_slider, selected_year, option_slctd,):
        # Figura Calendario de visistas 
        filtered_df = df[(df['FECHA'].dt.year >= fecha_slider[0]) & (df['FECHA'].dt.year <= fecha_slider[1])]
        fig = go.Figure()

        for well in filtered_df['WELL'].unique():
            well_data = filtered_df[filtered_df['WELL'] == well]
                       
            fig.add_trace(go.Scatter(
                x=well_data['FECHA'],
                y=[well] * len(well_data),
                mode='markers', 
                marker=dict(symbol="square", size=5),
                name=well
            ))
        
        fig.update_layout(
                title=f'Record of last well visits',
                showlegend=True,
                height=1500,
                plot_bgcolor='#1f2c56',
                paper_bgcolor='#1f2c56',  
                titlefont={'color': 'white',
                                'size': 18, },
                legend= dict(font=dict(family="sans-serif",
                                size=10,
                                color='white')),
                xaxis=dict(
                    side='top',  
                    showgrid=True,
                    zeroline=True,
                    showline=True,
                    showticklabels=True,
                    tickfont=dict(
                                family='Arial',
                                size=14,
                                color= 'white')),)
        fig.update_yaxes(categoryorder='total ascending',
                        tickfont=dict(
                                family='Arial',
                                size=14,
                                color= 'white'),
                                    )
       
        filtered_df = df[df['FECHA'].dt.year == selected_year]

        last_values_df = filtered_df.groupby('WELL').first().reset_index()

        last_values_df = last_values_df.sort_values(by='RED KW', ascending=False)
        
        fig_bar = go.Figure()

        fig_bar.add_trace(go.Bar(x= last_values_df['WELL'], 
                            y= last_values_df['RED KW'],
                            textposition = 'auto',
                            text= last_values_df['RED KW'], 
                            hoverinfo = 'text',
                            hovertext =
                                ('<b>Well</b>: ' + last_values_df['WELL'].astype(str) + '<br>' +
                                '<b>Red Kw</b>: ' + last_values_df['RED KW'].astype(str) + '<br>'), 
                            width = 0.8,
                            marker=dict(color='#912d2d'),
                            textfont = dict(
                                    family = "sans-serif",
                                    size = 13,
                                    color = 'white'),
                            ), )
        
        fig_bar.add_trace(go.Scatter(x=last_values_df['WELL'], 
                            y= last_values_df['RED KW'],
                            mode='lines',
                            hoverinfo = 'none', 
                            line=dict(color='orange', width=2, shape = "spline", smoothing = 1.3,),
                            ))

        fig_bar.update_layout(
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
    #Mapa de ubicacion de pozos activos e inactivos 
        color_mapping = {"Act": "green","No_act": "#bd061c"}

        if option_slctd == 'No_actAct':
                # Si se selecciona "Alls", mostramos todos los pozos
            filtered_df = df_deptos
        else:
               # Si se selecciona "Active" o "Inactive", filtramos por esa opción
            filtered_df = df_deptos[df_deptos['ACTIVIDAD'] == option_slctd]

        fig_map = go.Figure(go.Scattermapbox(
            lat=filtered_df['LATITUD'],
            lon=filtered_df['LONGITUD'],
            mode='markers',
            text=filtered_df['ACTIVIDAD'],  # Esto configura el texto en la etiqueta emergente
            hovertext=filtered_df['DEPARTAMENTO'] + '<br>'  + filtered_df['ACTIVIDAD'],
            marker= dict(
                size=20,
                opacity = 0.7,
                color=[color_mapping[act] for act in filtered_df['ACTIVIDAD']],
                # symbol = 'circle-open',
                autocolorscale=False,
                cmin=0,
                ),
        ))
        fig_map.update_layout(coloraxis=dict(colorscale='Viridis'))

        fig_map.update_layout(
                mapbox=dict(
                    center=dict(lat=4.5, lon=-74.5),
                    style= 'carto-darkmatter',
                    zoom=4, 
                ) )
        
        fig_map.update_layout(plot_bgcolor='#1f2c56',
                        paper_bgcolor='#1f2c56',)
            
        fig_map.update_layout(height=450,
                        margin={"r":0,"t":0,"l":0,"b":0},
                        )
        return fig, fig_bar, fig_map