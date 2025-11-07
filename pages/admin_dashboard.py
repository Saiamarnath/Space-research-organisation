from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from config.database import db
from datetime import datetime

def admin_dashboard_page():
    """
    Admin Dashboard - Full database management interface
    CRUD operations for all tables, system monitoring, and admin controls
    """
    
    # Get system statistics
    try:
        departments = db.get_all_departments()
        employees = db.get_all_employees()
        satellites = db.get_all_satellites()
        missions = db.get_all_missions()
        research_facts = db.get_all_research_facts()
    except Exception as e:
        print(f"Error loading admin dashboard data: {e}")
        departments = []
        employees = []
        satellites = []
        missions = []
        research_facts = []
    
    # Header with admin badge
    header = html.Div([
        dbc.Row([
            dbc.Col([
                html.H1([
                    html.I(className="fas fa-user-shield me-3", style={"color": "#ef4444"}),
                    "Admin Control Center"
                ], className="mb-0 page-title", style={"color": "#e5e7eb"}),
                html.P("Full database management and system administration", className="text-secondary mb-0 mt-2")
            ], width="auto"),
            dbc.Col([
                html.Div([
                    html.Span("ADMIN ACCESS", className="badge", style={
                        "background": "rgba(239, 68, 68, 0.2)",
                        "color": "#ef4444",
                        "border": "1px solid #ef4444",
                        "fontSize": "1rem",
                        "padding": "0.5rem 1.5rem"
                    })
                ], className="d-flex justify-content-end align-items-center h-100")
            ], width="auto", className="ms-auto"),
        ], className="align-items-center")
    ], className="dashboard-header mb-4 fade-in")
    
    # System Overview Cards
    overview_cards = dbc.Row([
        dbc.Col([
            html.Div([
                html.I(className="fas fa-building mb-2", style={"fontSize": "2rem", "color": "#6366f1"}),
                html.H3(len(departments), className="mb-0"),
                html.Small("Departments", className="text-secondary")
            ], className="stat-card slide-up stagger-1 text-center")
        ], width=6, md=3, className="mb-3"),
        
        dbc.Col([
            html.Div([
                html.I(className="fas fa-users mb-2", style={"fontSize": "2rem", "color": "#10b981"}),
                html.H3(len(employees), className="mb-0"),
                html.Small("Employees", className="text-secondary")
            ], className="stat-card slide-up stagger-2 text-center")
        ], width=6, md=3, className="mb-3"),
        
        dbc.Col([
            html.Div([
                html.I(className="fas fa-satellite mb-2", style={"fontSize": "2rem", "color": "#06b6d4"}),
                html.H3(len(satellites), className="mb-0"),
                html.Small("Satellites", className="text-secondary")
            ], className="stat-card slide-up stagger-3 text-center")
        ], width=6, md=3, className="mb-3"),
        
        dbc.Col([
            html.Div([
                html.I(className="fas fa-rocket mb-2", style={"fontSize": "2rem", "color": "#f59e0b"}),
                html.H3(len(missions), className="mb-0"),
                html.Small("Missions", className="text-secondary")
            ], className="stat-card slide-up stagger-4 text-center")
        ], width=6, md=3, className="mb-3"),
    ], className="mb-4")
    
    # Database Management Tabs
    tabs = dbc.Tabs([
        # Employees Management Tab
        dbc.Tab(
            create_employees_management_tab(employees),
            label="Employees",
            tab_id="tab-employees",
            label_style={"color": "#e5e7eb"},
            active_label_style={"color": "#06b6d4"}
        ),
        
        # Departments Management Tab
        dbc.Tab(
            create_departments_management_tab(departments),
            label="Departments",
            tab_id="tab-departments",
            label_style={"color": "#e5e7eb"},
            active_label_style={"color": "#06b6d4"}
        ),
        
        # Satellites Management Tab
        dbc.Tab(
            create_satellites_management_tab(satellites),
            label="Satellites",
            tab_id="tab-satellites",
            label_style={"color": "#e5e7eb"},
            active_label_style={"color": "#06b6d4"}
        ),
        
        # Missions Management Tab
        dbc.Tab(
            create_missions_management_tab(missions),
            label="Missions",
            tab_id="tab-missions",
            label_style={"color": "#e5e7eb"},
            active_label_style={"color": "#06b6d4"}
        ),
        
        # Research Facts Management Tab
        dbc.Tab(
            create_research_facts_management_tab(research_facts),
            label="Research Facts",
            tab_id="tab-research",
            label_style={"color": "#e5e7eb"},
            active_label_style={"color": "#06b6d4"}
        ),
        
        # System Settings Tab
        dbc.Tab(
            create_system_settings_tab(),
            label="System Settings",
            tab_id="tab-settings",
            label_style={"color": "#e5e7eb"},
            active_label_style={"color": "#06b6d4"}
        ),
    ], id="admin-tabs", active_tab="tab-employees", className="mb-4")
    
    return dbc.Container([
        header,
        overview_cards,
        tabs,
        
        # Hidden stores for managing state
        dcc.Store(id='admin-action-trigger', data=0),
        dcc.Interval(id='admin-refresh-interval', interval=30000, n_intervals=0),
        
        # Global feedback/notification area
        html.Div(id="admin-global-notification"),
    ], fluid=True, className="dashboard-container")


