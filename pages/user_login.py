from dash import html, dcc
import dash_bootstrap_components as dbc

def user_login_page():
    """User login page with blue theme"""
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
                    html.I(className="fas fa-user fa-4x mb-3", style={
                        "color": "#06b6d4",
                        "textShadow": "0 0 40px rgba(6, 182, 212, 0.8)"
                    }),
                ], className="text-center"),
                
                # Title
                html.H2("USER ACCESS PORTAL", className="login-title", style={
                    "background": "linear-gradient(135deg, #06b6d4, #0891b2)",
                    "-webkit-background-clip": "text",
                    "-webkit-text-fill-color": "transparent"
                }),
                html.P("User Authentication System", className="login-subtitle"),
                
                # User info badge
                html.Div([
                    html.Span([
                        html.I(className="fas fa-info-circle me-2"),
                        "USER ACCESS - VIEW MISSIONS & DATA"
                    ], className="badge w-100 mb-3 py-2", style={
                        "background": "rgba(6, 182, 212, 0.2)",
                        "color": "#06b6d4",
                        "border": "1px solid #06b6d4",
                        "fontSize": "0.875rem"
                    })
                ]),
                
                # Error/Success message area
                html.Div(id="user-login-error", className="mb-3"),
                
                # Email input
                html.Div([
                    dbc.Label([
                        html.I(className="fas fa-envelope me-2"),
                        "Email Address"
                    ], html_for="user-login-email", className="form-label"),
                    dbc.Input(
                        id="user-login-email",
                        type="email",
                        placeholder="user@space.mission",
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
                        "Access Code"
                    ], html_for="user-login-password", className="form-label"),
                    dbc.InputGroup([
                        dbc.Input(
                            id="user-login-password",
                            type="password",
                            placeholder="••••••••",
                            className="form-control",
                            value="",
                            autoComplete="current-password",
                            n_submit=0
                        ),
                        html.Div(
                            html.I(className="fas fa-eye", id="user-password-toggle-icon"),
                            id="user-password-toggle",
                            n_clicks=0,
                            className="input-group-text",
                            style={
                                "cursor": "pointer", 
                                "userSelect": "none",
                                "background": "rgba(255, 255, 255, 0.1)",
                                "border": "1px solid rgba(255, 255, 255, 0.2)",
                                "color": "#06b6d4"
                            }
                        ),
                    ]),
                ], className="mb-4"),
                
                # Login button
                dbc.Button(
                    [
                        html.Span("USER AUTHENTICATE", id="user-login-button-text"),
                        html.I(className="fas fa-arrow-right ms-2", id="user-login-button-icon"),
                    ],
                    id="user-login-button",
                    color="info",
                    className="w-100 mb-3",
                    size="lg",
                    n_clicks=0
                ),
                
                # Divider
                html.Div([
                    html.Hr(className="my-4", style={"borderColor": "rgba(255,255,255,0.1)"}),
                ]),
                
                # Links
                html.Div([
                    html.P([
                        html.A([
                            html.I(className="fas fa-user-shield me-2"),
                            "Admin Login"
                        ], href="/admin-login", className="text-danger", style={
                            "textDecoration": "none",
                            "borderBottom": "1px solid currentColor"
                        }),
                        html.Span(" | ", className="text-secondary mx-2"),
                        html.A([
                            html.I(className="fas fa-user-plus me-2"),
                            "Register as User"
                        ], href="/user-signup", className="text-info", style={
                            "textDecoration": "none",
                            "borderBottom": "1px solid currentColor"
                        })
                    ], className="text-center mb-0"),
                ]),
                
            ], className="login-card", style={"border": "1px solid rgba(6, 182, 212, 0.3)"}),
            
            # Test credentials card
            html.Div([
                html.Div([
                    html.H6([
                        html.I(className="fas fa-key me-2"),
                        "Test User Credentials"
                    ], className="mb-3", style={"color": "#06b6d4"}),
                    
                    html.P([
                        html.Code("user@space.com", style={"color": "#06b6d4", "background": "rgba(0,0,0,0.3)", "padding": "0.25rem 0.5rem", "borderRadius": "4px"}),
                        html.Br(),
                        html.Code("user123", style={"color": "#06b6d4", "background": "rgba(0,0,0,0.3)", "padding": "0.25rem 0.5rem", "borderRadius": "4px"}),
                    ], className="mb-0"),
                ], style={
                    "background": "rgba(0, 0, 0, 0.4)",
                    "backdropFilter": "blur(20px)",
                    "border": "1px solid rgba(6, 182, 212, 0.3)",
                    "borderRadius": "16px",
                    "padding": "1.5rem",
                    "marginTop": "2rem"
                })
            ], className="fade-in", style={"animation": "fadeIn 1s ease 0.5s both"}),
            
        ], className="login-container"),
        
        dcc.Store(id="user-login-store"),
    ], style={"minHeight": "100vh", "position": "relative"})
