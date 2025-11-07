"""
Space Research System - Fixed Main Application
With proper authentication, role-based access control, and all features
"""
import dash
from dash import dcc, html, Input, Output, State, dash_table, callback_context
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
# --- NEW IMPORT ---
import pandas as pd
from datetime import datetime
import json

# Import our modules
from config.database import db
from utils.auth import auth, store_session, load_session, check_authentication, get_user_role

# Page components moved to the `pages` package (modularized)
from pages import (
    login_page,
    signup_page,
    login_selection_page,
    admin_login_page,
    user_login_page,
    admin_signup_page,
    user_signup_page,
    research_facts_page,
    dashboard_home,
    common_dashboard_page,
    missions_page,
    satellites_page,
    employees_page,
    telemetry_page,
    analytics_page,
    unauthorized_page,
    admin_dashboard_page,
)

# ============================================
# INITIALIZE DASH APP
# ============================================

app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.FONT_AWESOME,
        "/assets/styles.css"  # Our custom space theme
    ],
    external_scripts=[],  # REMOVED custom.js, Dash loads it from /assets automatically
    suppress_callback_exceptions=True,
    title="Space Research - Mission Control",
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"},
        {"name": "description", "content": "Space Research and Exploration Mission Control Center"},
    ]
)

server = app.server

# ============================================
# NAVBAR COMPONENT
# ============================================
# ... (omitted, no changes) ...
def create_navbar(is_authenticated=False, user_role=None):
    """Create navigation bar based on auth status and role"""
    if is_authenticated:
        # Admin gets all access with red theme
        if user_role == 'admin':
            nav_items = dbc.Nav([
                dbc.NavItem(dbc.NavLink("Dashboard", href="/", className="text-white")),
                dbc.NavItem(dbc.NavLink([
                    html.I(className="fas fa-user-shield me-1"),
                    "Admin Control"
                ], href="/admin-dashboard", className="text-white", style={"borderBottom": "2px solid #ef4444"})),
                dbc.NavItem(dbc.NavLink("Missions", href="/missions", className="text-white")),
                dbc.NavItem(dbc.NavLink("Satellites", href="/satellites", className="text-white")),
                dbc.NavItem(dbc.NavLink([
                    html.I(className="fas fa-users-cog me-1"),
                    "Employees"
                ], href="/employees", className="text-white", style={"borderBottom": "2px solid #ef4444"})),
                dbc.NavItem(dbc.NavLink([
                    html.I(className="fas fa-satellite-dish me-1"),
                    "Telemetry"
                ], href="/telemetry", className="text-white", style={"borderBottom": "2px solid #ef4444"})),
                dbc.NavItem(dbc.NavLink("Research Facts", href="/research", className="text-white")),
                dbc.NavItem(dbc.NavLink([
                    html.I(className="fas fa-chart-line me-1"),
                    "Analytics"
                ], href="/analytics", className="text-white", style={"borderBottom": "2px solid #ef4444"})),
                dbc.NavItem(html.Span([
                    html.I(className="fas fa-user-shield me-2", style={"color": "#ef4444"}),
                    html.Span("ADMIN", style={"color": "#ef4444", "fontWeight": "700", "fontSize": "0.875rem"})
                ], className="nav-link")),
                dbc.NavItem(dbc.NavLink([
                    html.I(className="fas fa-sign-out-alt me-1"),
                    "Logout"
                ], href="/logout", id="logout-link", className="text-danger")),
            ], pills=True)
        else:
            # Regular users have limited access with blue theme
            nav_items = dbc.Nav([
                dbc.NavItem(dbc.NavLink("Home", href="/", className="text-white")),
                dbc.NavItem(dbc.NavLink("Missions", href="/missions", className="text-white")),
                dbc.NavItem(dbc.NavLink("Satellites", href="/satellites", className="text-white")),
                dbc.NavItem(dbc.NavLink("Research Facts", href="/research", className="text-white")),
                dbc.NavItem(html.Span([
                    html.I(className="fas fa-user me-2", style={"color": "#06b6d4"}),
                    html.Span("USER", style={"color": "#06b6d4", "fontWeight": "700", "fontSize": "0.875rem"})
                ], className="nav-link")),
                dbc.NavItem(dbc.NavLink([
                    html.I(className="fas fa-sign-out-alt me-1"),
                    "Logout"
                ], href="/logout", id="logout-link", className="text-danger")),
            ], pills=True)
    else:
        # Show a public navbar with disabled/proxy links to help discovery.
        # All links route to /login and show a lock icon to indicate auth is required.
        nav_items = dbc.Nav([
            dbc.NavItem(dbc.NavLink([
                html.I(className="fas fa-home me-1"),
                "Dashboard",
                html.I(className="fas fa-lock ms-2 text-warning")
            ], href="/login", className="text-white")),
            dbc.NavItem(dbc.NavLink([
                html.I(className="fas fa-rocket me-1"),
                "Missions",
                html.I(className="fas fa-lock ms-2 text-warning")
            ], href="/login", className="text-white")),
            dbc.NavItem(dbc.NavLink([
                html.I(className="fas fa-satellite me-1"),
                "Satellites",
                html.I(className="fas fa-lock ms-2 text-warning")
            ], href="/login", className="text-white")),
            dbc.NavItem(dbc.NavLink([
                html.I(className="fas fa-flask me-1"),
                "Research",
                html.I(className="fas fa-lock ms-2 text-warning")
            ], href="/login", className="text-white")),
            dbc.NavItem(dbc.NavLink([
                html.I(className="fas fa-sign-in-alt me-1"),
                "Login"
            ], href="/login", className="text-info fw-bold")),
        ], pills=True)
    
    navbar = dbc.Navbar(
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.A(
                        dbc.Row([
                            dbc.Col(html.I(className="fas fa-satellite fa-2x text-white")),
                            dbc.Col(dbc.NavbarBrand("Space Research System", className="ms-2 text-white")),
                        ], align="center", className="g-0"),
                        href="/",
                        style={"textDecoration": "none"}
                    )
                ], width="auto"),
            ], align="center"),
            dbc.NavbarToggler(id="navbar-toggler"),
            # Keep collapse open by default to ensure items are visible without a toggler callback
            dbc.Collapse(nav_items, id="navbar-collapse", navbar=True, className="ms-auto", is_open=True),
        ], fluid=True),
        color="dark",
        dark=True,
        className="mb-4"
    )
    
    return navbar

# ============================================
# APP LAYOUT
# ============================================
# ... (omitted, no changes) ...
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='session-store', storage_type='session'),
    dcc.Store(id='redirect-trigger', data=0),
    html.Div(id='navbar-container'),
    html.Div(id='page-content')
])

# ============================================
# MAIN CALLBACKS (Auth, Routing, etc.)
# ============================================
# ... (omitted, no changes) ...
@app.callback(
    Output('navbar-container', 'children'),
    Input('session-store', 'data')
)
def update_navbar(session_data):
    """Update navbar based on authentication status and role"""
    try:
        is_authenticated = check_authentication(session_data)
        user_role = get_user_role(session_data) if is_authenticated else None
        return create_navbar(is_authenticated, user_role)
    except Exception as e:
        print(f"Error in update_navbar: {str(e)}")
        import traceback
        traceback.print_exc()
        # Return a simple navbar on error
        return dbc.Navbar(
            dbc.Container([
                dbc.NavbarBrand("Space Research System", className="text-white"),
                dbc.Nav([
                    dbc.NavItem(dbc.NavLink("Login", href="/login", className="text-white")),
                ], pills=True, className="ms-auto")
            ], fluid=True),
            color="dark",
            dark=True,
        )

@app.callback(
    Output('session-store', 'data', allow_duplicate=True),
    Input('url', 'pathname'),
    prevent_initial_call=True
)
def clear_session_on_logout(pathname):
    """When user hits /logout, clear the browser session-store and sign out server-side."""
    if pathname == '/logout':
        try:
            auth.sign_out()
        except Exception:
            pass
        # Clear the stored session on the client
        return None
    return dash.no_update

@app.callback(
    Output('session-store', 'data', allow_duplicate=True),
    Input('logout-link', 'n_clicks'),
    prevent_initial_call=True
)
def clear_session_on_logout_click(n_clicks):
    """Clear client session when logout link is clicked (extra robustness)."""
    if n_clicks and n_clicks > 0:
        try:
            auth.sign_out()
        except Exception:
            pass
        return None
    return dash.no_update

