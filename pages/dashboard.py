from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from config.database import db
from datetime import datetime

def dashboard_home(user_role=None):
    """Ultra-polished mission control dashboard with immersive experience - ADMIN ONLY"""
    if user_role != 'admin':
        # Non-admin users redirected by app.py; this is defensive
        return html.Div([
            dbc.Alert("This page is for administrators only.", color="warning")
        ])
    try:
        mission_stats = db.get_mission_statistics()
        satellite_stats = db.get_satellite_statistics()
        departments = db.get_all_departments()
        employees = db.get_all_employees()
        
        # Dashboard header with live clock and status
        header = html.Div([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.Span(className="status-indicator me-3"),
                        html.Span("SYSTEMS ONLINE", className="systems-online"),
                    ], className="d-flex align-items-center"),
                ], width="auto"),
                dbc.Col([
                    html.Div([
                        html.Div([
                            html.I(className="fas fa-globe me-2"),
                            html.Span("UTC: ", className="text-secondary me-2"),
                            html.Span(id="live-utc-clock", className="utc-clock"),
                        ], className="d-flex align-items-center justify-content-end"),
                    ]),
                ], width="auto", className="ms-auto"),
            ], className="align-items-center"),
            
            # Interval for live clock update
            dcc.Interval(id='clock-update', interval=1000, n_intervals=0),
        ], className="dashboard-header mb-4 fade-in")
        
        # Mission ticker banner
        missions = db.get_all_missions()
        ticker_items = []
        if missions:
            for mission in missions[:5]:
                status = mission.get('status', 'Unknown')
                ticker_items.append(
                    html.Span([
                        html.I(className="fas fa-satellite me-2"),
                        f"{mission.get('mission_name', 'Unknown')} - {status}",
                    ], className="ticker-item")
                )
        
        if not ticker_items:
            ticker_items = [html.Span("No active missions", className="ticker-item")]
        
        ticker = html.Div([
            html.Div(ticker_items + ticker_items, className="ticker-content"),  # Duplicate for seamless loop
        ], className="mission-ticker mb-4 slide-up stagger-1")
        
        # Animated stat cards
        stat_cards = dbc.Row([
            dbc.Col([
                html.Div([
                    html.I(className="fas fa-rocket stat-icon", style={"color": "#6366f1"}),
                    html.Div([
                        html.Div("0", id="missions-count", className="stat-value", **{"data-target": mission_stats.get('total', 0)}),
                        html.P("Total Missions", className="stat-label"),
                    ]),
                ], className="stat-card slide-up stagger-1")
            ], width=12, md=6, lg=3, className="mb-3"),
            
            dbc.Col([
                html.Div([
                    html.I(className="fas fa-satellite-dish stat-icon", style={"color": "#10b981"}),
                    html.Div([
                        html.Div("0", id="satellites-count", className="stat-value", **{"data-target": satellite_stats.get('operational', 0)}),
                        html.P("Operational Satellites", className="stat-label"),
                    ]),
                ], className="stat-card slide-up stagger-2")
            ], width=12, md=6, lg=3, className="mb-3"),
            
            dbc.Col([
                html.Div([
                    html.I(className="fas fa-users-cog stat-icon", style={"color": "#06b6d4"}),
                    html.Div([
                        html.Div("0", id="employees-count", className="stat-value", **{"data-target": len(employees)}),
                        html.P("Crew Members", className="stat-label"),
                    ]),
                ], className="stat-card slide-up stagger-3")
            ], width=12, md=6, lg=3, className="mb-3"),
            
            dbc.Col([
                html.Div([
                    html.I(className="fas fa-network-wired stat-icon", style={"color": "#f59e0b"}),
                    html.Div([
                        html.Div("0", id="departments-count", className="stat-value", **{"data-target": len(departments)}),
                        html.P("Active Departments", className="stat-label"),
                    ]),
                ], className="stat-card slide-up stagger-4")
            ], width=12, md=6, lg=3, className="mb-3"),
        ])
        
        # Main content area - Three column layout
        main_content = dbc.Row([
            # Left column - Mission timeline
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-list-ul me-2"),
                            "Mission Timeline"
                        ], className="mb-0 glow-text", style={"color": "#06b6d4"})
                    ]),
                    dbc.CardBody([
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Span(className="badge badge-success me-2", children="ACTIVE"),
                                    html.Strong(mission.get('mission_name', 'Unknown')),
                                ]),
                                html.Small(f"Status: {mission.get('status', 'N/A')}", className="text-secondary d-block mt-1"),
                            ], className="mb-3 p-2", style={
                                "borderLeft": "3px solid #10b981",
                                "background": "rgba(16, 185, 129, 0.05)",
                                "borderRadius": "4px"
                            }) for mission in missions[:5]
                        ] if missions else [html.P("No missions available", className="text-muted text-center")])
                    ], style={"maxHeight": "400px", "overflowY": "auto"})
                ], className="glass-card h-100 slide-up stagger-1")
            ], width=12, lg=4, className="mb-4"),
            
            # Center column - 3D Globe placeholder + Telemetry feed
            dbc.Col([
                # 3D Globe visualization placeholder
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-globe-americas me-2"),
                            "Orbital Overview"
                        ], className="mb-0 glow-text", style={"color": "#6366f1"})
                    ]),
                    dbc.CardBody([
                        html.Div([
                            html.Div([
                                html.I(className="fas fa-spinner fa-spin fa-3x mb-3", style={"color": "#6366f1"}),
                                html.P("3D Globe Visualization", className="text-secondary mb-2"),
                                html.Small("Interactive satellite tracking coming soon", className="text-muted"),
                            ], className="text-center py-5")
                        ], style={"minHeight": "300px", "display": "flex", "alignItems": "center", "justifyContent": "center"})
                    ])
                ], className="glass-card mb-4 slide-up stagger-2"),
                
                # Live telemetry feed
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-terminal me-2"),
                            "Live Telemetry Feed"
                        ], className="mb-0 glow-text", style={"color": "#00ff88"})
                    ]),
                    dbc.CardBody([
                        html.Div([
                            html.Div([
                                html.Span(datetime.utcnow().strftime("%H:%M:%S"), className="telemetry-timestamp"),
                                html.Span(">> SYSTEM INITIALIZED", style={"color": "#00ff88"})
                            ], className="telemetry-line"),
                            html.Div([
                                html.Span(datetime.utcnow().strftime("%H:%M:%S"), className="telemetry-timestamp"),
                                html.Span(">> CONNECTING TO SATELLITE NETWORK...", style={"color": "#06b6d4"})
                            ], className="telemetry-line"),
                            html.Div([
                                html.Span(datetime.utcnow().strftime("%H:%M:%S"), className="telemetry-timestamp"),
                                html.Span(f">> {satellite_stats.get('operational', 0)} SATELLITES OPERATIONAL", style={"color": "#10b981"})
                            ], className="telemetry-line"),
                            html.Div([
                                html.Span(datetime.utcnow().strftime("%H:%M:%S"), className="telemetry-timestamp"),
                                html.Span(">> DATA STREAM ACTIVE", style={"color": "#00ff88"})
                            ], className="telemetry-line"),
                            html.Div([
                                html.Span(datetime.utcnow().strftime("%H:%M:%S"), className="telemetry-timestamp"),
                                html.Span(">> ALL SYSTEMS NOMINAL", style={"color": "#10b981"})
                            ], className="telemetry-line"),
                        ], className="telemetry-feed", id="telemetry-feed-content")
                    ])
                ], className="glass-card slide-up stagger-3")
            ], width=12, lg=4, className="mb-4"),
            
            # Right column - Satellite status & quick stats
            dbc.Col([
                # Satellite status grid
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-satellite me-2"),
                            "Satellite Status"
                        ], className="mb-0 glow-text", style={"color": "#f59e0b"})
                    ]),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.Div("OPERATIONAL", className="text-center mb-2 fw-bold", style={"color": "#10b981", "fontSize": "0.75rem"}),
                                    html.Div(str(satellite_stats.get('operational', 0)), className="text-center", style={"fontSize": "2rem", "fontFamily": "Courier New", "color": "#10b981"}),
                                ], className="p-2", style={"background": "rgba(16, 185, 129, 0.1)", "borderRadius": "8px", "border": "1px solid rgba(16, 185, 129, 0.3)"})
                            ], width=6, className="mb-3"),
                            dbc.Col([
                                html.Div([
                                    html.Div("MAINTENANCE", className="text-center mb-2 fw-bold", style={"color": "#f59e0b", "fontSize": "0.75rem"}),
                                    html.Div(str(satellite_stats.get('maintenance', 0)), className="text-center", style={"fontSize": "2rem", "fontFamily": "Courier New", "color": "#f59e0b"}),
                                ], className="p-2", style={"background": "rgba(245, 158, 11, 0.1)", "borderRadius": "8px", "border": "1px solid rgba(245, 158, 11, 0.3)"})
                            ], width=6, className="mb-3"),
                        ]),
                        html.Hr(style={"borderColor": "rgba(255,255,255,0.1)"}),
                        html.Div([
                            html.Small("TOTAL MASS", className="text-secondary d-block mb-1"),
                            html.Div(f"{satellite_stats.get('total_mass', 0):.0f} kg", className="fw-bold", style={"fontSize": "1.25rem", "color": "#e5e7eb"}),
                        ])
                    ])
                ], className="glass-card mb-4 slide-up stagger-1"),
                
                # Department load indicators
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-chart-bar me-2"),
                            "Department Activity"
                        ], className="mb-0 glow-text", style={"color": "#ec4899"})
                    ]),
                    dbc.CardBody([
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Small(dept.get('dept_name', 'Unknown')[:15], className="text-secondary mb-1 d-block"),
                                    html.Div([
                                        html.Div(className="progress-bar", style={
                                            "width": f"{min((dept.get('budget', 0) or 0) / 10000, 100)}%"
                                        })
                                    ], className="progress mb-2"),
                                ]) for dept in departments[:5]
                            ])
                        ] if departments else [html.P("No departments", className="text-muted text-center")])
                    ])
                ], className="glass-card slide-up stagger-2"),
            ], width=12, lg=4, className="mb-4"),
        ])
        
        # Charts row
        charts_row = dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-chart-pie me-2"),
                            "Mission Status Distribution"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(
                            figure=create_mission_chart(missions),
                            config={'displayModeBar': False},
                            style={"height": "350px"}
                        ) if missions else html.P("No mission data", className="text-muted text-center py-5")
                    ])
                ], className="glass-card slide-up stagger-3")
            ], width=12, md=6, className="mb-4"),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-chart-bar me-2"),
                            "Satellites by Orbit Type"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(
                            figure=create_satellite_chart(db.get_all_satellites()),
                            config={'displayModeBar': False},
                            style={"height": "350px"}
                        ) if db.get_all_satellites() else html.P("No satellite data", className="text-muted text-center py-5")
                    ])
                ], className="glass-card slide-up stagger-4")
            ], width=12, md=6, className="mb-4"),
        ])
        
        return dbc.Container([
            header,
            ticker,
            stat_cards,
            html.Hr(className="my-4", style={"borderColor": "rgba(255,255,255,0.1)"}),
            main_content,
            charts_row,
        ], fluid=True, className="dashboard-container")
        
    except Exception as e:
        return dbc.Container([
            dbc.Alert([
                html.H4([html.I(className="fas fa-exclamation-triangle me-2"), "Error Loading Dashboard"], className="alert-heading"),
                html.P(f"Error: {str(e)}"),
                html.Hr(),
                html.P("Please check your database connection.", className="mb-0")
            ], color="danger", className="fade-in")
        ], fluid=True)


