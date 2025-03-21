import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
import pandas as pd
import plotly.express as px
import socket
import os

def run_dashboard():
    EXCEL_FILE = "output.xlsx"
    REQUESTS_FILE = "requests.csv"

    # Ensure the requests CSV exists
    if not os.path.exists(REQUESTS_FILE):
        pd.DataFrame(columns=["Request"]).to_csv(REQUESTS_FILE, index=False)

    # Load Job Site Summary
    try:
        job_site_summary = pd.read_excel(EXCEL_FILE, sheet_name="Job Site Summary")
    except Exception as e:
        print(f"[ERROR] Could not load Excel file: {e}")
        job_site_summary = pd.DataFrame()

    # Create dark-themed bar chart if data is valid
    if not job_site_summary.empty and "Total Electricians" in job_site_summary.columns:
        job_site_summary = job_site_summary.sort_values("Total Electricians", ascending=False)
        fig = px.bar(
            job_site_summary,
            x="Job Site",
            y="Total Electricians",
            title="Total Electricians per Job Site",
            labels={"Total Electricians": "Total Electricians", "Job Site": "Job Site"},
            template="plotly_dark"
        )
    else:
        fig = {}

    # Load Employee List
    try:
        employee_list = pd.read_excel(EXCEL_FILE, sheet_name="Employee List")
    except Exception as e:
        print(f"[ERROR] Could not load Employee List: {e}")
        employee_list = pd.DataFrame()

    # Load Employees sheet for status
    try:
        employees_df = pd.read_excel(EXCEL_FILE, sheet_name="Employees")
    except Exception as e:
        print(f"[ERROR] Could not load Employees sheet: {e}")
        employees_df = pd.DataFrame()

    # Forward-fill ONLY the "Job Site" column if needed
    employee_list["Job Site"] = employee_list["Job Site"].fillna(method="ffill")

    # Exclude GM, PM, Super roles
    filtered_employee_list = employee_list[~employee_list['Role'].isin(['GM', 'PM', 'Super'])]

    # Merge in employee status, excluding Sick employees
    if not employees_df.empty and "current_status" in employees_df.columns:
        employees_df = employees_df[['text', 'current_status']]
        employees_df.rename(columns={'text': 'Employee Name'}, inplace=True)
        filtered_employee_list = filtered_employee_list.merge(employees_df, on='Employee Name', how='left')
        filtered_employee_list = filtered_employee_list[filtered_employee_list['current_status'] != 'Sick']
    else:
        print("[WARNING] 'current_status' column not found in Employees sheet. Skipping sickness filter.")

    # Group employees by Job Site
    grouped_employees = (
        filtered_employee_list
        .groupby("Job Site")["Employee Name"]
        .apply(lambda x: ', '.join(x.dropna()))
        .reset_index()
    )

    # Merge group with job site summary
    grouped_employees = grouped_employees.merge(
        job_site_summary[['Job Site', 'Total Electricians']],
        on='Job Site',
        how='left'
    )
    grouped_employees = grouped_employees.sort_values(by='Total Electricians', ascending=False)

    # Filter out any job sites with no employees
    grouped_employees["Employee Name"] = grouped_employees["Employee Name"].fillna("")
    grouped_employees = grouped_employees[grouped_employees["Employee Name"].str.strip() != ""]

    # Build display for crew elements
    crew_elements = []
    for _, row in grouped_employees.iterrows():
        crew_elements.extend([
            html.H4(row["Job Site"], className="mt-3"),
            html.P(row["Employee Name"]),
            html.Hr(className="mb-3")
        ])

    # Pre-load the requested changes from the CSV file
    if os.path.exists(REQUESTS_FILE):
        requests_df = pd.read_csv(REQUESTS_FILE)
        initial_requests = [html.Li(req) for req in requests_df["Request"].dropna().tolist()]
    else:
        initial_requests = []

    local_ip = socket.gethostbyname(socket.gethostname())

    # Initialize Dash app with a dark theme (DARKLY)
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

    app.layout = dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Team Dashboard", className="text-center text-light mb-4"), width=12)
        ]),
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dcc.Graph(id="bar-graph", figure=fig),
                    className="shadow-sm"
                ),
                width=12
            )
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(
                html.Div(crew_elements, className="p-3"),
                width=12
            )
        ], className="mb-4"),
        dbc.Row([dbc.Col(html.H2("Request Changes", className="text-light"), width=12)]),
        dbc.Row([
            dbc.Col(
                # Set maxLength=120 for the text input
                dbc.Input(id="request-input", type="text", placeholder="Enter your change request...",
                          className="mb-2", maxLength=120),
                width=8
            ),
            dbc.Col(
                dbc.Button("Submit", id="submit-request", n_clicks=0, color="primary", className="mb-2"),
                width=2
            ),
            dbc.Col(
                dbc.Button("Clear Requests", id="clear-requests", n_clicks=0, color="danger", className="mb-2"),
                width=2
            )
        ], align="center"),
        # Row to display confirmation messages
        dbc.Row([
            dbc.Col(html.Div(id="request-confirmation", className="mt-2 text-success"), width=12)
        ]),
        # Row to display the heading for submitted changes
        dbc.Row([dbc.Col(html.H3("Submitted Requests", className="text-light"), width=12)]),
        # Row to display all submitted requests (pre-populated on load)
        dbc.Row([
            dbc.Col(
                html.Ul(id="request-list", className="list-unstyled", children=initial_requests,
                        style={"maxHeight": "300px", "overflowY": "auto"}),
                width=12
            )
        ]),
        # Hidden Interval component for delaying the submit button (5 seconds)
        dcc.Interval(id="submit-interval", interval=5000, disabled=True)
    ], fluid=True, className="mt-4", style={"backgroundColor": "#343a40", "minHeight": "100vh"})

    @app.callback(
        [Output("request-confirmation", "children"),
         Output("request-list", "children"),
         Output("request-input", "value")],
        [Input("submit-request", "n_clicks"),
         Input("clear-requests", "n_clicks")],
        [State("request-input", "value")]
    )
    def handle_request(submit_clicks, clear_clicks, request_text):
        ctx = dash.callback_context
        if not ctx.triggered:
            requests_df = pd.read_csv(REQUESTS_FILE)
            request_items = [html.Li(req) for req in requests_df["Request"].dropna().tolist()]
            return "", request_items, ""
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == "submit-request" and request_text:
            new_request = pd.DataFrame([[request_text]], columns=["Request"])
            new_request.to_csv(REQUESTS_FILE, mode='a', header=False, index=False)
        elif button_id == "clear-requests":
            pd.DataFrame(columns=["Request"]).to_csv(REQUESTS_FILE, index=False)

        requests_df = pd.read_csv(REQUESTS_FILE)
        request_items = [html.Li(req) for req in requests_df["Request"].dropna().tolist()]
        return "Request updated successfully!", request_items, ""

    # Callback to disable the submit button for 5 seconds after being pressed
    @app.callback(
        [Output("submit-request", "disabled"),
         Output("submit-interval", "disabled"),
         Output("submit-interval", "n_intervals")],
        [Input("submit-request", "n_clicks"),
         Input("submit-interval", "n_intervals")],
        [State("submit-request", "disabled"),
         State("submit-interval", "disabled")]
    )
    def update_submit_button(submit_clicks, interval_ticks, btn_disabled, interval_disabled):
        ctx = dash.callback_context
        if not ctx.triggered:
            # Default state: button enabled, interval disabled
            return False, True, 0

        trigger = ctx.triggered[0]['prop_id'].split('.')[0]
        if trigger == "submit-request":
            # When submit is clicked, disable the button and enable the interval (reset interval counter to 0)
            return True, False, 0
        elif trigger == "submit-interval":
            # Once the interval ticks (5 seconds), re-enable the button and disable the interval again
            if interval_ticks >= 1:
                return False, True, 0
            return btn_disabled, interval_disabled, interval_ticks

    print(f"\nDashboard is running at: http://{local_ip}:5000\n")
    app.run_server(debug=False, use_reloader=False, host="0.0.0.0", port=5000)

if __name__ == "__main__":
    run_dashboard()
