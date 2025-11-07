from dash import html, dash_table, dcc
import dash_bootstrap_components as dbc
import pandas as pd
from config.database import db
from datetime import datetime

def research_facts_page(user_role=None):
    """Research facts page with RBAC - users can edit own facts, admins can edit all"""
    facts = db.get_all_research_facts()
    
    # Default to 'user' if role is None
    if user_role is None:
        user_role = 'user'
    
    # Role badge display
    role_badge = None
    if user_role == 'admin':
        role_badge = html.Span([
            html.I(className="fas fa-user-shield me-2"),
            "ADMIN ACCESS"
        ], className="badge", style={
            "background": "rgba(239, 68, 68, 0.2)",
            "color": "#ef4444",
            "border": "1px solid #ef4444",
            "fontSize": "0.875rem",
            "padding": "0.5rem 1rem",
            "marginLeft": "1rem"
        })
    else:
        role_badge = html.Span([
            html.I(className="fas fa-user me-2"),
            "USER ACCESS"
        ], className="badge", style={
            "background": "rgba(6, 182, 212, 0.2)",
            "color": "#06b6d4",
            "border": "1px solid #06b6d4",
            "fontSize": "0.875rem",
            "padding": "0.5rem 1rem",
            "marginLeft": "1rem"
        })
    
    content = [
        html.Div([
            html.H2([
                html.I(className="fas fa-brain me-3"),
                "Research Facts Database",
                role_badge
            ], className="mb-2"),
            html.P(
                "You can view all research facts. " + 
                ("As an admin, you can edit and delete any fact." if user_role == 'admin' else "You can only edit or delete your own contributions."),
                className="text-secondary mb-4"
            )
        ])
    ]
    
    # Add new fact form - Admin only can add
    if user_role == 'admin':
        content.append(
            dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-plus-circle me-2"),
                    "Add New Research Fact",
                    html.Small(" (Admin Only)", className="text-muted ms-2")
                ], style={"background": "rgba(16, 185, 129, 0.1)"}),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Fact Title"),
                            dbc.Input(id="fact-title", placeholder="Enter fact title"),
                        ], md=6),
                        dbc.Col([
                            dbc.Label("Category"),
                            dbc.Select(
                                id="fact-category",
                                options=[
                                    {"label": "Space Weather", "value": "Space Weather"},
                                    {"label": "Orbital Mechanics", "value": "Orbital Mechanics"},
                                    {"label": "Mission Analysis", "value": "Mission Analysis"},
                                    {"label": "Propulsion", "value": "Propulsion"},
                                    {"label": "Communications", "value": "Communications"},
                                    {"label": "Other", "value": "Other"},
                                ]
                            ),
                        ], md=6),
                    ], className="mb-3"),
                    dbc.Label("Description"),
                    dbc.Textarea(id="fact-description", placeholder="Enter detailed description", rows=3, className="mb-3"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Source"),
                            dbc.Input(id="fact-source", placeholder="Enter source"),
                        ], md=6),
                        dbc.Col([
                            html.Br(),
                            dbc.Button([
                                html.I(className="fas fa-plus me-2"),
                                "Add Fact"
                            ], id="add-fact-btn", color="success", className="w-100"),
                        ], md=6),
                    ]),
                    html.Div(id="fact-add-message", className="mt-3"),
                ])
            ], className="glass-card mb-4")
        )
    else:
        # For non-admin users, show info message but include hidden form elements to prevent callback errors
        content.append(
            html.Div([
                dbc.Alert([
                    html.I(className="fas fa-info-circle me-2"),
                    "You are viewing in read-only mode. Only administrators can add or edit research facts."
                ], color="info", className="mb-3"),
                # Hidden form inputs to prevent callback errors
                html.Div([
                    dbc.Input(id="fact-title", type="hidden"),
                    dbc.Select(id="fact-category", style={"display": "none"}),
                    dbc.Textarea(id="fact-description", style={"display": "none"}),
                    dbc.Input(id="fact-source", type="hidden"),
                    dbc.Button(id="add-fact-btn", style={"display": "none"}),
                    html.Div(id="fact-add-message", style={"display": "none"}),
                ], style={"display": "none"})
            ])
        )
    
    # Table columns (single username column)
    table_columns = [
        {"name": "Fact ID", "id": "fact_id"},
        {"name": "User Name", "id": "username"},
        {"name": "Title", "id": "fact_title"},
        {"name": "Category", "id": "category"},
        {"name": "Description", "id": "description"},
        {"name": "Source", "id": "source"},
        {"name": "Date Added", "id": "date_added"},
    ]

    df = pd.DataFrame(facts or [])
    table_data = df.to_dict('records') if not df.empty else []

    table = dash_table.DataTable(
        id='research-facts-table',
        columns=table_columns,
        data=table_data,
        style_table={'overflowX': 'auto', 'background': 'transparent'},
        style_cell={
            'textAlign': 'left',
            'padding': '12px',
            'whiteSpace': 'normal',
            'height': 'auto',
            'backgroundColor': 'rgba(0, 0, 0, 0.2)',
            'color': '#e5e7eb',
            'border': '1px solid rgba(255, 255, 255, 0.1)',
            'fontFamily': 'Inter, sans-serif'
        },
        style_cell_conditional=[
            {'if': {'column_id': 'description'}, 'minWidth': '300px'},
        ],
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
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgba(255,255,255,0.03)'
            }
        ],
        page_size=10,
        sort_action='native',
        filter_action='native'
    )

    empty_state = None if table_data else html.Div([
        html.I(className="fas fa-flask mb-2", style={"color": "#06b6d4", "fontSize": "1.25rem"}),
        html.P("No research facts yet. Add the first one!", className="text-secondary mb-0"),
    ], className="text-center py-4")

    content.append(
        dbc.Card([
            dbc.CardHeader([
                html.Div([
                    html.Span([html.I(className="fas fa-database me-2"), "All Research Facts"], className="mb-0"),
                    dbc.Button([html.I(className="fas fa-sync-alt me-2"), "Refresh"], id="research-refresh-button", size="sm", color="primary", outline=True, className="ms-auto")
                ], className="d-flex align-items-center")
            ], className="mb-0"),
            dbc.CardBody([
                empty_state,
                table
            ], className="p-0")
        ], className="glass-card mb-4")
    )

    # Add a light polling interval to keep data fresh
    content.append(dcc.Interval(id='research-facts-poll', interval=10_000, n_intervals=0))
    
    return dbc.Container(content, fluid=True, className="dashboard-container")