def create_employees_management_tab(employees):
    """Create employees management interface"""
    import pandas as pd
    
    df = pd.DataFrame(employees) if employees else pd.DataFrame()
    
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.H4([html.I(className="fas fa-users me-2"), "Employee Management"], className="mb-3"),
            ], width="auto"),
            dbc.Col([
                dbc.Button([html.I(className="fas fa-plus me-2"), "Add Employee"], 
                           id="btn-add-employee", color="success", size="sm", className="me-2", n_clicks=0),
                dbc.Button([html.I(className="fas fa-edit me-2"), "Edit Selected"], 
                           id="btn-edit-employee", color="warning", size="sm", className="me-2", n_clicks=0, outline=True),
                dbc.Button([html.I(className="fas fa-trash me-2"), "Delete Selected"], 
                           id="btn-delete-employee", color="danger", size="sm", className="me-2", n_clicks=0, outline=True),
                dbc.Button([html.I(className="fas fa-sync me-2"), "Refresh"], 
                           id="btn-refresh-employees", color="primary", size="sm", outline=True, n_clicks=0),
            ], width="auto", className="ms-auto"),
        ], className="align-items-center mb-3"),
        
        dbc.Card([
            dbc.CardBody([
                dash_table.DataTable(
                    id='admin-employees-table',
                    columns=[
                        {"name": "ID", "id": "emp_id"},
                        {"name": "Name", "id": "emp_name"},
                        {"name": "Position", "id": "position"},
                        {"name": "Department", "id": "dept_name"},
                        {"name": "Salary", "id": "salary", "type": "numeric"},
                    ] if not df.empty else [],
                    data=df.to_dict('records') if not df.empty else [],
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
                        'backgroundColor': 'rgba(239, 68, 68, 0.2)',
                        'fontWeight': '700',
                        'color': '#ef4444',
                        'textTransform': 'uppercase',
                        'fontSize': '0.875rem',
                        'letterSpacing': '0.05em',
                        'border': '1px solid rgba(239, 68, 68, 0.3)'
                    },
                    page_size=15,
                    sort_action='native',
                    filter_action='native',
                    row_selectable='single',
                    selected_rows=[],
                )
            ], className="p-0"),
        ], className="glass-card"),
        
        html.Div(id="employee-action-feedback", className="mt-3"),
        
        # Add/Edit Employee Modal
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle(id="employee-modal-title")),
            dbc.ModalBody([
                dcc.Store(id='employee-modal-store', data={'mode': 'add', 'emp_id': None}), # To store mode and emp_id
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Employee Name"),
                        dbc.Input(id="input-emp-name", placeholder="Enter name"),
                    ], md=6),
                    dbc.Col([
                        dbc.Label("Position"),
                        dbc.Input(id="input-emp-position", placeholder="Enter position"),
                    ], md=6),
                ], className="mb-3"),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Department ID"),
                        dbc.Input(id="input-emp-dept", type="number", placeholder="Department ID"),
                    ], md=6),
                    dbc.Col([
                        dbc.Label("Salary"),
                        dbc.Input(id="input-emp-salary", type="number", placeholder="Salary"),
                    ], md=6),
                ], className="mb-3"),
                 dbc.Row([
                    dbc.Col([
                        dbc.Label("Phone"),
                        dbc.Input(id="input-emp-phone", placeholder="e.g. 555-1234"),
                    ], md=6),
                    dbc.Col([
                        dbc.Label("Hire Date"),
                        dcc.DatePickerSingle(
                            id='input-emp-hire-date',
                            min_date_allowed=datetime(1990, 1, 1),
                            max_date_allowed=datetime.now().date(),
                            display_format='YYYY-MM-DD',
                            className="w-100"
                        ),
                    ], md=6),
                ]),
            ]),
            dbc.ModalFooter([
                dbc.Button("Save", id="btn-save-employee", color="success", className="me-2", n_clicks=0),
                dbc.Button("Cancel", id="btn-cancel-employee", color="secondary", n_clicks=0),
            ]),
        ], id="modal-employee", is_open=False, size="lg"),

        # Confirm Delete Employee Modal
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Confirm Deletion")),
            dbc.ModalBody([
                html.P("Are you sure you want to delete this employee? This action cannot be undone."),
                html.P(id="employee-delete-confirm-text", className="fw-bold")
            ]),
            dbc.ModalFooter([
                dbc.Button("Delete", id="btn-confirm-delete-employee", color="danger", className="me-2", n_clicks=0),
                dbc.Button("Cancel", id="btn-cancel-delete-employee", color="secondary", n_clicks=0),
            ]),
        ], id="modal-confirm-delete-employee", is_open=False),
    ])


