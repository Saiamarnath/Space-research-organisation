from dash import html, dcc
import dash_bootstrap_components as dbc

def login_page():
    """Ultra-polished mission control login with immersive experience"""
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
                    html.I(className="fas fa-satellite fa-4x mb-3", style={
                        "color": "#06b6d4",
                        "textShadow": "0 0 40px rgba(6, 182, 212, 0.8)"
                    }),
                ], className="text-center"),
                
                # Title
                html.H2("SECURE ACCESS PORTAL", className="login-title"),
                html.P("Mission Control Authentication System", className="login-subtitle"),
                
                # Error/Success message area
                html.Div(id="login-error", className="mb-3"),
                html.Div(id="login-success", className="mb-3"),
                
                # Email input
                html.Div([
                    dbc.Label([
                        html.I(className="fas fa-envelope me-2"),
                        "Email Address"
                    ], html_for="login-email", className="form-label"),
                    dbc.Input(
                        id="login-email",
                        type="email",
                        placeholder="commander@space.mission",
                        className="form-control",
                        value="",
                        autoFocus=True,
                        autoComplete="email",
                        n_submit=0  # Enable Enter key submission
                    ),
                ], className="mb-3"),
                
                # Password input
                html.Div([
                    dbc.Label([
                        html.I(className="fas fa-lock me-2"),
                        "Access Code"
                    ], html_for="login-password", className="form-label"),
                    dbc.InputGroup([
                        dbc.Input(
                            id="login-password",
                            type="password",
                            placeholder="••••••••",
                            className="form-control",
                            value="",
                            autoComplete="current-password",
                            n_submit=0  # Enable Enter key submission
                        ),
                        html.Div(
                            html.I(className="fas fa-eye", id="password-toggle-icon"),
                            id="password-toggle",
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
                
                # Remember me & forgot password
                html.Div([
                    dbc.Checkbox(
                        id="remember-me",
                        label="Remember Email",
                        value=False,
                        className="text-secondary"
                    ),
                ], className="mb-4"),
                
                # Login button
                dbc.Button(
                    [
                        html.Span("AUTHENTICATE", id="login-button-text"),
                        html.I(className="fas fa-arrow-right ms-2", id="login-button-icon"),
                    ],
                    id="login-button",
                    color="primary",
                    className="w-100 mb-3",
                    size="lg",
                    n_clicks=0
                ),
                
                # Divider
                html.Div([
                    html.Hr(className="my-4", style={"borderColor": "rgba(255,255,255,0.1)"}),
                ]),
                
                # Create account link
                html.Div([
                    html.P([
                        "Don't have access credentials? ",
                        html.A("Request Authorization", href="/signup", className="text-info fw-bold", style={
                            "textDecoration": "none",
                            "borderBottom": "1px solid currentColor"
                        })
                    ], className="text-center text-secondary mb-0"),
                ]),
                
            ], className="login-card"),
            
            # Test credentials card
            html.Div([
                html.Div([
                    html.H6([
                        html.I(className="fas fa-info-circle me-2"),
                        "Test Credentials"
                    ], className="mb-3", style={"color": "#06b6d4"}),
                    
                    # Admin credentials
                    html.Div([
                        html.Div([
                            html.Span("ADMIN", className="badge badge-danger me-2"),
                            html.Small("Full System Access", className="text-secondary")
                        ], className="mb-2"),
                        html.P([
                            html.Code("admin@test.com", style={"color": "#00ff88", "background": "rgba(0,0,0,0.3)", "padding": "0.25rem 0.5rem", "borderRadius": "4px"}),
                            html.Br(),
                            html.Code("admin123456", style={"color": "#00ff88", "background": "rgba(0,0,0,0.3)", "padding": "0.25rem 0.5rem", "borderRadius": "4px"}),
                        ], className="mb-3"),
                    ]),
                    
                    # User credentials
                    html.Div([
                        html.Div([
                            html.Span("USER", className="badge badge-info me-2"),
                            html.Small("Limited Access", className="text-secondary")
                        ], className="mb-2"),
                        html.P([
                            html.Code("user@space.com", style={"color": "#06b6d4", "background": "rgba(0,0,0,0.3)", "padding": "0.25rem 0.5rem", "borderRadius": "4px"}),
                            html.Br(),
                            html.Code("user123", style={"color": "#06b6d4", "background": "rgba(0,0,0,0.3)", "padding": "0.25rem 0.5rem", "borderRadius": "4px"}),
                        ], className="mb-0"),
                    ]),
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
        
        # Client-side callback for Enter key and password toggle
        dcc.Store(id="login-store"),
    ], style={"minHeight": "100vh", "position": "relative"})