@app.callback(
    [Output('page-content', 'children'),
     Output('url', 'pathname', allow_duplicate=True)],
    [Input('url', 'pathname'),
     Input('redirect-trigger', 'data')],
    [State('session-store', 'data')],
    prevent_initial_call='initial_duplicate'
)
def display_page(pathname, redirect_trigger, session_data):
    """Route to different pages with role-based access control"""
    try:
        is_authenticated = check_authentication(session_data)
        user_role = get_user_role(session_data) if is_authenticated else 'user'  # Default to 'user' if not set
        
        # Public routes
        if pathname == '/login-select':
            if is_authenticated:
                if user_role == 'admin':
                    return dashboard_home(user_role), '/'
                else:
                    return common_dashboard_page(user_role), '/'
            return login_selection_page(), dash.no_update
        
        if pathname == '/login':
            if is_authenticated:
                return common_dashboard_page(user_role), '/'
            return user_login_page(), dash.no_update
        
        if pathname == '/admin-login':
            if is_authenticated:
                return dashboard_home(user_role), '/'
            return admin_login_page(), dash.no_update
        
        if pathname == '/signup':
            if is_authenticated:
                return common_dashboard_page(user_role), '/'
            return user_signup_page(), dash.no_update
        
        if pathname == '/user-signup':
            if is_authenticated:
                return common_dashboard_page(user_role), '/'
            return user_signup_page(), dash.no_update
        
        if pathname == '/admin-signup':
            if is_authenticated:
                return dashboard_home(user_role), '/'
            return admin_signup_page(), dash.no_update
        
        # Logout route
        if pathname == '/logout':
            auth.sign_out()
            return login_selection_page(), '/login-select'
        
        # Protected routes - redirect to login selection if not authenticated
        if not is_authenticated:
            return login_selection_page(), '/login-select'
        
        # Admin-only routes
        admin_routes = ['/employees', '/telemetry', '/analytics', '/admin-dashboard', '/dashboard']
        if pathname in admin_routes and user_role != 'admin':
            return unauthorized_page(), dash.no_update
        
        # Route to pages
        if pathname == '/':
            # Admin sees the full dashboard, users see common dashboard
            if user_role == 'admin':
                return dashboard_home(user_role), dash.no_update
            else:
                return common_dashboard_page(user_role), dash.no_update
        elif pathname == '/dashboard':
            # Admin-only full dashboard
            if user_role == 'admin':
                return dashboard_home(user_role), dash.no_update
            else:
                return unauthorized_page(), dash.no_update
        elif pathname == '/common-dashboard':
            # Common dashboard accessible to both
            return common_dashboard_page(user_role), dash.no_update
        elif pathname == '/admin-dashboard':
            return admin_dashboard_page(), dash.no_update
        elif pathname == '/missions':
            return missions_page(user_role), dash.no_update
        elif pathname == '/satellites':
            return satellites_page(user_role), dash.no_update
        elif pathname == '/employees':
            return employees_page(), dash.no_update
        elif pathname == '/telemetry':
            return telemetry_page(), dash.no_update
        elif pathname == '/research':
            return research_facts_page(user_role), dash.no_update
        elif pathname == '/analytics':
            return analytics_page(), dash.no_update
        else:
            # Default to common dashboard for authenticated users
            return common_dashboard_page(user_role), dash.no_update
            
    except Exception as e:
        print(f"Error in display_page: {str(e)}")
        import traceback
        traceback.print_exc()
        return html.Div([
            dbc.Alert([
                html.H4("Page Error", className="alert-heading"),
                html.P(f"Error: {str(e)}")
            ], color="danger")
        ]), dash.no_update

@app.callback(
    [Output('session-store', 'data', allow_duplicate=True),
     Output('login-error', 'children'),
     Output('redirect-trigger', 'data', allow_duplicate=True)],
    [Input('login-button', 'n_clicks'),
     Input('login-email', 'n_submit'),
     Input('login-password', 'n_submit')],
    [State('login-email', 'value'),
     State('login-password', 'value')],
    prevent_initial_call=True
)
def handle_login(n_clicks, email_submit, password_submit, email, password):
    """Handle login with proper redirect - supports Enter key and button click"""
    ctx = callback_context
    if not ctx.triggered:
        return dash.no_update, dash.no_update, dash.no_update
    
    if not email or not password:
        return dash.no_update, dbc.Alert("Please enter email and password", color="danger", className="shake"), dash.no_update
    
    try:
        result = auth.sign_in(email, password)
        
        if result.get("success"):
            session_data = store_session(result)
            success_msg = dbc.Alert([
                html.I(className="fas fa-check-circle me-2"),
                "Access granted — Welcome back, Commander"
            ], color="success", className="fade-in")
            return session_data, success_msg, (n_clicks or 0) + (email_submit or 0) + (password_submit or 0)
        else:
            error_msg = result.get("error", "Login failed")
            return dash.no_update, dbc.Alert([
                html.I(className="fas fa-times-circle me-2"),
                f"Invalid credentials: {error_msg}"
            ], color="danger", className="shake"), dash.no_update
    except Exception as e:
        return dash.no_update, dbc.Alert([
            html.I(className="fas fa-exclamation-triangle me-2"),
            f"Error: {str(e)}"
        ], color="danger", className="shake"), dash.no_update

@app.callback(
    Output('signup-message', 'children'),
    [Input('signup-button', 'n_clicks')],
    [State('signup-username', 'value'),
     State('signup-email', 'value'),
     State('signup-password', 'value'),
     State('signup-password-confirm', 'value')],
    prevent_initial_call=True
)
def handle_signup(n_clicks, username, email, password, password_confirm):
    """Handle user signup - stays on signup page"""
    if not n_clicks or n_clicks == 0:
        return dash.no_update
    
    if not email or not password or not username:
        return dbc.Alert("Please fill in all fields", color="danger")
    
    if len(password) < 6:
        return dbc.Alert("Password must be at least 6 characters", color="danger")
    
    if password != password_confirm:
        return dbc.Alert("Passwords do not match", color="danger")
    
    try:
        result = auth.sign_up(email, password, username, role='user')
        
        if result.get("success"):
            return dbc.Alert([
                html.H5("✅ Account created successfully!", className="alert-heading"),
                html.P("Your account has been created. You can now login."),
                html.Hr(),
                html.A("Go to Login", href="/login", className="alert-link btn btn-success")
            ], color="success")
        else:
            error_msg = result.get("error", "Signup failed")
            return dbc.Alert(f"Signup failed: {error_msg}", color="danger")
    except Exception as e:
        return dbc.Alert(f"Error: {str(e)}", color="danger")

@app.callback(
    [Output('session-store', 'data', allow_duplicate=True),
     Output('admin-login-error', 'children'),
     Output('redirect-trigger', 'data', allow_duplicate=True)],
    [Input('admin-login-button', 'n_clicks'),
     Input('admin-login-email', 'n_submit'),
     Input('admin-login-password', 'n_submit')],
    [State('admin-login-email', 'value'),
     State('admin-login-password', 'value')],
    prevent_initial_call=True
)
def handle_admin_login(n_clicks, email_submit, password_submit, email, password):
    """Handle admin login"""
    ctx = callback_context
    if not ctx.triggered:
        return dash.no_update, dash.no_update, dash.no_update
    
    if not email or not password:
        return dash.no_update, dbc.Alert("Please enter email and password", color="danger", className="shake"), dash.no_update
    
    try:
        result = auth.sign_in(email, password)
        
        if result.get("success"):
            session_data = store_session(result)
            success_msg = dbc.Alert([
                html.I(className="fas fa-check-circle me-2"),
                "Admin access granted"
            ], color="success", className="fade-in")
            return session_data, success_msg, (n_clicks or 0) + (email_submit or 0) + (password_submit or 0)
        else:
            error_msg = result.get("error", "Login failed")
            return dash.no_update, dbc.Alert([
                html.I(className="fas fa-times-circle me-2"),
                f"Invalid admin credentials: {error_msg}"
            ], color="danger", className="shake"), dash.no_update
    except Exception as e:
        return dash.no_update, dbc.Alert([
            html.I(className="fas fa-exclamation-triangle me-2"),
            f"Error: {str(e)}"
        ], color="danger", className="shake"), dash.no_update

@app.callback(
    [Output('session-store', 'data', allow_duplicate=True),
     Output('user-login-error', 'children'),
     Output('redirect-trigger', 'data', allow_duplicate=True)],
    [Input('user-login-button', 'n_clicks'),
     Input('user-login-email', 'n_submit'),
     Input('user-login-password', 'n_submit')],
    [State('user-login-email', 'value'),
     State('user-login-password', 'value')],
    prevent_initial_call=True
)
def handle_user_login(n_clicks, email_submit, password_submit, email, password):
    """Handle user login"""
    ctx = callback_context
    if not ctx.triggered:
        return dash.no_update, dash.no_update, dash.no_update
    
    if not email or not password:
        return dash.no_update, dbc.Alert("Please enter email and password", color="danger", className="shake"), dash.no_update
    
    try:
        result = auth.sign_in(email, password)
        
        if result.get("success"):
            session_data = store_session(result)
            success_msg = dbc.Alert([
                html.I(className="fas fa-check-circle me-2"),
                "User access granted"
            ], color="success", className="fade-in")
            return session_data, success_msg, (n_clicks or 0) + (email_submit or 0) + (password_submit or 0)
        else:
            error_msg = result.get("error", "Login failed")
            return dash.no_update, dbc.Alert([
                html.I(className="fas fa-times-circle me-2"),
                f"Invalid user credentials: {error_msg}"
            ], color="danger", className="shake"), dash.no_update
    except Exception as e:
        return dash.no_update, dbc.Alert([
            html.I(className="fas fa-exclamation-triangle me-2"),
            f"Error: {str(e)}"
        ], color="danger", className="shake"), dash.no_update