def create_departments_management_tab(departments):
    """Create departments management interface"""
    import pandas as pd
    
    df = pd.DataFrame(departments) if departments else pd.DataFrame()
    
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.H4([html.I(className="fas fa-building me-2"), "Department Management"], className="mb-3"),
            ], width="auto"),
            dbc.Col([
                dbc.Button([html.I(className="fas fa-plus me-2"), "Add Department"], 
                           id="btn-add-department", color="success", size="sm", className="me-2", n_clicks=0),
                dbc.Button([html.I(className="fas fa-edit me-2"), "Edit Selected"], 
                           id="btn-edit-department", color="warning", size="sm", className="me-2", n_clicks=0, outline=True),
                dbc.Button([html.I(className="fas fa-trash me-2"), "Delete Selected"], 
                           id="btn-delete-department", color="danger", size="sm", className="me-2", n_clicks=0, outline=True),
                dbc.Button([html.I(className="fas fa-sync me-2"), "Refresh"], 
                           id="btn-refresh-departments", color="primary", size="sm", outline=True, n_clicks=0),
            ], width="auto", className="ms-auto"),
        ], className="align-items-center mb-3"),
        
        dbc.Card([
            dbc.CardBody([
                dash_table.DataTable(
                    id='admin-departments-table',
                    columns=[
                        {"name": "ID", "id": "dept_id"},
                        {"name": "Department Name", "id": "dept_name"},
                        {"name": "Budget", "id": "budget", "type": "numeric"},
                        {"name": "Head ID", "id": "head_id"}, 
                    ] if not df.empty else [],
                    data=df.to_dict('records') if not df.empty else [],
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
                        'backgroundColor': 'rgba(239, 68, 68, 0.2)',
                        'fontWeight': '700',
                        'color': '#ef4444',
                        'textTransform': 'uppercase',
                        'fontSize': '0.875rem',
                        'letterSpacing': '0.05em',
                        'border': '1px solid rgba(239, 68, 68, 0.3)'
                    },
                    page_size=15,
                    sort_action='native',
                    filter_action='native',
                    row_selectable='single',
                    selected_rows=[],
                )
            ], className="p-0"),
        ], className="glass-card"),
        
        html.Div(id="department-action-feedback", className="mt-3"),

        # Add/Edit Department Modal
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle(id="department-modal-title")),
            dbc.ModalBody([
                dcc.Store(id='department-modal-store', data={'mode': 'add', 'dept_id': None}),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Department Name"),
                        dbc.Input(id="input-dept-name", placeholder="Enter name"),
                    ], md=12),
                ], className="mb-3"),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Budget"),
                        dbc.Input(id="input-dept-budget", type="number", placeholder="Budget"),
                    ], md=6),
                    dbc.Col([
                        dbc.Label("Head ID (optional)"),
                        dbc.Input(id="input-dept-head-id", type="number", placeholder="Head ID"), 
                    ], md=6),
                ]),
            ]),
            dbc.ModalFooter([
                dbc.Button("Save", id="btn-save-department", color="success", className="me-2", n_clicks=0),
                dbc.Button("Cancel", id="btn-cancel-department", color="secondary", n_clicks=0),
            ]),
        ], id="modal-department", is_open=False, size="lg"),

        # Confirm Delete Department Modal
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Confirm Deletion")),
            dbc.ModalBody([
                html.P("Are you sure you want to delete this department? This action cannot be undone."),
                html.P(id="department-delete-confirm-text", className="fw-bold")
            ]),
            dbc.ModalFooter([
                dbc.Button("Delete", id="btn-confirm-delete-department", color="danger", className="me-2", n_clicks=0),
                dbc.Button("Cancel", id="btn-cancel-delete-department", color="secondary", n_clicks=0),
            ]),
        ], id="modal-confirm-delete-department", is_open=False),
    ])


