from dash import html, dcc
import dash_bootstrap_components as dbc

def signup_page():
    """Ultra-polished signup page with password strength meter"""
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
                        "color": "#00ff88",
                        "textShadow": "0 0 40px rgba(0, 255, 136, 0.8)"
                    }),
                ], className="text-center"),
                
                # Title
                html.H2("AUTHORIZATION REQUEST", className="login-title", style={
                    "background": "linear-gradient(135deg, #00ff88, #10b981)",
                    "-webkit-background-clip": "text",
                    "-webkit-text-fill-color": "transparent"
                }),
                html.P("New Crew Member Registration", className="login-subtitle"),
                
                # Message area
                html.Div(id="signup-message", className="mb-3"),
                
                # Username input
                html.Div([
                    dbc.Label([
                        html.I(className="fas fa-user me-2"),
                        "Call Sign / Username"
                    ], html_for="signup-username", className="form-label"),
                    dbc.Input(
                        id="signup-username",
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
                    ], html_for="signup-email", className="form-label"),
                    dbc.Input(
                        id="signup-email",
                        type="email",
                        placeholder="your.name@space.mission",
                        className="form-control",
                        autoComplete="email",
                        n_submit=0
                    ),
                ], className="mb-3"),
                
                # Password input with strength meter
                html.Div([
                    dbc.Label([
                        html.I(className="fas fa-lock me-2"),
                        "Access Code"
                    ], html_for="signup-password", className="form-label"),
                    dbc.InputGroup([
                        dbc.Input(
                            id="signup-password",
                            type="password",
                            placeholder="Minimum 6 characters",
                            className="form-control",
                            n_submit=0
                        ),
                        dbc.Button(
                            html.I(className="fas fa-eye", id="signup-password-toggle-icon"),
                            id="signup-password-toggle",
                            color="link",
                            className="text-secondary",
                            n_clicks=0,
                            style={"border": "none", "background": "transparent"}
                        ),
                    ]),
                    # Password strength meter
                    html.Div([
                        html.Div(id="password-strength-bar", className="progress mt-2", style={"height": "6px"}, children=[
                            html.Div(className="progress-bar", style={"width": "0%"}, id="password-strength-progress")
                        ]),
                        html.Small(id="password-strength-text", className="text-muted mt-1 d-block"),
                    ]),
                ], className="mb-3"),
                
                # Confirm password input
                html.Div([
                    dbc.Label([
                        html.I(className="fas fa-lock me-2"),
                        "Confirm Access Code"
                    ], html_for="signup-password-confirm", className="form-label"),
                    dbc.Input(
                        id="signup-password-confirm",
                        type="password",
                        placeholder="Re-enter your access code",
                        className="form-control",
                        n_submit=0
                    ),
                    html.Div(id="password-match-indicator", className="mt-1"),
                ], className="mb-4"),
                
                # Terms acceptance
                html.Div([
                    dbc.Checkbox(
                        id="accept-terms",
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
                        html.Span("REQUEST AUTHORIZATION", id="signup-button-text"),
                        html.I(className="fas fa-rocket ms-2", id="signup-button-icon"),
                    ],
                    id="signup-button",
                    color="success",
                    className="w-100 mb-3",
                    size="lg",
                    n_clicks=0
                ),
                
                # Divider
                html.Div([
                    html.Hr(className="my-4", style={"borderColor": "rgba(255,255,255,0.1)"}),
                ]),
                
                # Back to login link
                html.Div([
                    html.P([
                        "Already authorized? ",
                        html.A("Return to Access Portal", href="/login", className="text-info fw-bold", style={
                            "textDecoration": "none",
                            "borderBottom": "1px solid currentColor"
                        })
                    ], className="text-center text-secondary mb-0"),
                ]),
                
            ], className="login-card"),
            
            # Security info card
            html.Div([
                html.Div([
                    html.H6([
                        html.I(className="fas fa-shield-alt me-2"),
                        "Security Requirements"
                    ], className="mb-3", style={"color": "#00ff88"}),
                    
                    html.Ul([
                        html.Li("Minimum 6 characters", className="text-secondary mb-2"),
                        html.Li("Unique email address", className="text-secondary mb-2"),
                        html.Li("All crew members start with User role", className="text-secondary mb-2"),
                        html.Li("Admin access requires authorization", className="text-secondary"),
                    ], style={"listStyle": "none", "paddingLeft": "0"}),
                ], style={
                    "background": "rgba(0, 0, 0, 0.4)",
                    "backdropFilter": "blur(20px)",
                    "border": "1px solid rgba(0, 255, 136, 0.3)",
                    "borderRadius": "16px",
                    "padding": "1.5rem",
                    "marginTop": "2rem"
                })
            ], className="fade-in", style={"animation": "fadeIn 1s ease 0.5s both"}),
            
        ], className="login-container"),
        
        # Store for password validation
        dcc.Store(id="signup-store"),
    ], style={"minHeight": "100vh", "position": "relative"})
