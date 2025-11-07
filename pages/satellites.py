from dash import html, dash_table, dcc
import dash_bootstrap_components as dbc
import pandas as pd
from config.database import db
from datetime import datetime

def satellites_page(user_role=None):
    """Satellites monitoring page"""
    satellites = db.get_all_satellites()
    is_admin = (user_role == 'admin')
    
    if not satellites:
        return dbc.Container([
            html.H2("🛰️ Satellites", className="mb-4 page-title"),
            dbc.Alert("No satellites found", color="info")
        ], fluid=True, className="dashboard-container")
    
    df = pd.DataFrame(satellites)
    
    # Build table columns
    table_columns = [
        {"name": "ID", "id": "sat_id"},
        {"name": "Name", "id": "sat_name"},
        {"name": "Status", "id": "sat_status"},
        {"name": "Orbit", "id": "orbit_type"},
        {"name": "Mass (kg)", "id": "mass", "type": "numeric"},
        {"name": "Manager", "id": "manager_name"},
    ]
    
    table = dash_table.DataTable(
        id='satellites-table',
        columns=table_columns,
        data=df.to_dict('records'),
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
        style_data_conditional=[
            {'if': {'filter_query': '{sat_status} = "Operational"'}, 'backgroundColor': 'rgba(16,185,129,0.1)', 'borderLeft': '3px solid #10b981'},
            {'if': {'filter_query': '{sat_status} = "Maintenance"'}, 'backgroundColor': 'rgba(245,158,11,0.1)', 'borderLeft': '3px solid #f59e0b'}
        ],
        page_size=10,
        sort_action='native',
        filter_action='native',
        row_selectable='single' if is_admin else False,
        selected_rows=[]
    )
    
    # --- MODALS AND CONTROLS FOR ADMIN ---
    admin_controls = []
    if is_admin:
        admin_controls = [
            # Store for modal state
            dcc.Store(id='page-satellite-modal-store', data={'mode': 'add', 'sat_id': None}),
            
            
            # Feedback area
            html.Div(id="page-satellite-feedback", className="mb-3"),

            # Add/Edit Modal
            dbc.Modal([
                dbc.ModalHeader(dbc.ModalTitle(id="page-satellite-modal-title")),
                dbc.ModalBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Satellite Name"),
                            dbc.Input(id="page-input-sat-name", placeholder="Enter name"),
                        ], md=6),
                         dbc.Col([
                            dbc.Label("Launch Date"),
                            dcc.DatePickerSingle(
                                id='page-input-sat-launch-date',
                                min_date_allowed=datetime(1990, 1, 1),
                                max_date_allowed=datetime.now().date(),
                                display_format='YYYY-MM-DD',
                                className="w-100"
                            ),
                        ], md=6),
                    ], className="mb-3"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Status"),
                            dbc.Select(
                                id="page-input-sat-status",
                                options=[
                                    {"label": "Operational", "value": "Operational"},
                                    {"label": "Maintenance", "value": "Maintenance"},
                                    {"label": "Planned", "value": "Planned"},
                                    {"label": "Decommissioned", "value": "Decommissioned"},
                                ]
                            ),
                        ], md=6),
                        dbc.Col([
                            dbc.Label("Orbit Type"),
                            dbc.Input(id="page-input-sat-orbit", placeholder="e.g. LEO, GEO"),
                        ], md=6),
                    ], className="mb-3"),
                     dbc.Row([
                        dbc.Col([
                            dbc.Label("Mass (kg)"),
                            dbc.Input(id="page-input-sat-mass", type="number", placeholder="Mass in kg"),
                        ], md=6),
                        dbc.Col([
                            dbc.Label("Manager ID (optional)"),
                            dbc.Input(id="page-input-sat-manager-id", type="number", placeholder="Manager ID"),
                        ], md=6),
                    ]),
                ]),
                dbc.ModalFooter([
                    dbc.Button("Save", id="page-save-satellite-btn", color="success", className="me-2", n_clicks=0),
                    dbc.Button("Cancel", id="page-cancel-satellite-btn", color="secondary", n_clicks=0),
                ]),
            ], id="page-modal-satellite", is_open=False, size="lg"),

            # Confirm Delete Modal
            dbc.Modal([
                dbc.ModalHeader(dbc.ModalTitle("Confirm Deletion")),
                dbc.ModalBody([
                    html.P("Are you sure you want to delete this satellite? This action cannot be undone."),
                    html.P(id="page-satellite-delete-confirm-text", className="fw-bold")
                ]),
                dbc.ModalFooter([
                    dbc.Button("Delete", id="page-confirm-delete-satellite-btn", color="danger", className="me-2", n_clicks=0),
                    dbc.Button("Cancel", id="page-cancel-delete-satellite-btn", color="secondary", n_clicks=0),
                ]),
            ], id="page-modal-confirm-delete-satellite", is_open=False),
        ]
    
    return dbc.Container([
        html.H2("🛰️ Satellites", className="mb-4 page-title"),
        
        # Conditionally render admin controls or user message
        html.Div(admin_controls) if is_admin else html.Div([
            dbc.Alert([
                html.I(className="fas fa-info-circle me-2"),
                "You are viewing in read-only mode. Only administrators can edit satellite data."
            ], color="info", className="mb-3")
        ]),
        
        dbc.Card([
            dbc.CardHeader([html.I(className="fas fa-satellite me-2"), "Satellite Fleet"], className="mb-0"),
            dbc.CardBody(table, className="p-0")
        ], className="glass-card")
    ], fluid=True, className="dashboard-container")