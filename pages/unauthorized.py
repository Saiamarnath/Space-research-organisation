from dash import html, dcc
import dash_bootstrap_components as dbc

def unauthorized_page():
    """Unauthorized access page with mission-control aesthetic"""
    return html.Div([
        # Space background
        html.Div(className="space-bg"),
        
        # Content
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        # Animated warning icon
                        html.Div([
                            html.I(className="fas fa-shield-alt", style={
                                'fontSize': '120px',
                                'color': '#ef4444',
                                'marginBottom': '30px',
                                'animation': 'shake 0.5s infinite alternate'
                            })
                        ], className="text-center"),
                        
                        # Alert heading
                        html.H1([
                            html.I(className="fas fa-exclamation-triangle me-3"),
                            "ACCESS RESTRICTED"
                        ], style={
                            'color': '#ef4444',
                            'fontSize': '2.5rem',
                            'fontWeight': '700',
                            'textAlign': 'center',
                            'marginBottom': '20px',
                            'textTransform': 'uppercase',
                            'letterSpacing': '3px',
                            'textShadow': '0 0 20px rgba(239, 68, 68, 0.5)'
                        }),
                        
                        # Message
                        html.Div([
                            html.P([
                                html.I(className="fas fa-user-lock me-2"),
                                "You do not have authorization to access this area."
                            ], style={
                                'fontSize': '1.3rem',
                                'color': '#e0e0e0',
                                'marginBottom': '15px',
                                'textAlign': 'center'
                            }),
                            
                            html.P([
                                "This section is restricted to ",
                                html.Span("ADMIN", style={
                                    'color': '#ef4444',
                                    'fontWeight': 'bold',
                                    'fontSize': '1.1em'
                                }),
                                " personnel only."
                            ], style={
                                'fontSize': '1.1rem',
                                'color': '#a0a0a0',
                                'marginBottom': '30px',
                                'textAlign': 'center'
                            }),
                            
                            # Warning box
                            html.Div([
                                html.I(className="fas fa-info-circle me-2"),
                                "Unauthorized access attempts are monitored and logged."
                            ], style={
                                'backgroundColor': 'rgba(239, 68, 68, 0.1)',
                                'border': '1px solid rgba(239, 68, 68, 0.3)',
                                'borderRadius': '8px',
                                'padding': '15px',
                                'color': '#fca5a5',
                                'fontSize': '0.95rem',
                                'marginBottom': '30px',
                                'textAlign': 'center'
                            }),
                            
                            # Action buttons
                            html.Div([
                                dbc.Button([
                                    html.I(className="fas fa-home me-2"),
                                    "Return to Dashboard"
                                ], href="/", color="primary", size="lg", className="me-3", style={
                                    'background': 'linear-gradient(135deg, #06b6d4 0%, #0284c7 100%)',
                                    'border': 'none',
                                    'boxShadow': '0 4px 15px rgba(6, 182, 212, 0.4)',
                                    'padding': '12px 30px',
                                    'fontSize': '1.1rem',
                                    'fontWeight': '600',
                                    'transition': 'all 0.3s'
                                }),
                                
                                dbc.Button([
                                    html.I(className="fas fa-arrow-left me-2"),
                                    "Go Back"
                                ], id="go-back-btn", color="secondary", size="lg", style={
                                    'background': 'rgba(255, 255, 255, 0.1)',
                                    'border': '1px solid rgba(255, 255, 255, 0.2)',
                                    'backdropFilter': 'blur(10px)',
                                    'padding': '12px 30px',
                                    'fontSize': '1.1rem',
                                    'fontWeight': '600',
                                    'transition': 'all 0.3s'
                                })
                            ], className="text-center"),
                            
                        ], style={
                            'padding': '40px'
                        })
                        
                    ], className="glass-card", style={
                        'maxWidth': '700px',
                        'margin': '0 auto',
                        'padding': '50px 30px',
                        'border': '2px solid rgba(239, 68, 68, 0.3)',
                        'animation': 'glow-pulse-red 2s ease-in-out infinite'
                    })
                ], width=12)
            ], justify="center", style={'minHeight': '80vh', 'alignItems': 'center'})
        ], fluid=True, style={'position': 'relative', 'zIndex': '1'})
    ], style={'position': 'relative', 'minHeight': '100vh'})