def create_satellites_management_tab(satellites):
    """Create satellites management interface"""
    import pandas as pd
    
    df = pd.DataFrame(satellites) if satellites else pd.DataFrame()
    
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.H4([html.I(className="fas fa-satellite me-2"), "Satellite Management"], className="mb-3"),
            ], width="auto"),
            dbc.Col([
                dbc.Button([html.I(className="fas fa-plus me-2"), "Add Satellite"], 
                           id="btn-add-satellite", color="success", size="sm", className="me-2", n_clicks=0),
                # --- NEW BUTTONS ---
                dbc.Button([html.I(className="fas fa-edit me-2"), "Edit Selected"], 
                           id="btn-edit-satellite", color="warning", size="sm", className="me-2", n_clicks=0, outline=True),
                dbc.Button([html.I(className="fas fa-trash me-2"), "Delete Selected"], 
                           id="btn-delete-satellite", color="danger", size="sm", className="me-2", n_clicks=0, outline=True),
                dbc.Button([html.I(className="fas fa-sync me-2"), "Refresh"], 
                           id="btn-refresh-satellites", color="primary", size="sm", outline=True, n_clicks=0),
            ], width="auto", className="ms-auto"),
        ], className="align-items-center mb-3"),
        
        dbc.Card([
            dbc.CardBody([
                dash_table.DataTable(
                    id='admin-satellites-table',
                    columns=[
                        {"name": "ID", "id": "sat_id"},
                        {"name": "Name", "id": "sat_name"},
                        {"name": "Status", "id": "sat_status"},
                        {"name": "Orbit", "id": "orbit_type"},
                        {"name": "Mass (kg)", "id": "mass", "type": "numeric"},
                    ] if not df.empty else [],
                    data=df.to_dict('records') if not df.empty else [],
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
                        'backgroundColor': 'rgba(239, 68, 68, 0.2)',
                        'fontWeight': '700',
                        'color': '#ef4444',
                        'textTransform': 'uppercase',
                        'fontSize': '0.875rem',
                        'letterSpacing': '0.05em',
                        'border': '1px solid rgba(239, 68, 68, 0.3)'
                    },
                    page_size=15,
                    sort_action='native',
                    filter_action='native',
                    row_selectable='single',
                    selected_rows=[],
                )
            ], className="p-0"),
        ], className="glass-card"),
        
        html.Div(id="satellite-action-feedback", className="mt-3"),

        # Add/Edit Satellite Modal
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle(id="satellite-modal-title")),
            dbc.ModalBody([
                dcc.Store(id='satellite-modal-store', data={'mode': 'add', 'sat_id': None}),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Satellite Name"),
                        dbc.Input(id="input-sat-name", placeholder="Enter name"),
                    ], md=6),
                     dbc.Col([
                        dbc.Label("Launch Date"),
                        dcc.DatePickerSingle(
                            id='input-sat-launch-date',
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
                            id="input-sat-status",
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
                        dbc.Input(id="input-sat-orbit", placeholder="e.g. LEO, GEO"),
                    ], md=6),
                ], className="mb-3"),
                 dbc.Row([
                    dbc.Col([
                        dbc.Label("Mass (kg)"),
                        dbc.Input(id="input-sat-mass", type="number", placeholder="Mass in kg"),
                    ], md=6),
                    dbc.Col([
                        dbc.Label("Manager ID (optional)"),
                        dbc.Input(id="input-sat-manager-id", type="number", placeholder="Manager ID"),
                    ], md=6),
                ]),
            ]),
            dbc.ModalFooter([
                dbc.Button("Save", id="btn-save-satellite", color="success", className="me-2", n_clicks=0),
                dbc.Button("Cancel", id="btn-cancel-satellite", color="secondary", n_clicks=0),
            ]),
        ], id="modal-satellite", is_open=False, size="lg"),

        # --- NEW MODAL ---
        # Confirm Delete Satellite Modal
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Confirm Deletion")),
            dbc.ModalBody([
                html.P("Are you sure you want to delete this satellite? This action cannot be undone."),
                html.P(id="satellite-delete-confirm-text", className="fw-bold")
            ]),
            dbc.ModalFooter([
                dbc.Button("Delete", id="btn-confirm-delete-satellite", color="danger", className="me-2", n_clicks=0),
                dbc.Button("Cancel", id="btn-cancel-delete-satellite", color="secondary", n_clicks=0),
            ]),
        ], id="modal-confirm-delete-satellite", is_open=False),
    ])


