from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
from config.database import db

def employees_page():
    """Employee management page - ADMIN ONLY"""
    employees = db.get_all_employees()
    
    if not employees:
        return dbc.Container([
            html.H2("👨‍🚀 Employees", className="mb-4 page-title"),
            dbc.Alert("No employees found", color="info")
        ], fluid=True, className="dashboard-container")
    
    df = pd.DataFrame(employees)
    
    table = dash_table.DataTable(
        id='employees-table',
        columns=[
            {"name": "ID", "id": "emp_id"},
            {"name": "Name", "id": "emp_name"},
            {"name": "Position", "id": "position"},
            {"name": "Department", "id": "dept_name"},
            {"name": "Salary", "id": "salary", "type": "numeric", "format": {"specifier": "$,.2f"}},
            {"name": "Supervisor", "id": "supervisor_name"},
        ],
        data=df.to_dict('records'),
        style_table={'overflowX': 'auto', 'background': 'transparent'},
        style_cell={
            'textAlign': 'left',
            'padding': '12px',
            'backgroundColor': 'rgba(0, 0, 0, 0.2)',
            'color': '#e5e7eb',
            'border': '1px solid rgba(255, 255, 255, 0.1)',
            'fontFamily': 'Inter, sans-serif'
        },
        style_header={
            'backgroundColor': 'rgba(99, 102, 241, 0.2)',
            'fontWeight': '700',
            'color': '#06b6d4',
            'textTransform': 'uppercase',
            'fontSize': '0.875rem',
            'letterSpacing': '0.05em',
            'border': '1px solid rgba(99, 102, 241, 0.3)'
        },
        page_size=10,
        sort_action='native',
        filter_action='native'
    )
    
    salary_chart = None
    try:
        import plotly.express as px
        salary_chart = dcc.Graph(
            figure=px.box(
                df,
                x='dept_name',
                y='salary',
                title="Salary Distribution by Department",
                labels={'dept_name': 'Department', 'salary': 'Salary ($)'}
            )
        )
    except Exception:
        salary_chart = dbc.Alert("Salary analysis requires plotly", color="warning")

    return dbc.Container([
        html.H2("👨‍🚀 Employees", className="mb-4 page-title"),
        dbc.Card([
            dbc.CardHeader([html.I(className="fas fa-users me-2"), "Employee Directory"], className="mb-0"),
            dbc.CardBody(table, className="p-0")
        ], className="mb-4 glass-card"),
        dbc.Card([
            dbc.CardHeader([html.I(className="fas fa-chart-line me-2"), "Salary Analysis"], className="mb-0"),
            dbc.CardBody(salary_chart)
        ], className="glass-card")
    ], fluid=True, className="dashboard-container")