@app.callback(
    Output('admin-signup-message', 'children'),
    [Input('admin-signup-button', 'n_clicks')],
    [State('admin-signup-username', 'value'),
     State('admin-signup-email', 'value'),
     State('admin-signup-password', 'value'),
     State('admin-signup-password-confirm', 'value')],
    prevent_initial_call=True
)
def handle_admin_signup(n_clicks, username, email, password, password_confirm):
    """Handle admin signup"""
    if not n_clicks or n_clicks == 0:
        return dash.no_update
    
    if not email or not password or not username:
        return dbc.Alert("Please fill in all fields", color="danger")
    
    if len(password) < 8:
        return dbc.Alert("Admin password must be at least 8 characters", color="danger")
    
    if password != password_confirm:
        return dbc.Alert("Passwords do not match", color="danger")
    
    try:
        result = auth.sign_up(email, password, username, role='admin')
        
        if result.get("success"):
            return dbc.Alert([
                html.H5("✅ Admin account created!", className="alert-heading"),
                html.P("Your admin account has been created. You can now login."),
                html.Hr(),
                html.A("Go to Admin Login", href="/admin-login", className="alert-link btn btn-danger")
            ], color="success")
        else:
            error_msg = result.get("error", "Signup failed")
            return dbc.Alert(f"Admin signup failed: {error_msg}", color="danger")
    except Exception as e:
        return dbc.Alert(f"Error: {str(e)}", color="danger")

@app.callback(
    Output('user-signup-message', 'children'),
    [Input('user-signup-button', 'n_clicks')],
    [State('user-signup-username', 'value'),
     State('user-signup-email', 'value'),
     State('user-signup-password', 'value'),
     State('user-signup-password-confirm', 'value')],
    prevent_initial_call=True
)
def handle_user_signup(n_clicks, username, email, password, password_confirm):
    """Handle user signup"""
    if not n_clicks or n_clicks == 0:
        return dash.no_update
    
    if not email or not password or not username:
        return dbc.Alert("Please fill in all fields", color="danger")
    
    if len(password) < 6:
        return dbc.Alert("Password must be at least 6 characters", color="danger")
    
    if password != password_confirm:
        return dbc.Alert("Passwords do not match", color="danger")
    
    try:
        result = auth.sign_up(email, password, username, role='user')
        
        if result.get("success"):
            return dbc.Alert([
                html.H5("✅ User account created!", className="alert-heading"),
                html.P("Your account has been created. You can now login."),
                html.Hr(),
                html.A("Go to User Login", href="/login", className="alert-link btn btn-info")
            ], color="success")
        else:
            error_msg = result.get("error", "Signup failed")
            return dbc.Alert(f"User signup failed: {error_msg}", color="danger")
    except Exception as e:
        return dbc.Alert(f"Error: {str(e)}", color="danger")

# ============================================
# RESEARCH FACTS CALLBACKS
# ============================================
# ... (omitted, no changes) ...
@app.callback(
    [Output('fact-add-message', 'children')],
    [Input('add-fact-btn', 'n_clicks')],
    [State('fact-title', 'value'),
     State('fact-description', 'value'),
     State('fact-category', 'value'),
     State('fact-source', 'value'),
     State('session-store', 'data')],
    prevent_initial_call=True
)
def add_research_fact(n_clicks, title, description, category, source, session_data):
    """Add a new research fact"""
    if not n_clicks:
        return [dash.no_update]
    
    if not title or not description:
        return [dbc.Alert("Please fill in title and description", color="danger")]
    
    try:
        session = load_session(session_data)
        user_id = session.get('user_id') if session else None
        
        if not user_id:
            return [dbc.Alert("User not authenticated", color="danger")]
        
        fact_data = {
            'fact_title': title,
            'description': description,
            'category': category or 'Other',
            'source': source or 'User Contribution',
            'user_id': user_id,
            'date_added': datetime.now().date().isoformat()
        }
        
        result = db.add_research_fact(fact_data)
        
        if result:
            return [dbc.Alert([
                html.I(className="fas fa-check-circle me-2"),
                "Research fact added successfully!"
            ], color="success")]
        else:
            return [dbc.Alert("Failed to add research fact", color="danger")]
    except Exception as e:
        return [dbc.Alert(f"Error: {str(e)}", color="danger")]

@app.callback(
    Output('research-facts-table', 'data'),
    [Input('research-facts-poll', 'n_intervals'),
     Input('fact-add-message', 'children'),
     Input('research-refresh-button', 'n_clicks')],
    prevent_initial_call=True
)
def refresh_research_facts(_n, _message, _clicks):
    try:
        facts = db.get_all_research_facts()
        return facts or []
    except Exception as e:
        print(f"Error refreshing research facts: {e}")
        return []

@app.callback(
    Output('live-utc-clock', 'children'),
    Input('clock-update', 'n_intervals')
)
def update_clock(n):
    """Update the live UTC clock"""
    from datetime import datetime
    return datetime.utcnow().strftime("%H:%M:%S")

# ============================================
# ADMIN DASHBOARD - REFRESH CALLBACKS
# ============================================
# ... (omitted, no changes) ...
def _refresh_admin_table(table_id, data_func):
    try:
        data = data_func()
        return (data or [],)
    except Exception as e:
        print(f"Error refreshing {table_id}: {e}")
        return ([],)

@app.callback(
    Output('admin-employees-table', 'data'),
    Input('btn-refresh-employees', 'n_clicks'),
    Input('admin-action-trigger', 'data')
)
def refresh_admin_employees(n_clicks, action_trigger):
    return _refresh_admin_table('admin-employees-table', db.get_all_employees)[0]

@app.callback(
    Output('admin-departments-table', 'data'),
    Input('btn-refresh-departments', 'n_clicks'),
    Input('admin-action-trigger', 'data')
)
def refresh_admin_departments(n_clicks, action_trigger):
    return _refresh_admin_table('admin-departments-table', db.get_all_departments)[0]

@app.callback(
    Output('admin-satellites-table', 'data'),
    Input('btn-refresh-satellites', 'n_clicks'),
    Input('admin-action-trigger', 'data')
)
def refresh_admin_satellites(n_clicks, action_trigger):
    return _refresh_admin_table('admin-satellites-table', db.get_all_satellites)[0]

@app.callback(
    Output('admin-missions-table', 'data'),
    Input('btn-refresh-missions', 'n_clicks'),
    Input('admin-action-trigger', 'data')
)
def refresh_admin_missions(n_clicks, action_trigger):
    return _refresh_admin_table('admin-missions-table', db.get_all_missions)[0]

@app.callback(
    Output('admin-research-facts-table', 'data'),
    Input('btn-refresh-research-facts', 'n_clicks'),
    Input('admin-action-trigger', 'data')
)
def refresh_admin_research_facts(n_clicks, action_trigger):
    return _refresh_admin_table('admin-research-facts-table', db.get_all_research_facts)[0]


# ============================================
# --- NEW CALLBACK TO FIX REFRESH ALL DATA ---
# ============================================
@app.callback(
    Output('admin-action-trigger', 'data', allow_duplicate=True),
    Input('btn-refresh-all-data', 'n_clicks'),
    State('admin-action-trigger', 'data'),
    prevent_initial_call=True
)
def handle_global_refresh(n_clicks, trigger_data):
    if not n_clicks or n_clicks == 0:
        return dash.no_update
    # Increment the trigger to fire all callbacks listening to it
    print("--- GLOBAL REFRESH TRIGGERED ---") # For debugging
    return (trigger_data or 0) + 1


