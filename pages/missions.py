from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from config.database import db
from datetime import datetime

def missions_page(user_role=None):
    """Ultra-polished missions management page with cinematic styling"""
    missions = db.get_all_missions()
    is_admin = (user_role == 'admin')
    
    # Header with search and filters
    header = html.Div([
        dbc.Row([
            dbc.Col([
                html.H1([
                    html.I(className="fas fa-rocket me-3", style={"color": "#6366f1"}),
                    "Mission Control Center"
                ], className="mb-0 glow-text", style={"color": "#e5e7eb"}),
                html.P("Active mission tracking and management", className="text-secondary mb-0 mt-2")
            ], width=12, md=6),
            dbc.Col([
                html.Div([
                    dbc.Input(
                        id="mission-search",
                        type="text",
                        placeholder="🔍 Search missions...",
                        className="form-control mb-2",
                        style={"maxWidth": "400px", "marginLeft": "auto"}
                    ),
                ], className="d-flex justify-content-end")
            ], width=12, md=6)
        ], className="align-items-center")
    ], className="dashboard-header mb-4 fade-in")
    
    if not missions:
        return dbc.Container([
            header,
            dbc.Alert([
                html.I(className="fas fa-info-circle me-2"),
                "No missions found in the database"
            ], color="info", className="fade-in")
        ], fluid=True)
    
    df = pd.DataFrame(missions)
    
    # Status breakdown cards
    status_counts = df['status'].value_counts().to_dict()
    
    status_cards = dbc.Row([
        dbc.Col([
            html.Div([
                html.Div([
                    html.I(className="fas fa-check-circle mb-2", style={"fontSize": "2rem", "color": "#10b981"}),
                    html.H3(status_counts.get('Completed', 0), className="mb-0"),
                    html.Small("Completed", className="text-secondary")
                ], className="text-center")
            ], className="stat-card slide-up stagger-1")
        ], width=6, md=3, className="mb-3"),
        
        dbc.Col([
            html.Div([
                html.Div([
                    html.I(className="fas fa-spinner fa-pulse mb-2", style={"fontSize": "2rem", "color": "#06b6d4"}),
                    html.H3(status_counts.get('In Progress', 0), className="mb-0"),
                    html.Small("In Progress", className="text-secondary")
                ], className="text-center")
            ], className="stat-card slide-up stagger-2")
        ], width=6, md=3, className="mb-3"),
        
        dbc.Col([
            html.Div([
                html.Div([
                    html.I(className="fas fa-calendar-alt mb-2", style={"fontSize": "2rem", "color": "#f59e0b"}),
                    html.H3(status_counts.get('Planned', 0), className="mb-0"),
                    html.Small("Planned", className="text-secondary")
                ], className="text-center")
            ], className="stat-card slide-up stagger-3")
        ], width=6, md=3, className="mb-3"),
        
        dbc.Col([
            html.Div([
                html.Div([
                    html.I(className="fas fa-dollar-sign mb-2", style={"fontSize": "2rem", "color": "#6366f1"}),
                    html.H3(f"${df['budget'].sum()/1e6:.1f}M", className="mb-0"),
                    html.Small("Total Budget", className="text-secondary")
                ], className="text-center")
            ], className="stat-card slide-up stagger-4")
        ], width=6, md=3, className="mb-3"),
    ], className="mb-4")
    
    # Mission cards grid
    mission_cards = []
    for i, mission in enumerate(missions[:12]):  # Show first 12
        status = mission.get('status', 'Unknown')
        status_colors = {
            'Completed': '#10b981',
            'In Progress': '#06b6d4',
            'Planned': '#f59e0b',
            'Cancelled': '#ef4444'
        }
        status_color = status_colors.get(status, '#6b7280')
        
        card = dbc.Col([
            html.Div([
                # Status badge
                html.Div([
                    html.Span(status, className="badge", style={
                        "background": f"rgba{tuple(list(int(status_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + [0.2])}",
                        "color": status_color,
                        "border": f"1px solid {status_color}"
                    })
                ], className="mb-3"),
                
                # Mission name
                html.H5(mission.get('mission_name', 'Unknown'), className="mb-2", style={"color": "#e5e7eb"}),
                
                # Details
                html.Div([
                    html.Div([
                        html.I(className="fas fa-calendar me-2", style={"color": "#9ca3af"}),
                        html.Small(str(mission.get('launch_date', 'N/A')), className="text-secondary")
                    ], className="mb-2"),
                    html.Div([
                        html.I(className="fas fa-money-bill-wave me-2", style={"color": "#9ca3af"}),
                        html.Small(f"${mission.get('budget', 0):,.0f}", className="text-secondary")
                    ]),
                ]),
                
                # Progress bar if in progress
                html.Div([
                    html.Hr(style={"borderColor": "rgba(255,255,255,0.1)", "margin": "1rem 0"}),
                    html.Small("Mission Progress", className="text-muted d-block mb-1"),
                    html.Div([
                        html.Div(className="progress-bar", style={"width": "65%"})
                    ], className="progress")
                ]) if status == 'In Progress' else None,
                
            ], className="glass-card h-100 p-3 slide-up", style={"animationDelay": f"{i * 0.05}s"})
        ], width=12, md=6, lg=4, className="mb-3")
        mission_cards.append(card)
    
    missions_grid = dbc.Row(mission_cards)
    
    # Enhanced data table
    table = dash_table.DataTable(
        id='missions-table',
        columns=[
            {"name": "Mission ID", "id": "mission_id"},
            {"name": "Pad ID", "id": "pad_id"},
            {"name": "Loc ID", "id": "loc_id"},
            {"name": "Mission Name", "id": "mission_name"},
            {"name": "Launch Date", "id": "launch_date"},
            {"name": "Status", "id": "status"},
            {"name": "Budget", "id": "budget", "type": "numeric", "format": {"specifier": "$,.2f"}},
            {"name": "Objective", "id": "objective"},
        ],
        data=df.to_dict('records'),
        style_table={
            'overflowX': 'auto',
            'background': 'transparent'
        },
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
            'fontWeight': 'bold',
            'color': '#06b6d4',
            'textTransform': 'uppercase',
            'fontSize': '0.875rem',
            'letterSpacing': '0.05em',
            'border': '1px solid rgba(99, 102, 241, 0.3)'
        },
        style_data_conditional=[
            {
                'if': {'filter_query': '{status} = "Completed"'},
                'backgroundColor': 'rgba(16, 185, 129, 0.1)',
                'borderLeft': '3px solid #10b981'
            },
            {
                'if': {'filter_query': '{status} = "In Progress"'},
                'backgroundColor': 'rgba(6, 182, 212, 0.1)',
                'borderLeft': '3px solid #06b6d4'
            },
            {
                'if': {'filter_query': '{status} = "Planned"'},
                'backgroundColor': 'rgba(245, 158, 11, 0.1)',
                'borderLeft': '3px solid #f59e0b'
            }
        ],
        page_size=15,
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
            dcc.Store(id='page-mission-modal-store', data={'mode': 'add', 'ids': None}),
            dcc.Store(id='page-mission-action-trigger', data=0),
            
            # Action buttons
            html.Div([
                dbc.Button([
                    html.I(className="fas fa-plus-circle me-2"),
                    "Add New Mission"
                ], id="page-add-mission-btn", color="success", className="mb-3 me-2", n_clicks=0),
                dbc.Button([
                    html.I(className="fas fa-edit me-2"),
                    "Edit Selected"
                ], id="page-edit-mission-btn", color="warning", outline=True, className="mb-3 me-2", n_clicks=0),
                dbc.Button([
                    html.I(className="fas fa-trash me-2"),
                    "Delete Selected"
                ], id="page-delete-mission-btn", color="danger", outline=True, className="mb-3", n_clicks=0),
            ]),

            # Feedback area
            html.Div(id="page-mission-feedback", className="mb-3"),

            # Add/Edit Modal
            dbc.Modal([
                dbc.ModalHeader(dbc.ModalTitle(id="page-mission-modal-title")),
                dbc.ModalBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Mission Name"),
                            dbc.Input(id="page-input-mission-name", placeholder="Enter name"),
                        ], md=12),
                    ], className="mb-3"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Mission ID"),
                            dbc.Input(id="page-input-mission-id", type="number", placeholder="Mission ID"),
                        ], md=4),
                        dbc.Col([
                            dbc.Label("Pad ID"),
                            dbc.Input(id="page-input-mission-pad-id", type="number", placeholder="Pad ID"),
                        ], md=4),
                        dbc.Col([
                            dbc.Label("Location ID"),
                            dbc.Input(id="page-input-mission-loc-id", type="number", placeholder="Location ID"),
                        ], md=4),
                    ], className="mb-3"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Status"),
                            dbc.Select(
                                id="page-input-mission-status",
                                options=[
                                    {"label": "Planned", "value": "Planned"},
                                    {"label": "In Progress", "value": "In Progress"},
                                    {"label": "Completed", "value": "Completed"},
                                    {"label": "Cancelled", "value": "Cancelled"},
                                ]
                            ),
                        ], md=6),
                         dbc.Col([
                            dbc.Label("Launch Date"),
                            dcc.DatePickerSingle(
                                id='page-input-mission-launch-date',
                                min_date_allowed=datetime(1990, 1, 1),
                                display_format='YYYY-MM-DD',
                                className="w-100"
                            ),
                        ], md=6),
                    ], className="mb-3"),
                     dbc.Row([
                        dbc.Col([
                            dbc.Label("Budget"),
                            dbc.Input(id="page-input-mission-budget", type="number", placeholder="Budget"),
                        ], md=6),
                    ]),
                ]),
                dbc.ModalFooter([
                    dbc.Button("Save", id="page-save-mission-btn", color="success", className="me-2", n_clicks=0),
                    dbc.Button("Cancel", id="page-cancel-mission-btn", color="secondary", n_clicks=0),
                ]),
            ], id="page-modal-mission", is_open=False, size="lg"),

            # Confirm Delete Modal
            dbc.Modal([
                dbc.ModalHeader(dbc.ModalTitle("Confirm Deletion")),
                dbc.ModalBody([
                    html.P("Are you sure you want to delete this mission? This action cannot be undone."),
                    html.P(id="page-mission-delete-confirm-text", className="fw-bold")
                ]),
                dbc.ModalFooter([
                    dbc.Button("Delete", id="page-confirm-delete-mission-btn", color="danger", className="me-2", n_clicks=0),
                    dbc.Button("Cancel", id="page-cancel-delete-mission-btn", color="secondary", n_clicks=0),
                ]),
            ], id="page-modal-confirm-delete-mission", is_open=False),
        ]

    charts = dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-chart-bar me-2"),
                        "Budget Analysis"
                    ], className="mb-0")
                ]),
                dbc.CardBody(
                    dcc.Graph(figure=create_budget_chart(df), config={'displayModeBar': False})
                )
            ], className="glass-card slide-up stagger-3")
        ], width=12, lg=6, className="mb-4"),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-chart-line me-2"),
                        "Mission Timeline"
                    ], className="mb-0")
                ]),
                dbc.CardBody(
                    dcc.Graph(figure=create_timeline_chart(df), config={'displayModeBar': False})
                )
            ], className="glass-card slide-up stagger-4")
        ], width=12, lg=6, className="mb-4"),
    ])
    
    return dbc.Container([
        header,
        status_cards,
        
        # Conditionally render admin controls
        html.Div(admin_controls) if is_admin else html.Div([
            dbc.Alert([
                html.I(className="fas fa-info-circle me-2"),
                "You are viewing in read-only mode. Only administrators can edit mission data."
            ], color="info", className="mb-3")
        ]),
        
        # Toggle between cards and table view
        html.Div([
            dbc.ButtonGroup([
                dbc.Button([html.I(className="fas fa-th me-2"), "Cards"], color="primary", outline=True, size="sm"),
                dbc.Button([html.I(className="fas fa-table me-2"), "Table"], color="primary", size="sm"),
            ], className="mb-3")
        ]),
        
        missions_grid,
        
        html.Hr(className="my-4", style={"borderColor": "rgba(255,255,255,0.1)"}),
        
        # Data table section
        dbc.Card([
            dbc.CardHeader([
                html.H5([
                    html.I(className="fas fa-table me-2"),
                    "Mission Database"
                ], className="mb-0")
            ]),
            dbc.CardBody(table, className="p-0")
        ], className="glass-card mb-4 slide-up stagger-2"),
        
        # Charts
        charts
    ], fluid=True)


