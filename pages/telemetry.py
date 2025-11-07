from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
from config.database import db

def telemetry_page():
    """Real-time telemetry monitoring - ADMIN ONLY"""
    telemetry = db.get_all_telemetry()
    
    if not telemetry:
        return dbc.Container([
            html.H2("📡 Telemetry", className="mb-4 page-title"),
            dbc.Alert("No telemetry data available", color="info")
        ], fluid=True, className="dashboard-container")
    
    df = pd.DataFrame(telemetry)
    
    table = dash_table.DataTable(
        id='telemetry-table',
        columns=[
            {"name": "Satellite ID", "id": "sat_id"},
            {"name": "Timestamp", "id": "timestamp"},
            {"name": "Data Type", "id": "data_type"},
            {"name": "Value", "id": "value", "type": "numeric"},
            {"name": "Unit", "id": "unit"},
            {"name": "Status", "id": "status"},
        ],
        data=df.head(50).to_dict('records'),
        style_table={'overflowX': 'auto', 'background': 'transparent'},
        style_cell={
            'textAlign': 'left',
            'padding': '12px',
            'backgroundColor': 'rgba(0, 0, 0, 0.2)',
            'color': '#e5e7eb',
            'border': '1px solid rgba(255, 255, 255, 0.1)',
            'fontFamily': 'Inter, sans-serif'
        },
        style_header={
            'backgroundColor': 'rgba(99, 102, 241, 0.2)',
            'fontWeight': '700',
            'color': '#06b6d4',
            'textTransform': 'uppercase',
            'fontSize': '0.875rem',
            'letterSpacing': '0.05em',
            'border': '1px solid rgba(99, 102, 241, 0.3)'
        },
        page_size=15,
        sort_action='native',
        filter_action='native'
    )
    
    return dbc.Container([
        html.H2("📡 Telemetry Data", className="mb-4 page-title"),
        dbc.Card([
            dbc.CardHeader([html.I(className="fas fa-signal me-2"), "Recent Telemetry"], className="mb-0"),
            dbc.CardBody(table, className="p-0")
        ], className="glass-card"),
        dcc.Interval(id='telemetry-update', interval=10000)
    ], fluid=True, className="dashboard-container")
