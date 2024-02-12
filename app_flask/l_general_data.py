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
from main_final import data_df

df = data_df
num_pozos = df['WELL'].nunique()
first_year_available = df['FECHA'].dt.year.max()
df_deptos = pd.read_csv('deptos.csv', delimiter=';', encoding='latin-1')

app = Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],suppress_callback_exceptions=True)

# Grafica sunburst 
bins = [0, 50, 200, 500, float('inf')]
labels = ['0-50', '51-200', '201-500', '500+']

# Crear una nueva columna 'RED KW Group' que clasifica los valores en los grupos
df['RED KW Group'] = pd.cut(df['RED KW'], bins=bins, labels=labels, right=False)
total_value = df['RED KW'].sum()

# Agregar la fila al DataFrame
df_primeras_filas = df.groupby('WELL').first().reset_index()

df_grafica = df_primeras_filas[['RED KW Group', 'WELL', 'RED KW',]]

df_grafica = df_grafica.dropna()
count_per_group = df_grafica.groupby('RED KW Group')['WELL'].count().reset_index()
count_per_group.columns = ['RED KW Group', 'Pozo_Count']

# Fusiona la cuenta de pozos con tu DataFrame original
df_grafica = pd.merge(df_grafica, count_per_group, on='RED KW Group')
total_value = round(df_grafica['RED KW'].sum())

fig_sun = px.sunburst(df_grafica, path=['RED KW Group','Pozo_Count', 'WELL'], values='RED KW',
                color_discrete_sequence= px.colors.diverging.Spectral,
                branchvalues="total",
                maxdepth=2,
                )
fig_sun.update_traces(textinfo='label+percent entry+value')

fig_sun.update_layout(
                height=500,
                width=500,
                plot_bgcolor='#1f2c56',
                paper_bgcolor='#1f2c56',
                hovermode='closest',
                title={
                    'text': 'Last record of each well',
                    'y': 0.93,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                titlefont={
                    'color': 'white',
                    'size': 22},
                legend={
                    'orientation': 'h',
                    'bgcolor': '#1f2c56',
                    'xanchor': 'center', 'x':0.8, 'y':-0.1,
                    'traceorder': 'normal',
                    },
                font=dict(
                    family="sans-serif",
                    size=14,
                    color='white'),
                hoverlabel=dict(font=dict(size=14),),
                annotations=[dict(text= f'Total' + '<br>' + str(total_value) +' kW', 
                                font_size=16, showarrow=False, x=0.5, y=-0.12, xref="paper", yref="paper", align="center")],
            )
fig_sun.update_traces(hovertemplate='RED KW Group: %{id}<br>WELL: %{label}<br>Red kW: %{value}<br>', selector=dict(type='sunburst'))

general_data_layout = html.Div([
    html.H2('General data',  
            style={'color': 'white',
                           'margin-top': '10px',
                           }),
    html.P(f'The total number of wells reported is: {num_pozos}',  
            style={'color': 'white',
                           'fontSize': 22,
                           'margin-top': '0px',
                           'text-align': 'left'},
                    ), 
    html.Div([
            html.Div([
            
                dcc.RangeSlider(
                    max=df['FECHA'].max().year,
                    step=None,
                    id='fecha_slider',
                    marks={str(year): str(year) for year in range(df['FECHA'].min().year, df['FECHA'].max().year + 1)},
                    value=[df['FECHA'].min().year, df['FECHA'].max().year],
                    min=df['FECHA'].min().year,
                    ),
                dcc.Graph(id='visitas-chart', config={'displayModeBar': False}, figure={}),
                ],className= 'create_container1 twelve columns' ), ]),

            html.Div([
            html.Div([
                    html.P('Latest well power',
                   style = {'color': 'white',
                            'fontSize': 22, 
                            'margin-top': '20px'},
                   className = 'drop_down_list_title'
                   ),
            dcc.Dropdown(id = 'select_year',
                         multi = False,
                         clearable = True,
                         disabled = False,
                         style = {'display': 'inline-block','width': '150px', 'margin-top': '0px'},
                         value = first_year_available,
                         placeholder = 'Select year',
                         options = [{'label': year, 'value': year} for year in df['FECHA'].dt.year.unique()],
                         className = 'drop_down_list'),
                     ], className = 'title_drop_down_list'),
                     dcc.Graph(id='stack_bar_chart', figure={}, config = {'displayModeBar': False})
                ], className = "create_container1 twelve columns"),
html.Div([ 
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
                dcc.RadioItems(id='option_slctd',
                        inline=True,
                        options=[{'label': 'All', 'value': 'No_act' + 'Act'},
                                {'label': 'Active', 'value': 'Act'},
                                {'label': 'Inactive', 'value': 'No_act'}
                                ],
                        value= 'No_act' + 'Act',
                        style={'textAlign': 'left',
                        'color': 'white'},
                        className='dcc_compon'
                        ),   
                dcc.Graph(id='my_dept_map', figure={})], className="create_container1 five columns"),
            html.Div([
            html.Div([
                html.H6(children='Electrical performance',
                    style={'textAlign': 'left',
                        'color': 'white'}
                    ),
                dcc.Graph(figure= fig_sun),
                ], className="create_container1 five columns"),]),
            ]),
    ]),
])

