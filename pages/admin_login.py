from dash import html, dcc
import dash_bootstrap_components as dbc

def admin_login_page():
    """Admin login page with red theme"""
    return html.Div([
        # Shooting stars effect
        html.Div(className="shooting-star", style={"top": "10%", "left": "20%"}),
        html.Div(className="shooting-star", style={"top": "60%", "left": "70%", "animationDelay": "2s"}),
        html.Div(className="shooting-star", style={"top": "30%", "left": "80%", "animationDelay": "4s"}),
        
        # Main login container
        html.Div([
            # Glassmorphic login card
            html.Div([
                # Logo/Icon
                html.Div([
                    html.I(className="fas fa-user-shield fa-4x mb-3", style={
                        "color": "#ef4444",
                        "textShadow": "0 0 40px rgba(239, 68, 68, 0.8)"
                    }),
                ], className="text-center"),
                
                # Title
                html.H2("ADMIN ACCESS PORTAL", className="login-title", style={
                    "background": "linear-gradient(135deg, #ef4444, #dc2626)",
                    "-webkit-background-clip": "text",
                    "-webkit-text-fill-color": "transparent"
                }),
                html.P("Administrator Authentication System", className="login-subtitle"),
                
                # Admin warning badge
                html.Div([
                    html.Span([
                        html.I(className="fas fa-exclamation-triangle me-2"),
                        "RESTRICTED ACCESS - ADMINS ONLY"
                    ], className="badge w-100 mb-3 py-2", style={
                        "background": "rgba(239, 68, 68, 0.2)",
                        "color": "#ef4444",
                        "border": "1px solid #ef4444",
                        "fontSize": "0.875rem"
                    })
                ]),
                
                # Error/Success message area
                html.Div(id="admin-login-error", className="mb-3"),
                
                # Email input
                html.Div([
                    dbc.Label([
                        html.I(className="fas fa-envelope me-2"),
                        "Admin Email"
                    ], html_for="admin-login-email", className="form-label"),
                    dbc.Input(
                        id="admin-login-email",
                        type="email",
                        placeholder="admin@space.mission",
                        className="form-control",
                        value="",
                        autoFocus=True,
                        autoComplete="email",
                        n_submit=0
                    ),
                ], className="mb-3"),
                
                # Password input
                html.Div([
                    dbc.Label([
                        html.I(className="fas fa-lock me-2"),
                        "Admin Access Code"
                    ], html_for="admin-login-password", className="form-label"),
                    dbc.InputGroup([
                        dbc.Input(
                            id="admin-login-password",
                            type="password",
                            placeholder="••••••••",
                            className="form-control",
                            value="",
                            autoComplete="current-password",
                            n_submit=0
                        ),
                        html.Div(
                            html.I(className="fas fa-eye", id="admin-password-toggle-icon"),
                            id="admin-password-toggle",
                            n_clicks=0,
                            className="input-group-text",
                            style={
                                "cursor": "pointer", 
                                "userSelect": "none",
                                "background": "rgba(255, 255, 255, 0.1)",
                                "border": "1px solid rgba(255, 255, 255, 0.2)",
                                "color": "#ef4444"
                            }
                        ),
                    ]),
                ], className="mb-4"),
                
                # Login button
                dbc.Button(
                    [
                        html.Span("ADMIN AUTHENTICATE", id="admin-login-button-text"),
                        html.I(className="fas fa-shield-alt ms-2", id="admin-login-button-icon"),
                    ],
                    id="admin-login-button",
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
                            html.I(className="fas fa-user me-2"),
                            "User Login"
                        ], href="/login", className="text-info", style={
                            "textDecoration": "none",
                            "borderBottom": "1px solid currentColor"
                        }),
                        html.Span(" | ", className="text-secondary mx-2"),
                        html.A([
                            html.I(className="fas fa-user-plus me-2"),
                            "Register as Admin"
                        ], href="/admin-signup", className="text-danger", style={
                            "textDecoration": "none",
                            "borderBottom": "1px solid currentColor"
                        })
                    ], className="text-center mb-0"),
                ]),
                
            ], className="login-card", style={"border": "1px solid rgba(239, 68, 68, 0.3)"}),
            
            # Test credentials card
            html.Div([
                html.Div([
                    html.H6([
                        html.I(className="fas fa-key me-2"),
                        "Test Admin Credentials"
                    ], className="mb-3", style={"color": "#ef4444"}),
                    
                    html.P([
                        html.Code("admin@test.com", style={"color": "#ef4444", "background": "rgba(0,0,0,0.3)", "padding": "0.25rem 0.5rem", "borderRadius": "4px"}),
                        html.Br(),
                        html.Code("admin123456", style={"color": "#ef4444", "background": "rgba(0,0,0,0.3)", "padding": "0.25rem 0.5rem", "borderRadius": "4px"}),
                    ], className="mb-0"),
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
        
        dcc.Store(id="admin-login-store"),
    ], style={"minHeight": "100vh", "position": "relative"})
