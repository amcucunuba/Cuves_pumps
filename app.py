from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

# Incorporate data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# iniciar-crear la app
app = Dash(__name__)

colors = {
    'background': '#c1bebe',
    'text': '#ff7f7f',
    'fond': '#880E4F'
}
# dataframe 
df = pd.DataFrame({
    "Fruit": ["Pommes", "Oranges", "Bananas", "Pommes", "Oranges", "Bananas", "Bananas"],
    "Quantité": [4, 1, 2, 2, 4, 5, 3],
    "Ville": ["Bordeaux", "Bordeaux", "Bordeaux", "Lile", "Lile", "Lile", "Nantes"]
})

#fig = px.bar(df, x="Ville", y="Quantité", color="Fruit", barmode="group", title="Des Fruits")

# Crear el App layout, es el diseño de como se va a ver la aplicación
#Baner o titulo = H1, radioitems, graficos
app.layout = html.Div(className='row', style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Hello Dash',
        style={'textAlign': 'center',
            'color': colors['text'],
        }
    ),

    html.H2(children='Dash: mon premier essaie.', 
             style={'textAlign': 'center',
                    'color': colors['fond'],
    }), 

    dash_table.DataTable(data=df.to_dict('records'), page_size=10, style_table={'overflowX': 'auto'}),
#Separa la informacion 
    html.Hr(),

    html.Div([
        html.Div([
            html.H3('Choisir la variable', className= 'fix-label', style={'textAlign': 'center','color': 'red', 'margin-top':'35px'} ),
            dcc.RadioItems(id='controls-and-radio-item', 
                           labelStyle = {'display': 'inline-block'},
                           options=['Ville', 'Quantité', 'Fruit'], 
                           value='Fruit', 
                           style={'color': colors['text'], 'margin-top':'50px'}, className = 'dcc_compon'),  
                            ], className= 'create_container2 five columns', style = {'margin-bottom': '50px'})
                            ], className = 'row flex-display',),
                               
    html.Div([
        dcc.Graph(figure={}, id='controls-and-graph')]),

])

# Añadir controles para crear la interacción
@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(col_chosen):
    fig = px.bar(df, x="Ville", y=col_chosen, barmode="group", title="Des Fruits")
    return fig

# Ejecutar la app
if __name__ == '__main__':
    app.run(debug=True)