def create_missions_management_tab(missions):
    """Create missions management interface"""
    import pandas as pd
    
    df = pd.DataFrame(missions) if missions else pd.DataFrame()
    
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.H4([html.I(className="fas fa-rocket me-2"), "Mission Management"], className="mb-3"),
            ], width="auto"),
            dbc.Col([
                dbc.Button([html.I(className="fas fa-plus me-2"), "Add Mission"], 
                           id="btn-add-mission", color="success", size="sm", className="me-2", n_clicks=0),
                # --- NEW BUTTONS ---
                dbc.Button([html.I(className="fas fa-edit me-2"), "Edit Selected"], 
                           id="btn-edit-mission", color="warning", size="sm", className="me-2", n_clicks=0, outline=True),
                dbc.Button([html.I(className="fas fa-trash me-2"), "Delete Selected"], 
                           id="btn-delete-mission", color="danger", size="sm", className="me-2", n_clicks=0, outline=True),
                dbc.Button([html.I(className="fas fa-sync me-2"), "Refresh"], 
                           id="btn-refresh-missions", color="primary", size="sm", outline=True, n_clicks=0),
            ], width="auto", className="ms-auto"),
        ], className="align-items-center mb-3"),
        
        dbc.Card([
            dbc.CardBody([
                dash_table.DataTable(
                    id='admin-missions-table',
                    columns=[
                        {"name": "ID", "id": "mission_id"},
                        {"name": "Pad ID", "id": "pad_id"},
                        {"name": "Loc ID", "id": "loc_id"},
                        {"name": "Mission Name", "id": "mission_name"},
                        {"name": "Status", "id": "status"},
                        {"name": "Launch Date", "id": "launch_date"},
                        {"name": "Budget", "id": "budget", "type": "numeric"},
                    ] if not df.empty else [],
                    data=df.to_dict('records') if not df.empty else [],
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
                        'backgroundColor': 'rgba(239, 68, 68, 0.2)',
                        'fontWeight': '700',
                        'color': '#ef4444',
                        'textTransform': 'uppercase',
                        'fontSize': '0.875rem',
                        'letterSpacing': '0.05em',
                        'border': '1px solid rgba(239, 68, 68, 0.3)'
                    },
                    page_size=15,
                    sort_action='native',
                    filter_action='native',
                    row_selectable='single',
                    selected_rows=[],
                )
            ], className="p-0"),
        ], className="glass-card"),
        
        html.Div(id="mission-action-feedback", className="mt-3"),

        # Add/Edit Mission Modal
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle(id="mission-modal-title")),
            dbc.ModalBody([
                dcc.Store(id='mission-modal-store', data={'mode': 'add', 'ids': None}),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Mission Name"),
                        dbc.Input(id="input-mission-name", placeholder="Enter name"),
                    ], md=12),
                ], className="mb-3"),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Mission ID"),
                        dbc.Input(id="input-mission-id", type="number", placeholder="Mission ID"),
                    ], md=4),
                    dbc.Col([
                        dbc.Label("Pad ID"),
                        dbc.Input(id="input-mission-pad-id", type="number", placeholder="Pad ID"),
                    ], md=4),
                    dbc.Col([
                        dbc.Label("Location ID"),
                        dbc.Input(id="input-mission-loc-id", type="number", placeholder="Location ID"),
                    ], md=4),
                ], className="mb-3"),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Status"),
                        dbc.Select(
                            id="input-mission-status",
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
                            id='input-mission-launch-date',
                            min_date_allowed=datetime(1990, 1, 1),
                            display_format='YYYY-MM-DD',
                            className="w-100"
                        ),
                    ], md=6),
                ], className="mb-3"),
                 dbc.Row([
                    dbc.Col([
                        dbc.Label("Budget"),
                        dbc.Input(id="input-mission-budget", type="number", placeholder="Budget"),
                    ], md=6),
                ]),
            ]),
            dbc.ModalFooter([
                dbc.Button("Save", id="btn-save-mission", color="success", className="me-2", n_clicks=0),
                dbc.Button("Cancel", id="btn-cancel-mission", color="secondary", n_clicks=0),
            ]),
        ], id="modal-mission", is_open=False, size="lg"),

        # --- NEW MODAL ---
        # Confirm Delete Mission Modal
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Confirm Deletion")),
            dbc.ModalBody([
                html.P("Are you sure you want to delete this mission? This action cannot be undone."),
                html.P(id="mission-delete-confirm-text", className="fw-bold")
            ]),
            dbc.ModalFooter([
                dbc.Button("Delete", id="btn-confirm-delete-mission", color="danger", className="me-2", n_clicks=0),
                dbc.Button("Cancel", id="btn-cancel-delete-mission", color="secondary", n_clicks=0),
            ]),
        ], id="modal-confirm-delete-mission", is_open=False),
    ])