# ============================================
# ADMIN DASHBOARD - EMPLOYEE CRUD
# ============================================
# ... (omitted, no changes) ...
@app.callback(
    [Output('modal-employee', 'is_open'),
     Output('employee-modal-title', 'children'),
     Output('employee-modal-store', 'data'),
     Output('input-emp-name', 'value'),
     Output('input-emp-position', 'value'),
     Output('input-emp-dept', 'value'),
     Output('input-emp-salary', 'value'),
     Output('input-emp-phone', 'value'),
     Output('input-emp-hire-date', 'date'),
     Output('employee-action-feedback', 'children')],
    [Input('btn-add-employee', 'n_clicks'),
     Input('btn-edit-employee', 'n_clicks'),
     Input('btn-save-employee', 'n_clicks'),
     Input('btn-cancel-employee', 'n_clicks')],
    [State('modal-employee', 'is_open'),
     State('admin-employees-table', 'selected_rows'),
     State('admin-employees-table', 'data')],
    prevent_initial_call=True
)
def handle_employee_modal(n_add, n_edit, n_save, n_cancel, is_open, selected_rows, table_data):
    ctx = callback_context
    if not ctx.triggered:
        return is_open, "Add Employee", {'mode': 'add', 'emp_id': None}, "", "", None, None, "", None, None

    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if trigger_id == 'btn-add-employee':
        return True, "Add New Employee", {'mode': 'add', 'emp_id': None}, "", "", None, None, "", None, None
    
    if trigger_id == 'btn-edit-employee':
        if not selected_rows:
            return is_open, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dbc.Alert("Please select an employee to edit.", color="warning")
        
        try:
            row_data = table_data[selected_rows[0]]
            emp_id = row_data.get('emp_id')
            emp_data = db.get_employee_by_id(emp_id)
            if not emp_data:
                return is_open, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dbc.Alert("Could not find employee data.", color="danger")

            return (
                True, 
                f"Edit Employee (ID: {emp_id})", 
                {'mode': 'edit', 'emp_id': emp_id},
                emp_data.get('emp_name'),
                emp_data.get('position'),
                emp_data.get('dept_id'),
                emp_data.get('salary'),
                emp_data.get('phone'),
                emp_data.get('hire_date'),
                None
            )
        except Exception as e:
            return is_open, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dbc.Alert(f"Error: {str(e)}", color="danger")

    if trigger_id in ['btn-save-employee', 'btn-cancel-employee']:
        return False, dash.no_update, dash.no_update, "", "", None, None, "", None, None
    
    return is_open, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, None

@app.callback(
    [Output('employee-action-feedback', 'children', allow_duplicate=True),
     Output('admin-action-trigger', 'data', allow_duplicate=True)],
    Input('btn-save-employee', 'n_clicks'),
    [State('employee-modal-store', 'data'),
     State('input-emp-name', 'value'),
     State('input-emp-position', 'value'),
     State('input-emp-dept', 'value'),
     State('input-emp-salary', 'value'),
     State('input-emp-phone', 'value'),
     State('input-emp-hire-date', 'date'),
     State('admin-action-trigger', 'data')],
    prevent_initial_call=True
)
def save_employee(n_clicks, store_data, name, position, dept_id, salary, phone, hire_date, trigger_data):
    if not n_clicks:
        return dash.no_update, dash.no_update
    
    if not name or not position or not dept_id or not salary or not hire_date:
        return dbc.Alert("Please fill all required fields", color="danger"), dash.no_update
    
    try:
        emp_data = {
            "emp_name": name,
            "position": position,
            "dept_id": int(dept_id),
            "salary": float(salary),
            "phone": phone,
            "hire_date": hire_date
        }
        
        mode = store_data.get('mode', 'add')
        emp_id = store_data.get('emp_id')

        if mode == 'edit' and emp_id is not None:
            result = db.update_employee(emp_id, emp_data)
            message = "Employee updated successfully"
        else:
            result = db.add_employee(emp_data)
            message = "Employee added successfully"

        if result:
            return dbc.Alert(message, color="success"), (trigger_data or 0) + 1
        else:
            return dbc.Alert("Error: Failed to save employee. Check terminal for details.", color="danger"), dash.no_update
            
    except Exception as e:
        return dbc.Alert(f"Error: {str(e)}", color="danger"), dash.no_update

@app.callback(
    [Output('modal-confirm-delete-employee', 'is_open'),
     Output('employee-delete-confirm-text', 'children')],
    [Input('btn-delete-employee', 'n_clicks'),
     Input('btn-cancel-delete-employee', 'n_clicks')],
    [State('admin-employees-table', 'selected_rows'),
     State('admin-employees-table', 'data'),
     State('modal-confirm-delete-employee', 'is_open')],
    prevent_initial_call=True
)
def toggle_employee_delete_modal(n_delete, n_cancel, selected_rows, table_data, is_open):
    ctx = callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'btn-delete-employee':
        if not selected_rows:
            return is_open, "Please select an employee to delete."
        row_data = table_data[selected_rows[0]]
        return True, f"Employee: {row_data.get('emp_name')} (ID: {row_data.get('emp_id')})"
    
    if trigger_id == 'btn-cancel-delete-employee':
        return False, ""
    
    return is_open, ""

@app.callback(
    [Output('employee-action-feedback', 'children', allow_duplicate=True),
     Output('admin-action-trigger', 'data', allow_duplicate=True),
     Output('modal-confirm-delete-employee', 'is_open', allow_duplicate=True)],
    Input('btn-confirm-delete-employee', 'n_clicks'),
    [State('admin-employees-table', 'selected_rows'),
     State('admin-employees-table', 'data'),
     State('admin-action-trigger', 'data')],
    prevent_initial_call=True
)
def confirm_delete_employee(n_clicks, selected_rows, table_data, trigger_data):
    if not n_clicks or not selected_rows:
        return dash.no_update, dash.no_update, True
    
    try:
        emp_id = table_data[selected_rows[0]].get('emp_id')
        result = db.delete_employee(emp_id)
        if result:
            return dbc.Alert("Employee deleted successfully", color="success"), (trigger_data or 0) + 1, False
        else:
            return dbc.Alert("Failed to delete employee", color="danger"), dash.no_update, True
    except Exception as e:
        return dbc.Alert(f"Error: {str(e)}", color="danger"), dash.no_update, True

# ============================================
# ADMIN DASHBOARD - DEPARTMENT CRUD
# ============================================
# ... (omitted, no changes) ...
@app.callback(
    [Output('modal-department', 'is_open'),
     Output('department-modal-title', 'children'),
     Output('department-modal-store', 'data'),
     Output('input-dept-name', 'value'),
     Output('input-dept-budget', 'value'),
     Output('input-dept-head-id', 'value'),
     Output('department-action-feedback', 'children')],
    [Input('btn-add-department', 'n_clicks'),
     Input('btn-edit-department', 'n_clicks'),
     Input('btn-save-department', 'n_clicks'),
     Input('btn-cancel-department', 'n_clicks')],
    [State('modal-department', 'is_open'),
     State('admin-departments-table', 'selected_rows'),
     State('admin-departments-table', 'data')],
    prevent_initial_call=True
)
def handle_department_modal(n_add, n_edit, n_save, n_cancel, is_open, selected_rows, table_data):
    ctx = callback_context
    if not ctx.triggered:
        return is_open, "Add Department", {'mode': 'add', 'dept_id': None}, "", None, None, None

    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if trigger_id == 'btn-add-department':
        return True, "Add New Department", {'mode': 'add', 'dept_id': None}, "", None, None, None
    
    if trigger_id == 'btn-edit-department':
        if not selected_rows:
            return is_open, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dbc.Alert("Please select a department to edit.", color="warning")
        
        row_data = table_data[selected_rows[0]]
        dept_id = row_data.get('dept_id')
        return (
            True, 
            f"Edit Department (ID: {dept_id})", 
            {'mode': 'edit', 'dept_id': dept_id},
            row_data.get('dept_name'),
            row_data.get('budget'),
            row_data.get('head_id'),
            None
        )

    if trigger_id in ['btn-save-department', 'btn-cancel-department']:
        return False, dash.no_update, dash.no_update, "", None, None, None
    
    return is_open, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, None

@app.callback(
    [Output('department-action-feedback', 'children', allow_duplicate=True),
     Output('admin-action-trigger', 'data', allow_duplicate=True)],
    Input('btn-save-department', 'n_clicks'),
    [State('department-modal-store', 'data'),
     State('input-dept-name', 'value'),
     State('input-dept-budget', 'value'),
     State('input-dept-head-id', 'value'),
     State('admin-action-trigger', 'data')],
    prevent_initial_call=True
)
def save_department(n_clicks, store_data, name, budget, head_id, trigger_data):
    if not n_clicks:
        return dash.no_update, dash.no_update
    
    if not name or budget is None:
        return dbc.Alert("Please fill Department Name and Budget", color="danger"), dash.no_update
    
    try:
        dept_data = {
            "dept_name": name,
            "budget": float(budget),
            "head_id": int(head_id) if head_id else None
        }
        
        mode = store_data.get('mode', 'add')
        dept_id = store_data.get('dept_id')

        if mode == 'edit' and dept_id is not None:
            result = db.update_department(dept_id, dept_data)
            message = "Department updated successfully"
        else:
            result = db.add_department(dept_data)
            message = "Department added successfully"

        if result:
            return dbc.Alert(message, color="success"), (trigger_data or 0) + 1
        else:
            return dbc.Alert("Error: Failed to save department.", color="danger"), dash.no_update
            
    except Exception as e:
        return dbc.Alert(f"Error: {str(e)}", color="danger"), dash.no_update

