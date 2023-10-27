from dash import Dash, html, dash_table, callback, Output, Input
from dash import dcc
import pandas as pd
import plotly.express as px

#importar data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

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
        dcc.Dropdown(options=[{'label': well, 'value': well} for well in df['continent'].unique()], 
                     id= 'pandas-dropdown-1',),
        html.Div(id= 'pandas-output-container-1'),
        ]),
    html.Hr(),
    html.Div(
     dash_table.DataTable(
            id='data-table', page_size=10,
            columns=[{'name': col, 'id': col} for col in df.columns]
            ),
        ),

    html.Div([
        html.Div([
            html.Div([
                dcc.Dropdown(
                    df['Indicator Name'].unique(),
                    'Fertility rate, total (births per woman)',
                    id='xaxis-column'
                ),
                dcc.RadioItems(
                    ['Linear', 'Log'],
                    'Linear',
                    id='xaxis-type',
                    inline=True
                )
            ], style={'width': '48%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    df['Indicator Name'].unique(),
                    'Life expectancy at birth, total (years)',
                    id='yaxis-column'
                ),
                dcc.RadioItems(
                    ['Linear', 'Log'],
                    'Linear',
                    id='yaxis-type',
                    inline=True
                )
            ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
        ]),

        dcc.Graph(id='indicator-graphic'),

        dcc.Slider(
            df['Year'].min(),
            df['Year'].max(),
            step=None,
            id='year--slider',
            value=df['Year'].max(),
            marks={str(year): str(year) for year in df['Year'].unique()},

        )
    ])

])
@app.callback(
    Output(component_id='data-table', component_property= 'data'),
    [Input(component_id='pandas-dropdown-1', component_property= 'value')]
)
def update_table(selected_well):
    filtered_df = df[df['continent'] == selected_well]
    return filtered_df.to_dict('records')

# puedo cambiar el html de salida asignando un numero de 4 cifras, sin comas ni puntos
if __name__ == '__main__':
    app.run(debug=True)