def create_research_facts_management_tab(research_facts):
    """Create research facts management interface"""
    import pandas as pd
    
    df = pd.DataFrame(research_facts) if research_facts else pd.DataFrame()
    
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.H4([html.I(className="fas fa-brain me-2"), "Research Facts Management"], className="mb-3"),
                html.P("As admin, you can delete any research fact regardless of ownership", className="text-secondary small"),
            ], width="auto"),
            dbc.Col([
                dbc.Button([html.I(className="fas fa-trash-alt me-2"), "Delete Selected"], 
                           id="btn-delete-research-fact", color="danger", size="sm", className="me-2", n_clicks=0, outline=True),
                dbc.Button([html.I(className="fas fa-sync me-2"), "Refresh"], 
                           id="btn-refresh-research-facts", color="primary", size="sm", outline=True, n_clicks=0),
            ], width="auto", className="ms-auto"),
        ], className="align-items-center mb-3"),
        
        dbc.Card([
            dbc.CardBody([
                dash_table.DataTable(
                    id='admin-research-facts-table',
                    columns=[
                        {"name": "Fact ID", "id": "fact_id"},
                        {"name": "User ID", "id": "user_id"},
                        {"name": "Title", "id": "fact_title"},
                        {"name": "Category", "id": "category"},
                        {"name": "Username", "id": "username"},
                        {"name": "Date Added", "id": "date_added"},
                    ] if not df.empty else [],
                    data=df.to_dict('records') if not df.empty else [],
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
                        'backgroundColor': 'rgba(239, 68, 68, 0.2)',
                        'fontWeight': '700',
                        'color': '#ef4444',
                        'textTransform': 'uppercase',
                        'fontSize': '0.875rem',
                        'letterSpacing': '0.05em',
                        'border': '1px solid rgba(239, 68, 68, 0.3)'
                    },
                    page_size=15,
                    sort_action='native',
                    filter_action='native',
                    row_selectable='single',
                    selected_rows=[],
                )
            ], className="p-0"),
        ], className="glass-card"),
        
        html.Div(id="research-fact-action-feedback", className="mt-3"),

        # Confirm Delete Research Fact Modal
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Confirm Deletion")),
            dbc.ModalBody([
                html.P("Are you sure you want to delete this research fact? This action cannot be undone."),
                html.P(id="research-fact-delete-confirm-text", className="fw-bold")
            ]),
            dbc.ModalFooter([
                dbc.Button("Delete", id="btn-confirm-delete-research-fact", color="danger", className="me-2", n_clicks=0),
                dbc.Button("Cancel", id="btn-cancel-delete-research-fact", color="secondary", n_clicks=0),
            ]),
        ], id="modal-confirm-delete-research-fact", is_open=False),
    ])


