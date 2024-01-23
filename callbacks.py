from dash import Dash, html, dash_table, callback, Output, Input
from dash import dcc
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
from general_data_callbacks import register_general_data_callbacks
from well_data_callbacks import register_well_data_callbacks
from l_general_data import tabs_layouts

def register_callbacks(app):
    # Registra los callbacks para cada sección
    register_general_data_callbacks(app)
    register_well_data_callbacks(app)

    # Callback principal para actualizar el contenido de las tabs
    @app.callback(
        Output('tabs-content', 'children'),
        [Input('tabs', 'value')]
    )
    def update_tab_content(selected_tab):
        return tabs_layouts[selected_tab]

