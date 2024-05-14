from pathlib import Path

import dash
from dash import (
    dcc,
    html
)
from dash.dependencies import Input, Output

# Import your shop view and ceis view
from shop import app as appshop
from ceis import app as appceis
from ceis import (
    onTapEdge,
    onTapNode,
    update_table
)

def set_callbacks(app: dash.Dash) -> None:


    (
        update_table
    )
