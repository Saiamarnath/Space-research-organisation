from dash import html, dcc
import dash_bootstrap_components as dbc

def user_signup_page():
    """User signup page with blue theme"""
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
                    html.I(className="fas fa-user-astronaut fa-4x mb-3", style={
                        "color": "#06b6d4",
                        "textShadow": "0 0 40px rgba(6, 182, 212, 0.8)"
                    }),
                ], className="text-center"),
                
                # Title
                html.H2("USER REGISTRATION", className="login-title", style={
                    "background": "linear-gradient(135deg, #06b6d4, #0891b2)",
                    "-webkit-background-clip": "text",
                    "-webkit-text-fill-color": "transparent"
                }),
                html.P("New Crew Member Registration", className="login-subtitle"),
                
                # Info badge
                html.Div([
                    html.Span([
                        html.I(className="fas fa-info-circle me-2"),
                        "USER ACCOUNTS CAN VIEW MISSIONS & DATA"
                    ], className="badge w-100 mb-3 py-2", style={
                        "background": "rgba(6, 182, 212, 0.2)",
                        "color": "#06b6d4",
                        "border": "1px solid #06b6d4",
                        "fontSize": "0.875rem"
                    })
                ]),
                
                # Message area
                html.Div(id="user-signup-message", className="mb-3"),
                
                # Username input
                html.Div([
                    dbc.Label([
                        html.I(className="fas fa-user me-2"),
                        "Username / Call Sign"
                    ], html_for="user-signup-username", className="form-label"),
                    dbc.Input(
                        id="user-signup-username",
                        type="text",
                        placeholder="Choose your call sign",
                        className="form-control",
                        autoFocus=True,
                        n_submit=0
                    ),
                ], className="mb-3"),
                
                # Email input
                html.Div([
                    dbc.Label([
                        html.I(className="fas fa-envelope me-2"),
                        "Email Address"
                    ], html_for="user-signup-email", className="form-label"),
                    dbc.Input(
                        id="user-signup-email",
                        type="email",
                        placeholder="your.name@space.mission",
                        className="form-control",
                        autoComplete="email",
                        n_submit=0
                    ),
                ], className="mb-3"),
                
                # Password input
                html.Div([
                    dbc.Label([
                        html.I(className="fas fa-lock me-2"),
                        "Access Code"
                    ], html_for="user-signup-password", className="form-label"),
                    dbc.Input(
                        id="user-signup-password",
                        type="password",
                        placeholder="Minimum 6 characters",
                        className="form-control",
                        n_submit=0
                    ),
                ], className="mb-3"),
                
                # Confirm password input
                html.Div([
                    dbc.Label([
                        html.I(className="fas fa-lock me-2"),
                        "Confirm Access Code"
                    ], html_for="user-signup-password-confirm", className="form-label"),
                    dbc.Input(
                        id="user-signup-password-confirm",
                        type="password",
                        placeholder="Re-enter your access code",
                        className="form-control",
                        n_submit=0
                    ),
                ], className="mb-4"),
                
                # Terms acceptance
                html.Div([
                    dbc.Checkbox(
                        id="user-accept-terms",
                        label=[
                            "I acknowledge mission protocols and ",
                            html.Span("data handling policies", className="text-info fw-bold")
                        ],
                        value=False,
                        className="text-secondary"
                    ),
                ], className="mb-4"),
                
                # Signup button
                dbc.Button(
                    [
                        html.Span("CREATE USER ACCOUNT", id="user-signup-button-text"),
                        html.I(className="fas fa-rocket ms-2", id="user-signup-button-icon"),
                    ],
                    id="user-signup-button",
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
                            html.I(className="fas fa-sign-in-alt me-2"),
                            "User Login"
                        ], href="/login", className="text-info", style={
                            "textDecoration": "none",
                            "borderBottom": "1px solid currentColor"
                        }),
                        html.Span(" | ", className="text-secondary mx-2"),
                        html.A([
                            html.I(className="fas fa-user-shield me-2"),
                            "Admin Signup"
                        ], href="/admin-signup", className="text-danger", style={
                            "textDecoration": "none",
                            "borderBottom": "1px solid currentColor"
                        })
                    ], className="text-center mb-0"),
                ]),
                
            ], className="login-card", style={"border": "1px solid rgba(6, 182, 212, 0.3)"}),
            
            # User info card
            html.Div([
                html.Div([
                    html.H6([
                        html.I(className="fas fa-info-circle me-2"),
                        "User Access Rights"
                    ], className="mb-3", style={"color": "#06b6d4"}),
                    
                    html.Ul([
                        html.Li("View missions & satellites", className="text-secondary mb-2"),
                        html.Li("Browse research facts", className="text-secondary mb-2"),
                        html.Li("Access common dashboard", className="text-secondary mb-2"),
                        html.Li("Read-only data access", className="text-secondary"),
                    ], style={"listStyle": "none", "paddingLeft": "0"}),
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
        
        dcc.Store(id="user-signup-store"),
    ], style={"minHeight": "100vh", "position": "relative"})
