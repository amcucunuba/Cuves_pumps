from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

#importar data
df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/c78bf172206ce24f77d6363a2d754b59/raw/c353e8ef842413cae56ae3920b8fd78468aa4cb2/usa-agricultural-exports-2011.csv')

# iniciar-crear la app
app = Dash(__name__)

app.layout = html.Div([

    html.Div([
        html.H1("CURVES PUMPS PERENCO COLOMBIA", 
                style= {'textAlign': 'center',
                    'color': '#686363'}),
        html.Img(src='Perenco.jpg')]),

])

# puedo cambiar el html de salida asignando un numero de 4 cifras, sin comas ni puntos
if __name__ == '__main__':
    app.run(debug=True)

#    html.Div([
#         dash_table.DataTable(
#         data=df.to_dict('records'),
#         columns=[{'id': c, 'name': c} for c in df.columns],
#         page_size=10, 
#         style_cell={'minWidth': 95, 'maxWidth': 95, 'width': 95
#     }),
#     ]),
    
#     dcc.Dropdown(df.columns, id = 'pandas-dropdown-1'),
#     html.Div(id= 'pandas-output-container-1')
# ])
# @callback(
#         Output('pandas-output-container-1', 'children'),
#         Input('pandas-dropdown-1', 'value')
# )

# def update_output(value):
#     return f'You have selected {value}'