@app.callback(
    [Output('modal-confirm-delete-department', 'is_open'),
     Output('department-delete-confirm-text', 'children')],
    [Input('btn-delete-department', 'n_clicks'),
     Input('btn-cancel-delete-department', 'n_clicks')],
    [State('admin-departments-table', 'selected_rows'),
     State('admin-departments-table', 'data'),
     State('modal-confirm-delete-department', 'is_open')],
    prevent_initial_call=True
)
def toggle_department_delete_modal(n_delete, n_cancel, selected_rows, table_data, is_open):
    ctx = callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'btn-delete-department':
        if not selected_rows:
            return is_open, "Please select a department to delete."
        row_data = table_data[selected_rows[0]]
        return True, f"Department: {row_data.get('dept_name')} (ID: {row_data.get('dept_id')})"
    
    if trigger_id == 'btn-cancel-delete-department':
        return False, ""
    
    return is_open, ""

@app.callback(
    [Output('department-action-feedback', 'children', allow_duplicate=True),
     Output('admin-action-trigger', 'data', allow_duplicate=True),
     Output('modal-confirm-delete-department', 'is_open', allow_duplicate=True)],
    Input('btn-confirm-delete-department', 'n_clicks'),
    [State('admin-departments-table', 'selected_rows'),
     State('admin-departments-table', 'data'),
     State('admin-action-trigger', 'data')],
    prevent_initial_call=True
)
def confirm_delete_department(n_clicks, selected_rows, table_data, trigger_data):
    if not n_clicks or not selected_rows:
        return dash.no_update, dash.no_update, True
    
    try:
        dept_id = table_data[selected_rows[0]].get('dept_id')
        result = db.delete_department(dept_id)
        if result:
            return dbc.Alert("Department deleted successfully", color="success"), (trigger_data or 0) + 1, False
        else:
            return dbc.Alert("Failed to delete department. It might be referenced by employees.", color="danger"), dash.no_update, True
    except Exception as e:
        return dbc.Alert(f"Error: {str(e)}", color="danger"), dash.no_update, True

# ============================================
# ADMIN DASHBOARD - SATELLITE CRUD
# ============================================
# --- NEW CALLBACKS ---
@app.callback(
    [Output('modal-satellite', 'is_open'),
     Output('satellite-modal-title', 'children'),
     Output('satellite-modal-store', 'data'),
     Output('input-sat-name', 'value'),
     Output('input-sat-launch-date', 'date'),
     Output('input-sat-status', 'value'),
     Output('input-sat-orbit', 'value'),
     Output('input-sat-mass', 'value'),
     Output('input-sat-manager-id', 'value'),
     Output('satellite-action-feedback', 'children')],
    [Input('btn-add-satellite', 'n_clicks'),
     Input('btn-edit-satellite', 'n_clicks'),
     Input('btn-save-satellite', 'n_clicks'),
     Input('btn-cancel-satellite', 'n_clicks')],
    [State('modal-satellite', 'is_open'),
     State('admin-satellites-table', 'selected_rows'),
     State('admin-satellites-table', 'data')],
    prevent_initial_call=True
)
def handle_satellite_modal(n_add, n_edit, n_save, n_cancel, is_open, selected_rows, table_data):
    ctx = callback_context
    if not ctx.triggered:
        return is_open, "Add Satellite", {'mode': 'add', 'sat_id': None}, "", None, None, "", None, None, None

    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if trigger_id == 'btn-add-satellite':
        return True, "Add New Satellite", {'mode': 'add', 'sat_id': None}, "", None, None, "", None, None, None
    
    if trigger_id == 'btn-edit-satellite':
        if not selected_rows:
            return is_open, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dbc.Alert("Please select a satellite to edit.", color="warning")
        
        try:
            row_data = table_data[selected_rows[0]]
            sat_id = row_data.get('sat_id')
            sat_data = db.get_satellite_by_id(sat_id) # Need full data
            if not sat_data:
                return is_open, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dbc.Alert("Could not find satellite data.", color="danger")
            
            return (
                True,
                f"Edit Satellite (ID: {sat_id})",
                {'mode': 'edit', 'sat_id': sat_id},
                sat_data.get('sat_name'),
                sat_data.get('launch_date'),
                sat_data.get('status'),
                sat_data.get('orbit_type'),
                sat_data.get('mass'),
                sat_data.get('manager_id'),
                None
            )
        except Exception as e:
            return is_open, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dbc.Alert(f"Error: {str(e)}", color="danger")

    if trigger_id in ['btn-save-satellite', 'btn-cancel-satellite']:
        return False, dash.no_update, dash.no_update, "", None, None, "", None, None, None
    
    return is_open, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, None

@app.callback(
    [Output('satellite-action-feedback', 'children', allow_duplicate=True),
     Output('admin-action-trigger', 'data', allow_duplicate=True)],
    Input('btn-save-satellite', 'n_clicks'),
    [State('satellite-modal-store', 'data'),
     State('input-sat-name', 'value'),
     State('input-sat-launch-date', 'date'),
     State('input-sat-status', 'value'),
     State('input-sat-orbit', 'value'),
     State('input-sat-mass', 'value'),
     State('input-sat-manager-id', 'value'),
     State('admin-action-trigger', 'data')],
    prevent_initial_call=True
)
def save_satellite(n_clicks, store_data, name, launch_date, status, orbit, mass, manager_id, trigger_data):
    if not n_clicks:
        return dash.no_update, dash.no_update
    
    if not name or not launch_date or not status or not orbit or not mass:
        return dbc.Alert("Please fill all required fields", color="danger"), dash.no_update
    
    try:
        sat_data = {
            "sat_name": name,
            "launch_date": launch_date,
            "status": status,
            "orbit_type": orbit,
            "mass": float(mass),
            "manager_id": int(manager_id) if manager_id else None
        }
        
        mode = store_data.get('mode', 'add')
        sat_id = store_data.get('sat_id')

        if mode == 'edit' and sat_id is not None:
            result = db.update_satellite(sat_id, sat_data)
            message = "Satellite updated successfully"
        else:
            result = db.add_satellite(sat_data)
            message = "Satellite added successfully"

        if result:
            return dbc.Alert(message, color="success"), (trigger_data or 0) + 1
        else:
            return dbc.Alert("Error: Failed to save satellite.", color="danger"), dash.no_update
            
    except Exception as e:
        return dbc.Alert(f"Error: {str(e)}", color="danger"), dash.no_update

@app.callback(
    [Output('modal-confirm-delete-satellite', 'is_open'),
     Output('satellite-delete-confirm-text', 'children')],
    [Input('btn-delete-satellite', 'n_clicks'),
     Input('btn-cancel-delete-satellite', 'n_clicks')],
    [State('admin-satellites-table', 'selected_rows'),
     State('admin-satellites-table', 'data'),
     State('modal-confirm-delete-satellite', 'is_open')],
    prevent_initial_call=True
)
def toggle_satellite_delete_modal(n_delete, n_cancel, selected_rows, table_data, is_open):
    ctx = callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'btn-delete-satellite':
        if not selected_rows:
            return is_open, "Please select a satellite to delete."
        row_data = table_data[selected_rows[0]]
        return True, f"Satellite: {row_data.get('sat_name')} (ID: {row_data.get('sat_id')})"
    
    if trigger_id == 'btn-cancel-delete-satellite':
        return False, ""
    
    return is_open, ""

@app.callback(
    [Output('satellite-action-feedback', 'children', allow_duplicate=True),
     Output('admin-action-trigger', 'data', allow_duplicate=True),
     Output('modal-confirm-delete-satellite', 'is_open', allow_duplicate=True)],
    Input('btn-confirm-delete-satellite', 'n_clicks'),
    [State('admin-satellites-table', 'selected_rows'),
     State('admin-satellites-table', 'data'),
     State('admin-action-trigger', 'data')],
    prevent_initial_call=True
)
def confirm_delete_satellite(n_clicks, selected_rows, table_data, trigger_data):
    if not n_clicks or not selected_rows:
        return dash.no_update, dash.no_update, True
    
    try:
        sat_id = table_data[selected_rows[0]].get('sat_id')
        result = db.delete_satellite(sat_id)
        if result:
            return dbc.Alert("Satellite deleted successfully", color="success"), (trigger_data or 0) + 1, False
        else:
            return dbc.Alert("Failed to delete satellite. It might be referenced elsewhere.", color="danger"), dash.no_update, True
    except Exception as e:
        return dbc.Alert(f"Error: {str(e)}", color="danger"), dash.no_update, True

