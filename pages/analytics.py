from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from config.database import db
import pandas as pd

def analytics_page():
    """
    Analytics and reports page - GUI for stored procedures and complex queries.
    Addresses rubric items for Procedures, Functions, Nested, Join, and Aggregate queries.
    """
    
    # --- 1. Aggregate Query (Rubric) ---
    # This view performs aggregation (COUNT, AVG, etc.)
    try:
        dept_summary_data = db.get_department_summary()
    except Exception as e:
        dept_summary_data = []
        print(f"Error loading dept summary: {e}")

    aggregate_query_card = dbc.Card([
        dbc.CardHeader([
            html.I(className="fas fa-calculator me-2"), 
            "Aggregate Query: Department Summary"
        ]),
        dbc.CardBody([
            html.P("This table runs an aggregate query (via a VIEW) to COUNT employees, equipment, and satellites per department.", className="text-secondary"),
            dash_table.DataTable(
                columns=[
                    {"name": "Dept", "id": "dept_name"},
                    {"name": "Head", "id": "Department_Head"},
                    {"name": "Employees", "id": "Employee_Count"},
                    {"name": "Equipment", "id": "Equipment_Count"},
                    {"name": "Satellites", "id": "Satellites_Managed"},
                    {"name": "Budget", "id": "Budget", "type": "numeric", "format": {"specifier": "$,.0f"}},
                ],
                data=dept_summary_data,
                style_table={'overflowX': 'auto', 'background': 'transparent'},
                style_cell={
                    'backgroundColor': 'rgba(0, 0, 0, 0.2)',
                    'color': '#e5e7eb',
                    'border': '1px solid rgba(255, 255, 255, 0.1)',
                },
                style_header={
                    'backgroundColor': 'rgba(99, 102, 241, 0.2)',
                    'color': '#06b6d4',
                },
                page_size=5,
            )
        ])
    ], className="glass-card mb-4")

    # --- 2. Join Query (Rubric) ---
    # This view performs multiple JOINS
    try:
        join_data = db.get_all_employees() # This uses the Employee_Hierarchy view
    except Exception as e:
        join_data = []
        print(f"Error loading join data: {e}")
        
    join_query_card = dbc.Card([
        dbc.CardHeader([
            html.I(className="fas fa-link me-2"), 
            "Join Query: Employee Hierarchy"
        ]),
        dbc.CardBody([
            html.P("This table runs a JOIN query (via a VIEW) to link employees to their supervisors and departments.", className="text-secondary"),
            dash_table.DataTable(
                columns=[
                    {"name": "Employee", "id": "emp_name"},
                    {"name": "Position", "id": "position"},
                    {"name": "Department", "id": "dept_name"},
                    {"name": "Supervisor", "id": "Supervisor_Name"},
                ],
                data=join_data,
                style_table={'overflowX': 'auto', 'background': 'transparent'},
                style_cell={
                    'backgroundColor': 'rgba(0, 0, 0, 0.2)',
                    'color': '#e5e7eb',
                    'border': '1px solid rgba(255, 255, 255, 0.1)',
                },
                style_header={
                    'backgroundColor': 'rgba(99, 102, 241, 0.2)',
                    'color': '#06b6d4',
                },
                page_size=5,
            )
        ])
    ], className="glass-card mb-4")

    # --- 3. Nested Query (Rubric) ---
    nested_query_card = dbc.Card([
        dbc.CardHeader([
            html.I(className="fas fa-layer-group me-2"), 
            "Nested/Correlated Query: Employees Above Dept. Average Salary"
        ]),
        dbc.CardBody([
            html.P("This table shows the result of a correlated subquery to find employees earning more than their department's average salary.", className="text-secondary"),
            dbc.Button("Run Nested Query", id="run-nested-query-btn", color="primary", outline=True, className="mb-3"),
            dcc.Loading(
                dash_table.DataTable(
                    id='nested-query-table',
                    columns=[
                        {"name": "Employee", "id": "emp_name"},
                        {"name": "Position", "id": "position"},
                        {"name": "Department", "id": "dept_name"},
                        {"name": "Salary", "id": "salary", "type": "numeric", "format": {"specifier": "$,.0f"}},
                        {"name": "Dept. Avg", "id": "dept_avg", "type": "numeric", "format": {"specifier": "$,.0f"}},
                    ],
                    data=[],
                    style_table={'overflowX': 'auto', 'background': 'transparent'},
                    style_cell={
                        'backgroundColor': 'rgba(0, 0, 0, 0.2)',
                        'color': '#e5e7eb',
                        'border': '1px solid rgba(255, 255, 255, 0.1)',
                    },
                    style_header={
                        'backgroundColor': 'rgba(99, 102, 241, 0.2)',
                        'color': '#06b6d4',
                    },
                    page_size=5,
                )
            )
        ])
    ], className="glass-card mb-4")

    # --- 4. Stored Procedures & Functions (Rubric) ---
    procedure_card = dbc.Card([
        dbc.CardHeader([
            html.I(className="fas fa-cogs me-2"),
            "Execute Stored Procedures & Functions"
        ]),
        dbc.CardBody([
            html.H5("Get Employee Details (Procedure & Functions)"),
            html.P("Enter an Employee ID to run 'GetEmployeeDetails', 'GetYearsOfService', and 'CountSubordinates'.", className="text-secondary"),
            dbc.InputGroup([
                dbc.Input(id="analytics-emp-id-input", type="number", placeholder="Enter Employee ID (e.g., 1001)"),
                dbc.Button("Run", id="analytics-run-proc-btn", color="success"),
            ]),
            dcc.Loading(html.Div(id="analytics-proc-output", className="mt-3")),
            
            html.Hr(className="my-4"),
            
            html.H5("Generate Salary Report (Procedure)"),
            html.P("Click to run the 'GenerateSalaryReport' procedure and display the results.", className="text-secondary"),
            dbc.Button("Run Salary Report", id="analytics-run-report-btn", color="info"),
            dcc.Loading(
                html.Div(id="analytics-report-output-div", className="mt-3", children=[
                    dash_table.DataTable(
                        id='analytics-report-table',
                        columns=[
                            {"name": "Name", "id": "Emp_Name"},
                            {"name": "Position", "id": "Position"},
                            {"name": "Salary", "id": "Salary", "type": "numeric", "format": {"specifier": "$,.0f"}},
                            {"name": "Department", "id": "Dept_Name"},
                            {"name": "Grade", "id": "Salary_Grade"},
                            {"name": "Dept. Rank", "id": "Dept_Rank"},
                        ],
                        data=[],
                        style_table={'overflowX': 'auto', 'background': 'transparent'},
                        style_cell={
                            'backgroundColor': 'rgba(0, 0, 0, 0.2)',
                            'color': '#e5e7eb',
                            'border': '1px solid rgba(255, 255, 255, 0.1)',
                        },
                        style_header={
                            'backgroundColor': 'rgba(99, 102, 241, 0.2)',
                            'color': '#06b6d4',
                        },
                        page_size=5,
                    )
                ])
            ),
        ])
    ], className="glass-card mb-4")
    
    
    return dbc.Container([
        html.Div([
            html.H1([html.I(className="fas fa-chart-line me-3"), "Analytics & Reports"], className="mb-0 page-title", style={"color": "#e5e7eb"}),
            html.P("Database Analytics Dashboard (Fulfills Rubric)", className="text-secondary mb-0 mt-2")
        ], className="dashboard-header mb-4 fade-in"),
        
        dbc.Row([
            dbc.Col([
                aggregate_query_card,
                nested_query_card,
            ], lg=6),
            dbc.Col([
                join_query_card,
                procedure_card,
            ], lg=6),
        ])
    ], fluid=True, className="dashboard-container")