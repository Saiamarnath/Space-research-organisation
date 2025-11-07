from dash import html
import dash_bootstrap_components as dbc

def login_selection_page():
    """Login selection page - choose between Admin and User login"""
    return html.Div([
        # Shooting stars effect
        html.Div(className="shooting-star", style={"top": "10%", "left": "20%"}),
        html.Div(className="shooting-star", style={"top": "60%", "left": "70%", "animationDelay": "2s"}),
        html.Div(className="shooting-star", style={"top": "30%", "left": "80%", "animationDelay": "4s"}),
        
        # Main container
        html.Div([
            # Logo and title
            html.Div([
                html.I(className="fas fa-satellite fa-5x mb-4", style={
                    "color": "#06b6d4",
                    "textShadow": "0 0 60px rgba(6, 182, 212, 0.8)"
                }),
                html.H1("SPACE RESEARCH SYSTEM", className="mb-2", style={
                    "fontSize": "2.5rem",
                    "fontWeight": "700",
                    "background": "linear-gradient(135deg, #06b6d4, #6366f1, #00ff88)",
                    "-webkit-background-clip": "text",
                    "-webkit-text-fill-color": "transparent",
                    "letterSpacing": "0.05em"
                }),
                html.P("Mission Control Authentication", className="text-secondary mb-5", style={"fontSize": "1.1rem"}),
            ], className="text-center fade-in"),
            
            # Login cards row
            dbc.Row([
                # Admin Login Card
                dbc.Col([
                    html.A([
                        html.Div([
                            html.I(className="fas fa-user-shield fa-4x mb-3", style={"color": "#ef4444"}),
                            html.H3("ADMIN LOGIN", className="mb-2", style={"color": "#e5e7eb"}),
                            html.P("Full System Control", className="text-secondary mb-3"),
                            
                            html.Div([
                                html.I(className="fas fa-check me-2 text-danger"),
                                html.Span("Database Management", className="text-secondary")
                            ], className="mb-2 small"),
                            html.Div([
                                html.I(className="fas fa-check me-2 text-danger"),
                                html.Span("Employee Control", className="text-secondary")
                            ], className="mb-2 small"),
                            html.Div([
                                html.I(className="fas fa-check me-2 text-danger"),
                                html.Span("Analytics Access", className="text-secondary")
                            ], className="mb-3 small"),
                            
                            dbc.Button([
                                html.I(className="fas fa-shield-alt me-2"),
                                "Admin Login"
                            ], color="danger", className="w-100", size="lg"),
                        ], className="p-4 text-center hover-lift", style={
                            "background": "rgba(0, 0, 0, 0.4)",
                            "backdropFilter": "blur(20px)",
                            "border": "2px solid rgba(239, 68, 68, 0.3)",
                            "borderRadius": "16px",
                            "transition": "all 0.3s ease",
                            "cursor": "pointer"
                        })
                    ], href="/admin-login", style={"textDecoration": "none"})
                ], width=12, md=6, className="mb-4 slide-up stagger-1"),
                
                # User Login Card
                dbc.Col([
                    html.A([
                        html.Div([
                            html.I(className="fas fa-user fa-4x mb-3", style={"color": "#06b6d4"}),
                            html.H3("USER LOGIN", className="mb-2", style={"color": "#e5e7eb"}),
                            html.P("View Missions & Data", className="text-secondary mb-3"),
                            
                            html.Div([
                                html.I(className="fas fa-check me-2 text-info"),
                                html.Span("Mission Viewer", className="text-secondary")
                            ], className="mb-2 small"),
                            html.Div([
                                html.I(className="fas fa-check me-2 text-info"),
                                html.Span("Satellite Monitor", className="text-secondary")
                            ], className="mb-2 small"),
                            html.Div([
                                html.I(className="fas fa-check me-2 text-info"),
                                html.Span("Research Access", className="text-secondary")
                            ], className="mb-3 small"),
                            
                            dbc.Button([
                                html.I(className="fas fa-sign-in-alt me-2"),
                                "User Login"
                            ], color="info", className="w-100", size="lg"),
                        ], className="p-4 text-center hover-lift", style={
                            "background": "rgba(0, 0, 0, 0.4)",
                            "backdropFilter": "blur(20px)",
                            "border": "2px solid rgba(6, 182, 212, 0.3)",
                            "borderRadius": "16px",
                            "transition": "all 0.3s ease",
                            "cursor": "pointer"
                        })
                    ], href="/login", style={"textDecoration": "none"})
                ], width=12, md=6, className="mb-4 slide-up stagger-2"),
            ], className="mb-4"),
            
            # Divider
            html.Hr(className="my-4", style={"borderColor": "rgba(255,255,255,0.1)"}),
            
            # Signup section
            html.Div([
                html.H5("Don't have an account?", className="text-center mb-3 text-secondary"),
                dbc.Row([
                    dbc.Col([
                        dbc.Button([
                            html.I(className="fas fa-user-plus me-2"),
                            "Register as Admin"
                        ], href="/admin-signup", color="danger", outline=True, className="w-100")
                    ], width=12, md=6, className="mb-2"),
                    dbc.Col([
                        dbc.Button([
                            html.I(className="fas fa-user-plus me-2"),
                            "Register as User"
                        ], href="/user-signup", color="info", outline=True, className="w-100")
                    ], width=12, md=6, className="mb-2"),
                ])
            ], className="fade-in", style={"animation": "fadeIn 1s ease 1s both"}),
            
        ], className="login-container", style={"maxWidth": "900px"}),
        
    ], style={"minHeight": "100vh", "position": "relative"})
