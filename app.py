from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px

# Incorporate data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# Initialize the app
app = Dash(__name__)

colors = {
    'background': '#161515',
    'text': '#ff7f7f'
}
# dataframe 
df = pd.DataFrame({
    "Fruit": ["Pommes", "Oranges", "Bananas", "Pommes", "Oranges", "Bananas", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5, 3],
    "City": ["Bordeaux", "Bordeaux", "Bordeaux", "Lile", "Lile", "Lile", "Nantes"]
})

fig = px.bar(df, x="City", y="Amount", color="Fruit", barmode="group", title="Des Fruits")

# App layout
app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: mon premier essaie.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])
# Run the app
if __name__ == '__main__':
    app.run(debug=True)