def create_system_settings_tab():
    """Create system settings and monitoring interface"""
    # ----- THIS IS THE CORRECTED FUNCTION -----
    return html.Div([
        html.H4([html.I(className="fas fa-cog me-2"), "System Settings & Monitoring"], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([html.I(className="fas fa-database me-2"), "Database Status"]),
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-check-circle me-2", style={"color": "#10b981"}),
                            html.Span("Connected", style={"color": "#10b981", "fontWeight": "600"}),
                        ], className="mb-3"),
                        html.Div([
                            html.Small("Connection Type: ", className="text-secondary"),
                            html.Span("Supabase PostgreSQL", className="text-white"),
                        ], className="mb-2"),
                        html.Div([
                            html.Small("Last Check: ", className="text-secondary"),
                            html.Span(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), className="text-white"),
                        ]),
                    ])
                ], className="glass-card mb-4"),
            ], md=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([html.I(className="fas fa-shield-alt me-2"), "Security Settings"]),
                    dbc.CardBody([
                        html.Div([
                            dbc.Label("Row Level Security (RLS)"),
                            html.Div([
                                html.I(className="fas fa-lock me-2", style={"color": "#06b6d4"}),
                                html.Span("Enabled", style={"color": "#06b6d4", "fontWeight": "600"}),
                            ]),
                        ], className="mb-3"),
                        html.Div([
                            dbc.Label("Authentication Provider"),
                            html.Div("Supabase Auth", className="text-white"),
                        ]),
                    ])
                ], className="glass-card mb-4"),
            ], md=6),
        ]),
        
        dbc.Card([
            dbc.CardHeader([html.I(className="fas fa-tools me-2"), "Admin Actions"]),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Button([
                            html.I(className="fas fa-sync-alt me-2"),
                            "Refresh All Data"
                        ], id="btn-refresh-all-data", color="primary", className="w-100 mb-2"),
                        html.Small("Reload all database tables", className="text-secondary d-block"),
                    ], md=4),
                    
                    # --- FIXED "EXPORT DATA" BUTTON ---
                    dbc.Col([
                        html.A( # Wrap button in a link
                            dbc.Button([
                                html.I(className="fas fa-download me-2"),
                                "Export Data"
                            ], id="btn-export-data", color="info", className="w-100 mb-2"),
                            # Use the correct Project ID and URL for SQL Editor
                            href="https://supabase.com/dashboard/project/hhjvwdfwlftyylkpvyyv/sql/new",
                            target="_blank" # Open in new tab
                        ),
                        html.Small("Go to SQL Editor for manual backup", className="text-secondary d-block"),
                    ], md=4),
                    
                    # --- FIXED "VIEW LOGS" BUTTON ---
                    dbc.Col([
                        html.A( # Wrap button in a link
                            dbc.Button([
                                html.I(className="fas fa-chart-line me-2"),
                                "View Logs"
                            ], id="btn-view-logs", color="warning", className="w-100 mb-2"),
                            # Use the correct Project ID and URL for Logs Explorer
                            href="https://supabase.com/dashboard/project/hhjvwdfwlftyylkpvyyv/logs/explorer",
                            target="_blank" # Open in new tab
                        ),
                        html.Small("System activity logs", className="text-secondary d-block"),
                    ], md=4),
                ]),
            ])
        ], className="glass-card"),
        
        html.Div(id="system-action-feedback", className="mt-3"),
    ])