# ============================================
# ADMIN DASHBOARD - MISSION CRUD
# ============================================
# --- NEW CALLBACKS ---
@app.callback(
    [Output('modal-mission', 'is_open'),
     Output('mission-modal-title', 'children'),
     Output('mission-modal-store', 'data'),
     Output('input-mission-name', 'value'),
     Output('input-mission-id', 'value'),
     Output('input-mission-pad-id', 'value'),
     Output('input-mission-loc-id', 'value'),
     Output('input-mission-status', 'value'),
     Output('input-mission-launch-date', 'date'),
     Output('input-mission-budget', 'value'),
     Output('input-mission-id', 'disabled'),
     Output('input-mission-pad-id', 'disabled'),
     Output('input-mission-loc-id', 'disabled'),
     Output('mission-action-feedback', 'children')],
    [Input('btn-add-mission', 'n_clicks'),
     Input('btn-edit-mission', 'n_clicks'),
     Input('btn-save-mission', 'n_clicks'),
     Input('btn-cancel-mission', 'n_clicks')],
    [State('modal-mission', 'is_open'),
     State('admin-missions-table', 'selected_rows'),
     State('admin-missions-table', 'data')],
    prevent_initial_call=True
)
def handle_mission_modal(n_add, n_edit, n_save, n_cancel, is_open, selected_rows, table_data):
    ctx = callback_context
    if not ctx.triggered:
        return is_open, "Add Mission", {'mode': 'add', 'ids': None}, "", None, None, None, None, None, None, False, False, False, None

    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if trigger_id == 'btn-add-mission':
        return True, "Add New Mission", {'mode': 'add', 'ids': None}, "", None, None, None, None, None, None, False, False, False, None
    
    if trigger_id == 'btn-edit-mission':
        if not selected_rows:
            return is_open, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dbc.Alert("Please select a mission to edit.", color="warning")
        
        try:
            row_data = table_data[selected_rows[0]]
            ids = {
                'mission_id': row_data.get('mission_id'),
                'pad_id': row_data.get('pad_id'),
                'loc_id': row_data.get('loc_id')
            }
            mission_data = db.get_mission_by_id(ids['mission_id'], ids['pad_id'], ids['loc_id'])
            if not mission_data:
                return is_open, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dbc.Alert("Could not find mission data.", color="danger")
            
            return (
                True,
                f"Edit Mission (ID: {ids['mission_id']})",
                {'mode': 'edit', 'ids': ids},
                mission_data.get('mission_name'),
                mission_data.get('mission_id'),
                mission_data.get('pad_id'),
                mission_data.get('loc_id'),
                mission_data.get('status'),
                mission_data.get('launch_date'),
                mission_data.get('budget'),
                True, True, True, # Disable composite key fields
                None
            )
        except Exception as e:
            return is_open, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dbc.Alert(f"Error: {str(e)}", color="danger")

    if trigger_id in ['btn-save-mission', 'btn-cancel-mission']:
        return False, dash.no_update, dash.no_update, "", None, None, None, None, None, None, False, False, False, None
    
    return is_open, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, None

@app.callback(
    [Output('mission-action-feedback', 'children', allow_duplicate=True),
     Output('admin-action-trigger', 'data', allow_duplicate=True)],
    Input('btn-save-mission', 'n_clicks'),
    [State('mission-modal-store', 'data'),
     State('input-mission-name', 'value'),
     State('input-mission-id', 'value'),
     State('input-mission-pad-id', 'value'),
     State('input-mission-loc-id', 'value'),
     State('input-mission-status', 'value'),
     State('input-mission-launch-date', 'date'),
     State('input-mission-budget', 'value'),
     State('admin-action-trigger', 'data')],
    prevent_initial_call=True
)
def save_mission(n_clicks, store_data, name, mission_id, pad_id, loc_id, status, launch_date, budget, trigger_data):
    if not n_clicks:
        return dash.no_update, dash.no_update
    
    if not name or not mission_id or not pad_id or not loc_id or not status or not launch_date or not budget:
        return dbc.Alert("Please fill all required fields", color="danger"), dash.no_update
    
    try:
        mission_data = {
            "mission_name": name,
            "status": status,
            "launch_date": launch_date,
            "budget": float(budget),
        }
        
        mode = store_data.get('mode', 'add')
        ids = store_data.get('ids')

        if mode == 'edit' and ids is not None:
            result = db.update_mission(ids['mission_id'], ids['pad_id'], ids['loc_id'], mission_data)
            message = "Mission updated successfully"
        else:
            mission_data['mission_id'] = int(mission_id)
            mission_data['pad_id'] = int(pad_id)
            mission_data['loc_id'] = int(loc_id)
            result = db.add_mission(mission_data)
            message = "Mission added successfully"

        if result:
            return dbc.Alert(message, color="success"), (trigger_data or 0) + 1
        else:
            return dbc.Alert("Error: Failed to save mission. Check IDs are unique.", color="danger"), dash.no_update
            
    except Exception as e:
        return dbc.Alert(f"Error: {str(e)}", color="danger"), dash.no_update

@app.callback(
    [Output('modal-confirm-delete-mission', 'is_open'),
     Output('mission-delete-confirm-text', 'children')],
    [Input('btn-delete-mission', 'n_clicks'),
     Input('btn-cancel-delete-mission', 'n_clicks')],
    [State('admin-missions-table', 'selected_rows'),
     State('admin-missions-table', 'data'),
     State('modal-confirm-delete-mission', 'is_open')],
    prevent_initial_call=True
)
def toggle_mission_delete_modal(n_delete, n_cancel, selected_rows, table_data, is_open):
    ctx = callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'btn-delete-mission':
        if not selected_rows:
            return is_open, "Please select a mission to delete."
        row_data = table_data[selected_rows[0]]
        return True, f"Mission: {row_data.get('mission_name')} (ID: {row_data.get('mission_id')})"
    
    if trigger_id == 'btn-cancel-delete-mission':
        return False, ""
    
    return is_open, ""

@app.callback(
    [Output('mission-action-feedback', 'children', allow_duplicate=True),
     Output('admin-action-trigger', 'data', allow_duplicate=True),
     Output('modal-confirm-delete-mission', 'is_open', allow_duplicate=True)],
    Input('btn-confirm-delete-mission', 'n_clicks'),
    [State('admin-missions-table', 'selected_rows'),
     State('admin-missions-table', 'data'),
     State('admin-action-trigger', 'data')],
    prevent_initial_call=True
)
def confirm_delete_mission(n_clicks, selected_rows, table_data, trigger_data):
    if not n_clicks or not selected_rows:
        return dash.no_update, dash.no_update, True
    
    try:
        row_data = table_data[selected_rows[0]]
        mission_id = row_data.get('mission_id')
        pad_id = row_data.get('pad_id')
        loc_id = row_data.get('loc_id')

        result = db.delete_mission(mission_id, pad_id, loc_id)
        if result:
            return dbc.Alert("Mission deleted successfully", color="success"), (trigger_data or 0) + 1, False
        else:
            return dbc.Alert("Failed to delete mission.", color="danger"), dash.no_update, True
    except Exception as e:
        return dbc.Alert(f"Error: {str(e)}", color="danger"), dash.no_update, True

# ============================================
# ADMIN DASHBOARD - RESEARCH FACT DELETE
# ============================================
# ... (omitted, no changes) ...
@app.callback(
    [Output('modal-confirm-delete-research-fact', 'is_open'),
     Output('research-fact-delete-confirm-text', 'children')],
    [Input('btn-delete-research-fact', 'n_clicks'),
     Input('btn-cancel-delete-research-fact', 'n_clicks')],
    [State('admin-research-facts-table', 'selected_rows'),
     State('admin-research-facts-table', 'data'),
     State('modal-confirm-delete-research-fact', 'is_open')],
    prevent_initial_call=True
)
def toggle_research_fact_delete_modal(n_delete, n_cancel, selected_rows, table_data, is_open):
    ctx = callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'btn-delete-research-fact':
        if not selected_rows:
            return is_open, "Please select a fact to delete."
        row_data = table_data[selected_rows[0]]
        return True, f"Fact: {row_data.get('fact_title')} (ID: {row_data.get('fact_id')})"
    
    if trigger_id == 'btn-cancel-delete-research-fact':
        return False, ""
    
    return is_open, ""

@app.callback(
    [Output('research-fact-action-feedback', 'children'),
     Output('admin-action-trigger', 'data', allow_duplicate=True),
     Output('modal-confirm-delete-research-fact', 'is_open', allow_duplicate=True)],
    Input('btn-confirm-delete-research-fact', 'n_clicks'),
    [State('admin-research-facts-table', 'selected_rows'),
     State('admin-research-facts-table', 'data'),
     State('admin-action-trigger', 'data')],
    prevent_initial_call=True
)
def confirm_delete_research_fact(n_clicks, selected_rows, table_data, trigger_data):
    if not n_clicks or not selected_rows:
        return dash.no_update, dash.no_update, True
    
    try:
        selected_row_data = table_data[selected_rows[0]]
        fact_id = selected_row_data.get('fact_id')
        user_id = selected_row_data.get('user_id')
        
        if not fact_id or not user_id:
            return dbc.Alert("Invalid row data", color="danger"), dash.no_update

        db.delete_research_fact(fact_id, user_id)
        
        return dbc.Alert("Research fact deleted successfully", color="success"), (trigger_data or 0) + 1, False
    except Exception as e:
        return dbc.Alert(f"Error: {str(e)}", color="danger"), dash.no_update, True

