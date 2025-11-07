from dash import html, dcc
import dash_bootstrap_components as dbc

def admin_signup_page():
    """Admin signup page with red theme"""
    return html.Div([
        # Shooting stars effect
        html.Div(className="shooting-star", style={"top": "15%", "left": "25%", "animationDelay": "1s"}),
        html.Div(className="shooting-star", style={"top": "50%", "left": "75%", "animationDelay": "3s"}),
        
        # Main signup container
        html.Div([
            # Glassmorphic signup card
            html.Div([
                # Logo/Icon
                html.Div([
                    html.I(className="fas fa-user-shield fa-4x mb-3", style={
                        "color": "#ef4444",
                        "textShadow": "0 0 40px rgba(239, 68, 68, 0.8)"
                    }),
                ], className="text-center"),
                
                # Title
                html.H2("ADMIN REGISTRATION", className="login-title", style={
                    "background": "linear-gradient(135deg, #ef4444, #dc2626)",
                    "-webkit-background-clip": "text",
                    "-webkit-text-fill-color": "transparent"
                }),
                html.P("Administrator Authorization Request", className="login-subtitle"),
                
                # Warning badge
                html.Div([
                    html.Span([
                        html.I(className="fas fa-exclamation-triangle me-2"),
                        "ADMINs HAVE FULL SYSTEM CONTROL"
                    ], className="badge w-100 mb-3 py-2", style={
                        "background": "rgba(239, 68, 68, 0.2)",
                        "color": "#ef4444",
                        "border": "1px solid #ef4444",
                        "fontSize": "0.875rem"
                    })
                ]),
                
                # Message area
                html.Div(id="admin-signup-message", className="mb-3"),
                
                # Username input
                html.Div([
                    dbc.Label([
                        html.I(className="fas fa-user-cog me-2"),
                        "Admin Username"
                    ], html_for="admin-signup-username", className="form-label"),
                    dbc.Input(
                        id="admin-signup-username",
                        type="text",
                        placeholder="Choose admin username",
                        className="form-control",
                        autoFocus=True,
                        n_submit=0
                    ),
                ], className="mb-3"),
                
                # Email input
                html.Div([
                    dbc.Label([
                        html.I(className="fas fa-envelope me-2"),
                        "Admin Email"
                    ], html_for="admin-signup-email", className="form-label"),
                    dbc.Input(
                        id="admin-signup-email",
                        type="email",
                        placeholder="admin@space.mission",
                        className="form-control",
                        autoComplete="email",
                        n_submit=0
                    ),
                ], className="mb-3"),
                
                # Password input
                html.Div([
                    dbc.Label([
                        html.I(className="fas fa-lock me-2"),
                        "Admin Access Code"
                    ], html_for="admin-signup-password", className="form-label"),
                    dbc.Input(
                        id="admin-signup-password",
                        type="password",
                        placeholder="Minimum 8 characters (admin)",
                        className="form-control",
                        n_submit=0
                    ),
                ], className="mb-3"),
                
                # Confirm password input
                html.Div([
                    dbc.Label([
                        html.I(className="fas fa-lock me-2"),
                        "Confirm Access Code"
                    ], html_for="admin-signup-password-confirm", className="form-label"),
                    dbc.Input(
                        id="admin-signup-password-confirm",
                        type="password",
                        placeholder="Re-enter admin access code",
                        className="form-control",
                        n_submit=0
                    ),
                ], className="mb-4"),
                
                # Terms acceptance
                html.Div([
                    dbc.Checkbox(
                        id="admin-accept-terms",
                        label=[
                            "I acknowledge ",
                            html.Span("full administrative responsibilities", className="text-danger fw-bold"),
                            " and system control"
                        ],
                        value=False,
                        className="text-secondary"
                    ),
                ], className="mb-4"),
                
                # Signup button
                dbc.Button(
                    [
                        html.Span("REQUEST ADMIN ACCESS", id="admin-signup-button-text"),
                        html.I(className="fas fa-shield-alt ms-2", id="admin-signup-button-icon"),
                    ],
                    id="admin-signup-button",
                    className="w-100 mb-3",
                    size="lg",
                    n_clicks=0,
                    style={
                        "background": "linear-gradient(135deg, #ef4444, #dc2626)",
                        "border": "none"
                    }
                ),
                
                # Divider
                html.Div([
                    html.Hr(className="my-4", style={"borderColor": "rgba(255,255,255,0.1)"}),
                ]),
                
                # Links
                html.Div([
                    html.P([
                        html.A([
                            html.I(className="fas fa-sign-in-alt me-2"),
                            "Admin Login"
                        ], href="/admin-login", className="text-danger", style={
                            "textDecoration": "none",
                            "borderBottom": "1px solid currentColor"
                        }),
                        html.Span(" | ", className="text-secondary mx-2"),
                        html.A([
                            html.I(className="fas fa-user me-2"),
                            "User Signup"
                        ], href="/user-signup", className="text-info", style={
                            "textDecoration": "none",
                            "borderBottom": "1px solid currentColor"
                        })
                    ], className="text-center mb-0"),
                ]),
                
            ], className="login-card", style={"border": "1px solid rgba(239, 68, 68, 0.3)"}),
            
            # Admin info card
            html.Div([
                html.Div([
                    html.H6([
                        html.I(className="fas fa-crown me-2"),
                        "Admin Privileges"
                    ], className="mb-3", style={"color": "#ef4444"}),
                    
                    html.Ul([
                        html.Li("Full database access & editing", className="text-secondary mb-2"),
                        html.Li("Employee management", className="text-secondary mb-2"),
                        html.Li("Telemetry & analytics access", className="text-secondary mb-2"),
                        html.Li("Add/Edit/Delete all records", className="text-secondary"),
                    ], style={"listStyle": "none", "paddingLeft": "0"}),
                ], style={
                    "background": "rgba(0, 0, 0, 0.4)",
                    "backdropFilter": "blur(20px)",
                    "border": "1px solid rgba(239, 68, 68, 0.3)",
                    "borderRadius": "16px",
                    "padding": "1.5rem",
                    "marginTop": "2rem"
                })
            ], className="fade-in", style={"animation": "fadeIn 1s ease 0.5s both"}),
            
        ], className="login-container"),
        
        dcc.Store(id="admin-signup-store"),
    ], style={"minHeight": "100vh", "position": "relative"})