def create_budget_chart(df):
    """Create enhanced budget chart with dark theme"""
    fig = go.Figure(data=[go.Bar(
        x=df['mission_name'],
        y=df['budget'],
        marker=dict(
            color=df['budget'],
            colorscale=[[0, '#6366f1'], [0.5, '#06b6d4'], [1, '#00ff88']],
            line=dict(color='rgba(99, 102, 241, 0.5)', width=1)
        ),
        text=df['budget'].apply(lambda x: f'${x/1e6:.1f}M'),
        textposition='auto',
    )])
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e5e7eb'),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            showgrid=False,
            title='Mission'
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            showgrid=True,
            title='Budget ($)'
        ),
        margin=dict(t=20, b=60, l=60, r=20),
        height=350
    )
    
    return fig


def create_timeline_chart(df):
    """Create mission timeline chart"""
    df_sorted = df.sort_values('launch_date')
    
    fig = go.Figure(data=[go.Scatter(
        x=df_sorted['launch_date'],
        y=df_sorted['budget'],
        mode='markers+lines',
        marker=dict(
            size=12,
            color=df_sorted['budget'],
            colorscale='Viridis',
            line=dict(color='rgba(255, 255, 255, 0.3)', width=1)
        ),
        line=dict(color='rgba(99, 102, 241, 0.3)', width=2),
        text=df_sorted['mission_name'],
        hovertemplate='<b>%{text}</b><br>Date: %{x}<br>Budget: $%{y:,.0f}<extra></extra>'
    )])
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e5e7eb'),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            showgrid=True,
            title='Launch Date'
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            showgrid=True,
            title='Budget ($)'
        ),
        margin=dict(t=20, b=60, l=60, r=20),
        height=350
    )
    
    return fig