# ============================================
# SATELLITES PAGE CRUD
# ============================================
# --- NEW CALLBACKS ---
@app.callback(
    Output('satellites-table', 'data'),
    Input('page-satellite-action-trigger', 'data')
)
def refresh_page_satellites_table(action_trigger):
    return _refresh_admin_table('satellites-table', db.get_all_satellites)[0]

@app.callback(
    [Output('page-modal-satellite', 'is_open'),
     Output('page-satellite-modal-title', 'children'),
     Output('page-satellite-modal-store', 'data'),
     Output('page-input-sat-name', 'value'),
     Output('page-input-sat-launch-date', 'date'),
     Output('page-input-sat-status', 'value'),
     Output('page-input-sat-orbit', 'value'),
     Output('page-input-sat-mass', 'value'),
     Output('page-input-sat-manager-id', 'value'),
     Output('page-satellite-feedback', 'children')],
    [Input('page-add-satellite-btn', 'n_clicks'),
     Input('page-edit-satellite-btn', 'n_clicks'),
     Input('page-save-satellite-btn', 'n_clicks'),
     Input('page-cancel-satellite-btn', 'n_clicks')],
    [State('page-modal-satellite', 'is_open'),
     State('satellites-table', 'selected_rows'),
     State('satellites-table', 'data')],
    prevent_initial_call=True
)
def handle_page_satellite_modal(n_add, n_edit, n_save, n_cancel, is_open, selected_rows, table_data):
    ctx = callback_context
    if not ctx.triggered:
        return is_open, "Add Satellite", {'mode': 'add', 'sat_id': None}, "", None, None, "", None, None, None

    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if trigger_id == 'page-add-satellite-btn':
        return True, "Add New Satellite", {'mode': 'add', 'sat_id': None}, "", None, None, "", None, None, None
    
    if trigger_id == 'page-edit-satellite-btn':
        if not selected_rows:
            return is_open, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dbc.Alert("Please select a satellite to edit.", color="warning")
        
        try:
            row_data = table_data[selected_rows[0]]
            sat_id = row_data.get('sat_id')
            sat_data = db.get_satellite_by_id(sat_id)
            if not sat_data:
                return is_open, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dbc.Alert("Could not find satellite data.", color="danger")
            
            return (
                True,
                f"Edit Satellite (ID: {sat_id})",
                {'mode': 'edit', 'sat_id': sat_id},
                sat_data.get('sat_name'),
                sat_data.get('launch_date'),
                sat_data.get('status'),
                sat_data.get('orbit_type'),
                sat_data.get('mass'),
                sat_data.get('manager_id'),
                None
            )
        except Exception as e:
            return is_open, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dbc.Alert(f"Error: {str(e)}", color="danger")

    if trigger_id in ['page-save-satellite-btn', 'page-cancel-satellite-btn']:
        return False, dash.no_update, dash.no_update, "", None, None, "", None, None, None
    
    return is_open, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, None

@app.callback(
    [Output('page-satellite-feedback', 'children', allow_duplicate=True),
     Output('satellites-table', 'data', allow_duplicate=True)],
    Input('page-save-satellite-btn', 'n_clicks'),
    [State('page-satellite-modal-store', 'data'),
     State('page-input-sat-name', 'value'),
     State('page-input-sat-launch-date', 'date'),
     State('page-input-sat-status', 'value'),
     State('page-input-sat-orbit', 'value'),
     State('page-input-sat-mass', 'value'),
     State('page-input-sat-manager-id', 'value')],
    prevent_initial_call=True
)
def save_page_satellite(n_clicks, store_data, name, launch_date, status, orbit, mass, manager_id):
    if not n_clicks:
        return dash.no_update, dash.no_update
    
    if not name or not launch_date or not status or not orbit or not mass:
        return dbc.Alert("Please fill all required fields", color="danger"), dash.no_update
    
    try:
        sat_data = {
            "sat_name": name,
            "launch_date": launch_date,
            "status": status,
            "orbit_type": orbit,
            "mass": float(mass),
            "manager_id": int(manager_id) if manager_id else None
        }
        
        mode = store_data.get('mode', 'add')
        sat_id = store_data.get('sat_id')

        if mode == 'edit' and sat_id is not None:
            result = db.update_satellite(sat_id, sat_data)
            message = "Satellite updated successfully"
        else:
            result = db.add_satellite(sat_data)
            message = "Satellite added successfully"

        if result:
            new_data = db.get_all_satellites()
            return dbc.Alert(message, color="success"), new_data
        else:
            return dbc.Alert("Error: Failed to save satellite.", color="danger"), dash.no_update
            
    except Exception as e:
        return dbc.Alert(f"Error: {str(e)}", color="danger"), dash.no_update

@app.callback(
    [Output('page-modal-confirm-delete-satellite', 'is_open'),
     Output('page-satellite-delete-confirm-text', 'children')],
    [Input('page-delete-satellite-btn', 'n_clicks'),
     Input('page-cancel-delete-satellite-btn', 'n_clicks')],
    [State('satellites-table', 'selected_rows'),
     State('satellites-table', 'data'),
     State('page-modal-confirm-delete-satellite', 'is_open')],
    prevent_initial_call=True
)
def toggle_page_satellite_delete_modal(n_delete, n_cancel, selected_rows, table_data, is_open):
    ctx = callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'page-delete-satellite-btn':
        if not selected_rows:
            return is_open, "Please select a satellite to delete."
        row_data = table_data[selected_rows[0]]
        return True, f"Satellite: {row_data.get('sat_name')} (ID: {row_data.get('sat_id')})"
    
    if trigger_id == 'page-cancel-delete-satellite-btn':
        return False, ""
    
    return is_open, ""

@app.callback(
    [Output('page-satellite-feedback', 'children', allow_duplicate=True),
     Output('satellites-table', 'data', allow_duplicate=True),
     Output('page-modal-confirm-delete-satellite', 'is_open', allow_duplicate=True)],
    Input('page-confirm-delete-satellite-btn', 'n_clicks'),
    [State('satellites-table', 'selected_rows'),
     State('satellites-table', 'data')],
    prevent_initial_call=True
)
def confirm_page_delete_satellite(n_clicks, selected_rows, table_data):
    if not n_clicks or not selected_rows:
        return dash.no_update, dash.no_update, True
    
    try:
        sat_id = table_data[selected_rows[0]].get('sat_id')
        result = db.delete_satellite(sat_id)
        if result:
            new_data = db.get_all_satellites()
            return dbc.Alert("Satellite deleted successfully", color="success"), new_data, False
        else:
            return dbc.Alert("Failed to delete satellite. It might be referenced elsewhere.", color="danger"), dash.no_update, True
    except Exception as e:
        return dbc.Alert(f"Error: {str(e)}", color="danger"), dash.no_update, True

# ============================================
# MISSIONS PAGE CRUD
# ============================================
# --- NEW CALLBACKS ---
@app.callback(
    Output('missions-table', 'data'),
    Input('page-mission-action-trigger', 'data')
)
def refresh_page_missions_table(action_trigger):
    return _refresh_admin_table('missions-table', db.get_all_missions)[0]

@app.callback(
    [Output('page-modal-mission', 'is_open'),
     Output('page-mission-modal-title', 'children'),
     Output('page-mission-modal-store', 'data'),
     Output('page-input-mission-name', 'value'),
     Output('page-input-mission-id', 'value'),
     Output('page-input-mission-pad-id', 'value'),
     Output('page-input-mission-loc-id', 'value'),
     Output('page-input-mission-status', 'value'),
     Output('page-input-mission-launch-date', 'date'),
     Output('page-input-mission-budget', 'value'),
     Output('page-input-mission-id', 'disabled'),
     Output('page-input-mission-pad-id', 'disabled'),
     Output('page-input-mission-loc-id', 'disabled'),
     Output('page-mission-feedback', 'children')],
    [Input('page-add-mission-btn', 'n_clicks'),
     Input('page-edit-mission-btn', 'n_clicks'),
     Input('page-save-mission-btn', 'n_clicks'),
     Input('page-cancel-mission-btn', 'n_clicks')],
    [State('page-modal-mission', 'is_open'),
     State('missions-table', 'selected_rows'),
     State('missions-table', 'data')],
    prevent_initial_call=True
)
def handle_page_mission_modal(n_add, n_edit, n_save, n_cancel, is_open, selected_rows, table_data):
    ctx = callback_context
    if not ctx.triggered:
        return is_open, "Add Mission", {'mode': 'add', 'ids': None}, "", None, None, None, None, None, None, False, False, False, None

    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if trigger_id == 'page-add-mission-btn':
        return True, "Add New Mission", {'mode': 'add', 'ids': None}, "", None, None, None, None, None, None, False, False, False, None
    
    if trigger_id == 'page-edit-mission-btn':
        if not selected_rows:
            return is_open, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dbc.Alert("Please select a mission to edit.", color="warning")
        
        try:
            row_data = table_data[selected_rows[0]]
            ids = {
                'mission_id': row_data.get('mission_id'),
                'pad_id': row_data.get('pad_id'),
                'loc_id': row_data.get('loc_id')
            }
            mission_data = db.get_mission_by_id(ids['mission_id'], ids['pad_id'], ids['loc_id'])
            if not mission_data:
                return is_open, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dbc.Alert("Could not find mission data.", color="danger")
            
            return (
                True,
                f"Edit Mission (ID: {ids['mission_id']})",
                {'mode': 'edit', 'ids': ids},
                mission_data.get('mission_name'),
                mission_data.get('mission_id'),
                mission_data.get('pad_id'),
                mission_data.get('loc_id'),
                mission_data.get('status'),
                mission_data.get('launch_date'),
                mission_data.get('budget'),
                True, True, True, # Disable composite key fields
                None
            )
        except Exception as e:
            return is_open, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dbc.Alert(f"Error: {str(e)}", color="danger")

    if trigger_id in ['page-save-mission-btn', 'page-cancel-mission-btn']:
        return False, dash.no_update, dash.no_update, "", None, None, None, None, None, None, False, False, False, None
    
    return is_open, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, None