def create_mission_chart(missions):
    """Create mission status pie chart with dark theme"""
    if not missions:
        return go.Figure()
    
    df = pd.DataFrame(missions)
    status_counts = df['status'].value_counts()
    
    fig = go.Figure(data=[go.Pie(
        labels=status_counts.index,
        values=status_counts.values,
        hole=0.5,
        marker=dict(colors=['#10b981', '#f59e0b', '#6366f1', '#ef4444']),
        textfont=dict(color='white', size=14),
    )])
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e5e7eb'),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        margin=dict(t=20, b=20, l=20, r=20),
    )
    
    return fig


def create_satellite_chart(satellites):
    """Create satellite orbit bar chart with dark theme"""
    if not satellites:
        return go.Figure()
    
    df = pd.DataFrame(satellites)
    orbit_counts = df['orbit_type'].value_counts()
    
    fig = go.Figure(data=[go.Bar(
        x=orbit_counts.index,
        y=orbit_counts.values,
        marker=dict(
            color=orbit_counts.values,
            colorscale=[[0, '#6366f1'], [0.5, '#06b6d4'], [1, '#00ff88']],
            line=dict(color='rgba(99, 102, 241, 0.5)', width=1)
        ),
        text=orbit_counts.values,
        textposition='auto',
    )])
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e5e7eb'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', showgrid=True),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)', showgrid=True),
        margin=dict(t=20, b=40, l=40, r=20),
    )
    
    return fig
