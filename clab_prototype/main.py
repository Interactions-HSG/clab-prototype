#!/usr/bin/env python
from pathlib import Path

import dash
from dash import (
    dcc,
    html,
    DiskcacheManager
)
from dash.dependencies import (
    Input,
    Output,
)
import diskcache
from clab_ceis import shop, ceis
from recipe_synth.app import app as rs_app

import config as cfg

class CeisDemoHome():
    _shop = None
    _monitor = None
    _planner = None
    _app = None

    def __init__(self, app: dash.Dash) -> None:
        self._app = app
        self._shop = shop.CeisShop(app)
        self._monitor = ceis.CeisMonitor(app)
        self._planner = rs_app.RecipeSynthesizer(app)

    # Function to read Markdown content from a file
    def read_markdown_file(self, filename):
        folder_path = Path(__file__).resolve().parent.parent  # Path to subfolder parallel to parent folder
        file_path = folder_path / filename
        with open(file_path, 'r') as file:
            markdown_content = file.read()
        return markdown_content

    def make_app(self):
        # Define the layout for the home view
        home_layout = html.Div([
            dcc.Markdown(children=self.read_markdown_file("README.md"))
        ])

        # TODO: Makes this a dash page instead
        # https://dash.plotly.com/urls
        # Define the app layout, including tabs for switching between views
        self._app.layout = html.Div([
            dcc.Tabs(id='tabs', value='home', children=[
                dcc.Tab(label='Home', value='home'),
                dcc.Tab(label='Shop', value='shop'),
                dcc.Tab(label='CEM', value='monitor'),
                dcc.Tab(label='Planner', value='planner')
            ]),
            html.Div(id='tabs-content')
        ])

        # Define callback to switch between views based on tab selection
        @self._app.callback(Output('tabs-content', 'children'),
                    [Input('tabs', 'value')])
        def render_content(tab):
            if tab == 'home':
                return home_layout
            elif tab == 'shop':
                return self._shop.layout
            elif tab == 'monitor':
                return self._monitor.layout
            elif tab == 'planner':
                return self._planner.layout

if __name__ == '__main__':
    # Initialize Dash app
    # TODO: Move this to OS specific caches
    cache = diskcache.Cache(Path(__file__).parent / "cache")
    background_callback_manager = DiskcacheManager(cache)
    app = dash.Dash(
        __name__,
        suppress_callback_exceptions=True,
        background_callback_manager=background_callback_manager
    )
    demo_home = CeisDemoHome(app)
    demo_home.make_app()
    
   
    # app.run_server(host="localhost", port="8051", debug=True)
    app.run_server(host=cfg.PROTO_HOSTNAME, port=cfg.PROTO_PORT, debug=True)