@app.callback(
    [Output('page-mission-feedback', 'children', allow_duplicate=True),
     Output('missions-table', 'data', allow_duplicate=True)],
    Input('page-save-mission-btn', 'n_clicks'),
    [State('page-mission-modal-store', 'data'),
     State('page-input-mission-name', 'value'),
     State('page-input-mission-id', 'value'),
     State('page-input-mission-pad-id', 'value'),
     State('page-input-mission-loc-id', 'value'),
     State('page-input-mission-status', 'value'),
     State('page-input-mission-launch-date', 'date'),
     State('page-input-mission-budget', 'value')],
    prevent_initial_call=True
)
def save_page_mission(n_clicks, store_data, name, mission_id, pad_id, loc_id, status, launch_date, budget):
    if not n_clicks:
        return dash.no_update, dash.no_update
    
    if not name or not mission_id or not pad_id or not loc_id or not status or not launch_date or not budget:
        return dbc.Alert("Please fill all required fields", color="danger"), dash.no_update
    
    try:
        mission_data = {
            "mission_name": name,
            "status": status,
            "launch_date": launch_date,
            "budget": float(budget),
        }
        
        mode = store_data.get('mode', 'add')
        ids = store_data.get('ids')

        if mode == 'edit' and ids is not None:
            result = db.update_mission(ids['mission_id'], ids['pad_id'], ids['loc_id'], mission_data)
            message = "Mission updated successfully"
        else:
            mission_data['mission_id'] = int(mission_id)
            mission_data['pad_id'] = int(pad_id)
            mission_data['loc_id'] = int(loc_id)
            result = db.add_mission(mission_data)
            message = "Mission added successfully"

        if result:
            new_data = db.get_all_missions()
            return dbc.Alert(message, color="success"), new_data
        else:
            return dbc.Alert("Error: Failed to save mission. Check IDs are unique.", color="danger"), dash.no_update
            
    except Exception as e:
        return dbc.Alert(f"Error: {str(e)}", color="danger"), dash.no_update

@app.callback(
    [Output('page-modal-confirm-delete-mission', 'is_open'),
     Output('page-mission-delete-confirm-text', 'children')],
    [Input('page-delete-mission-btn', 'n_clicks'),
     Input('page-cancel-delete-mission-btn', 'n_clicks')],
    [State('missions-table', 'selected_rows'),
     State('missions-table', 'data'),
     State('page-modal-confirm-delete-mission', 'is_open')],
    prevent_initial_call=True
)
def toggle_page_mission_delete_modal(n_delete, n_cancel, selected_rows, table_data, is_open):
    ctx = callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'page-delete-mission-btn':
        if not selected_rows:
            return is_open, "Please select a mission to delete."
        row_data = table_data[selected_rows[0]]
        return True, f"Mission: {row_data.get('mission_name')} (ID: {row_data.get('mission_id')})"
    
    if trigger_id == 'page-cancel-delete-mission-btn':
        return False, ""
    
    return is_open, ""

@app.callback(
    [Output('page-mission-feedback', 'children', allow_duplicate=True),
     Output('missions-table', 'data', allow_duplicate=True),
     Output('page-modal-confirm-delete-mission', 'is_open', allow_duplicate=True)],
    Input('page-confirm-delete-mission-btn', 'n_clicks'),
    [State('missions-table', 'selected_rows'),
     State('missions-table', 'data')],
    prevent_initial_call=True
)
def confirm_page_delete_mission(n_clicks, selected_rows, table_data):
    if not n_clicks or not selected_rows:
        return dash.no_update, dash.no_update, True
    
    try:
        row_data = table_data[selected_rows[0]]
        mission_id = row_data.get('mission_id')
        pad_id = row_data.get('pad_id')
        loc_id = row_data.get('loc_id')

        result = db.delete_mission(mission_id, pad_id, loc_id)
        if result:
            new_data = db.get_all_missions()
            return dbc.Alert("Mission deleted successfully", color="success"), new_data, False
        else:
            return dbc.Alert("Failed to delete mission.", color="danger"), dash.no_update, True
    except Exception as e:
        return dbc.Alert(f"Error: {str(e)}", color="danger"), dash.no_update, True

# ============================================
# ANALYTICS PAGE CALLBACKS
# ============================================
# --- NEW CALLBACKS ---
@app.callback(
    Output('nested-query-table', 'data'),
    Input('run-nested-query-btn', 'n_clicks'),
    prevent_initial_call=True
)
def run_nested_query(n_clicks):
    if n_clicks:
        data = db.get_employees_above_avg_salary()
        return data
    return dash.no_update

@app.callback(
    Output('analytics-proc-output', 'children'),
    Input('analytics-run-proc-btn', 'n_clicks'),
    State('analytics-emp-id-input', 'value'),
    prevent_initial_call=True
)
def run_employee_procedures(n_clicks, emp_id):
    if not n_clicks or not emp_id:
        return dbc.Alert("Please enter an Employee ID.", color="warning")
    
    try:
        emp_id = int(emp_id)
        details = db.call_get_employee_details(emp_id)
        years = db.call_get_years_of_service(emp_id)
        subs = db.call_count_subordinates(emp_id)

        if not details:
            return dbc.Alert(f"No employee found with ID {emp_id}", color="danger")
        
        data = details[0]
        
        return dbc.Card([
            dbc.CardBody([
                html.H4(data.get('emp_name'), className="mb-0"),
                html.P(data.get('position'), className="text-info"),
                html.Hr(),
                html.P(f"Department: {data.get('dept_name')}", className="mb-1"),
                html.P(f"Supervisor: {data.get('supervisor_name')}", className="mb-1"),
                html.P(f"Salary: ${data.get('salary'):,.0f}", className="mb-1"),
                html.P(f"Hire Date: {data.get('hire_date')}", className="mb-1"),
                html.P(f"Years of Service: {years}", className="mb-1"),
                html.P(f"Subordinates: {subs}", className="mb-1"),
                html.P(f"Satellites Managed: {data.get('satellites_managed')}", className="mb-1"),
            ])
        ], className="stat-card")

    except Exception as e:
        return dbc.Alert(f"Error: {str(e)}", color="danger")

@app.callback(
    Output('analytics-report-table', 'data'),
    Input('analytics-run-report-btn', 'n_clicks'),
    prevent_initial_call=True
)
def run_salary_report(n_clicks):
    if n_clicks:
        data = db.call_generate_salary_report()
        return data
    return dash.no_update

# ============================================
# CLIENTSIDE CALLBACKS
# ============================================
# ... (omitted, no changes) ...
app.clientside_callback(
    """
    function(n_clicks) {
        if (!n_clicks) return window.dash_clientside.no_update;
        
        const passwordInput = document.getElementById('login-password');
        const icon = document.getElementById('password-toggle-icon');
        
        if (passwordInput && icon) {
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                icon.className = 'fas fa-eye-slash';
            } else {
                passwordInput.type = 'password';
                icon.className = 'fas fa-eye';
            }
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output('password-toggle', 'n_clicks'),
    Input('password-toggle', 'n_clicks'),
    prevent_initial_call=True
)

app.clientside_callback(
    """
    function(n_intervals) {
        if (n_intervals === 0) {
            const statElements = document.querySelectorAll('.stat-value[data-target]');
            statElements.forEach(element => {
                const target = parseInt(element.getAttribute('data-target')) || 0;
                let current = 0;
                const increment = target / 50;
                const timer = setInterval(() => {
                    current += increment;
                    if (current >= target) {
                        element.textContent = target;
                        clearInterval(timer);
                    } else {
                        element.textContent = Math.floor(current);
                    }
                }, 30);
            });
        }
        return null;
    }
    """,
    Output('missions-count', 'data-animated'),
    Input('clock-update', 'n_intervals')
)

# ============================================
# RUN APP
# ============================================

if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port=8050)