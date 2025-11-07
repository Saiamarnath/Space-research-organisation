from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
from config.database import db
from datetime import datetime

def common_dashboard_page(user_role=None):
    """
    Common Dashboard - Accessible to both Admin and User
    Read-only view of system statistics and overview
    """
    try:
        mission_stats = db.get_mission_statistics()
        satellite_stats = db.get_satellite_statistics()
        missions = db.get_all_missions()
        
        # Dashboard header
        header = html.Div([
            dbc.Row([
                dbc.Col([
                    html.H1([
                        html.I(className="fas fa-rocket me-3", style={"color": "#6366f1"}),
                        "Mission Control Overview"
                    ], className="mb-0 glow-text", style={"color": "#e5e7eb"}),
                    html.P("Real-time system monitoring and statistics", className="text-secondary mb-0 mt-2")
                ], width="auto"),
                dbc.Col([
                    html.Div([
                        html.Span([
                            html.I(className="fas fa-clock me-2"),
                            html.Span("UTC: ", className="text-secondary me-2"),
                            html.Span(id="live-utc-clock", className="utc-clock"),
                        ])
                    ], className="d-flex justify-content-end align-items-center h-100")
                ], width="auto", className="ms-auto"),
            ], className="align-items-center"),
            
            # Interval for live clock update
            dcc.Interval(id='clock-update', interval=1000, n_intervals=0),
        ], className="dashboard-header mb-4 fade-in")
        
        # Status indicator
        status_banner = html.Div([
            html.Div([
                html.Span(className="status-indicator me-3"),
                html.Span("SYSTEMS OPERATIONAL", className="systems-online"),
            ], className="d-flex align-items-center justify-content-center")
        ], className="text-center mb-4 slide-up")
        
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
                    html.I(className="fas fa-check-circle stat-icon", style={"color": "#06b6d4"}),
                    html.Div([
                        html.Div("0", className="stat-value", **{"data-target": mission_stats.get('completed', 0)}),
                        html.P("Completed Missions", className="stat-label"),
                    ]),
                ], className="stat-card slide-up stagger-3")
            ], width=12, md=6, lg=3, className="mb-3"),
            
            dbc.Col([
                html.Div([
                    html.I(className="fas fa-spinner fa-pulse stat-icon", style={"color": "#f59e0b"}),
                    html.Div([
                        html.Div("0", className="stat-value", **{"data-target": mission_stats.get('in_progress', 0)}),
                        html.P("Active Missions", className="stat-label"),
                    ]),
                ], className="stat-card slide-up stagger-4")
            ], width=12, md=6, lg=3, className="mb-3"),
        ])
        
        # Mission Status Overview
        mission_overview = dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-list-ul me-2"),
                            "Recent Missions"
                        ], className="mb-0 glow-text", style={"color": "#06b6d4"})
                    ]),
                    dbc.CardBody([
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Span(className="badge badge-success me-2", children=mission.get('status', 'Unknown').upper()),
                                    html.Strong(mission.get('mission_name', 'Unknown')),
                                ]),
                                html.Small(f"Launch: {mission.get('launch_date', 'N/A')}", className="text-secondary d-block mt-1"),
                            ], className="mb-3 p-2", style={
                                "borderLeft": "3px solid #10b981" if mission.get('status') == 'Completed' else "3px solid #06b6d4",
                                "background": "rgba(16, 185, 129, 0.05)" if mission.get('status') == 'Completed' else "rgba(6, 182, 212, 0.05)",
                                "borderRadius": "4px"
                            }) for mission in missions[:8]
                        ] if missions else [html.P("No missions available", className="text-muted text-center")])
                    ], style={"maxHeight": "400px", "overflowY": "auto"})
                ], className="glass-card h-100 slide-up")
            ], width=12, md=6, className="mb-4"),
            
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
                ], className="glass-card slide-up")
            ], width=12, md=6, className="mb-4"),
        ])
        
        # Satellite Status Overview
        satellite_overview = dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-satellite me-2"),
                            "Satellite Fleet Status"
                        ], className="mb-0 glow-text", style={"color": "#f59e0b"})
                    ]),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.Div("OPERATIONAL", className="text-center mb-2 fw-bold", style={"color": "#10b981", "fontSize": "0.75rem"}),
                                    html.Div(str(satellite_stats.get('operational', 0)), className="text-center", style={"fontSize": "2.5rem", "fontFamily": "Courier New", "color": "#10b981"}),
                                ], className="p-3", style={"background": "rgba(16, 185, 129, 0.1)", "borderRadius": "8px", "border": "1px solid rgba(16, 185, 129, 0.3)"})
                            ], width=6, className="mb-3"),
                            dbc.Col([
                                html.Div([
                                    html.Div("MAINTENANCE", className="text-center mb-2 fw-bold", style={"color": "#f59e0b", "fontSize": "0.75rem"}),
                                    html.Div(str(satellite_stats.get('maintenance', 0)), className="text-center", style={"fontSize": "2.5rem", "fontFamily": "Courier New", "color": "#f59e0b"}),
                                ], className="p-3", style={"background": "rgba(245, 158, 11, 0.1)", "borderRadius": "8px", "border": "1px solid rgba(245, 158, 11, 0.3)"})
                            ], width=6, className="mb-3"),
                        ]),
                        html.Hr(style={"borderColor": "rgba(255,255,255,0.1)"}),
                        html.Div([
                            html.Div([
                                html.Small("Total Fleet Mass: ", className="text-secondary"),
                                html.Span(f"{satellite_stats.get('total_mass', 0):,.0f} kg", className="text-white fw-bold"),
                            ], className="text-center"),
                        ])
                    ])
                ], className="glass-card slide-up")
            ], width=12, className="mb-4"),
        ])
        
        # Quick links for users
        quick_links = dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-rocket fa-3x mb-3", style={"color": "#6366f1"}),
                            html.H5("View Missions", className="mb-2"),
                            html.P("Explore detailed mission data", className="text-secondary small mb-3"),
                            dbc.Button("Go to Missions", href="/missions", color="primary", size="sm", className="w-100"),
                        ], className="text-center")
                    ])
                ], className="glass-card hover-lift")
            ], width=12, md=4, className="mb-3"),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-satellite fa-3x mb-3", style={"color": "#10b981"}),
                            html.H5("View Satellites", className="mb-2"),
                            html.P("Monitor satellite fleet", className="text-secondary small mb-3"),
                            dbc.Button("Go to Satellites", href="/satellites", color="success", size="sm", className="w-100"),
                        ], className="text-center")
                    ])
                ], className="glass-card hover-lift")
            ], width=12, md=4, className="mb-3"),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-flask fa-3x mb-3", style={"color": "#06b6d4"}),
                            html.H5("Research Facts", className="mb-2"),
                            html.P("Browse research database", className="text-secondary small mb-3"),
                            dbc.Button("Go to Research", href="/research", color="info", size="sm", className="w-100"),
                        ], className="text-center")
                    ])
                ], className="glass-card hover-lift")
            ], width=12, md=4, className="mb-3"),
        ])
        
        return dbc.Container([
            header,
            status_banner,
            stat_cards,
            html.Hr(className="my-4", style={"borderColor": "rgba(255,255,255,0.1)"}),
            mission_overview,
            satellite_overview,
            quick_links,
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
