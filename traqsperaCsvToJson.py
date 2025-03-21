# csv_to_json.py
import pandas as pd
import json
import os
import sys

# Default paths (will be overridden by the downloaded CSV path if provided)
DEFAULT_CSV_FILE_PATH = r'C:\Users\Work\Downloads\Employee-Locations-2025-03-03-to-2025-03-03.csv'
JSON_FILE_PATH = r'C:\Users\Work\PycharmProjects\PlanBoard\output.json'
UPDATED_JSON_FILE_PATH = 'output.json'
CHANGES_LOG_PATH = 'relocation_changes.log'  # Path to save relocation logs

def load_csv(csv_path):
    """Load only 'First Name', 'Last Name', and 'Job Description' from the CSV into a pandas DataFrame."""
    try:
        df = pd.read_csv(
            csv_path,
            usecols=['First Name', 'Last Name', 'Job Description'],
            dtype=str,
            skipinitialspace=True  # This skips spaces after delimiters
        )
        print(f"[INFO] CSV data loaded successfully from '{csv_path}'.")
        print(f"[DEBUG] CSV DataFrame Head:\n{df.head()}\n")
        print(f"[DEBUG] CSV Columns: {df.columns.tolist()}\n")
        return df
    except ValueError as ve:
        print(f"[ERROR] Missing expected columns in CSV: {ve}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Error loading CSV file: {e}")
        sys.exit(1)


def load_json(json_path):
    """Load JSON data into a Python dictionary."""
    try:
        with open(json_path, 'r') as file:
            data = json.load(file)
        print(f"[INFO] JSON data loaded successfully from '{json_path}'.")
        employees_count = len(data.get('employees', []))
        job_sites_count = len(data.get('job_sites', []))
        print(f"[DEBUG] Number of Employees Loaded: {employees_count}")
        print(f"[DEBUG] Number of Job Sites Loaded: {job_sites_count}\n")
        return data
    except json.JSONDecodeError as jde:
        print(f"[ERROR] JSON decoding failed: {jde}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Error loading JSON file: {e}")
        sys.exit(1)


def save_json(data, json_path):
    """Save the updated data back to a JSON file."""
    try:
        with open(json_path, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"[INFO] Updated JSON data saved to '{json_path}'.")
    except Exception as e:
        print(f"[ERROR] Error saving JSON file: {e}")
        sys.exit(1)


def concatenate_names(first, last):
    """Concatenate first and last names with a space."""
    return f"{first.strip()} {last.strip()}"


def update_employee_locations(csv_df, json_data):
    """
    Merge CSV data with JSON data to update employee locations.
    Also, mark any employee not present in the CSV as "Sick" (only if their role is Electrician or Roughing Electrician).
    """
    employees = json_data.get('employees', [])
    # Build a lookup for job sites based on lowercased site names.
    job_sites = {site['name'].strip().lower(): site for site in json_data.get('job_sites', [])}
    unmatched_names = []
    relocated_employees = []  # Track relocation/status changes.

    # Create a lookup dictionary for employees based on the 'text' field (full name).
    employee_lookup = {emp['text'].strip().lower(): emp for emp in employees}
    print(f"[DEBUG] Employee Lookup Keys (Sample): {list(employee_lookup.keys())[:5]}...\n")
    print(f"[DEBUG] Job Sites Available (Total: {len(job_sites)}): {list(job_sites.keys())[:5]}...\n")

    # Build a set of employee names detected in the CSV.
    csv_employee_names = set()

    # Define allowed roles for being marked as sick.
    allowed_sick_roles = {"electrician", "roughing electrician", "foreman", "fire alarm electrician"}

    for index, row in csv_df.iterrows():
        # Extract and clean data from the CSV row.
        first_name = row.get('First Name', '').strip()
        last_name = row.get('Last Name', '').strip()
        job_description = row.get('Job Description', '').strip()

        # Validate essential fields.
        if not first_name or not last_name:
            print(f"        [WARNING] Missing first or last name in row {index + 1}. Skipping this row.\n")
            continue

        # Concatenate full name and add to the CSV set.
        full_name = f"{first_name} {last_name}"
        full_name_key = full_name.lower()
        csv_employee_names.add(full_name_key)

        # Debug info.
        print(f"[DEBUG] Processing Row {index + 1}:")
        print(f"        First Name      : {first_name}")
        print(f"        Last Name       : {last_name}")
        print(f"        Job Description : {job_description}")

        if not job_description:
            print(f"        [WARNING] Missing 'Job Description' for '{full_name}'. Skipping this row.\n")
            continue

        # Lookup employee in JSON data.
        employee = employee_lookup.get(full_name_key)
        if employee:
            old_job_site = employee.get('job_site', 'N/A').strip()
            print(f"        [INFO] Employee '{full_name}' found. Current Job Site: '{old_job_site}'")

            new_job_site_raw = job_description
            new_job_site_key = new_job_site_raw.lower()
            print(f"        [DEBUG] Attempting to update to New Job Site: '{new_job_site_raw}'")

            if new_job_site_key in job_sites:
                new_job_site = job_sites[new_job_site_key]['name']
                print(f"        [INFO] Mapped Job Description to Job Site: '{new_job_site}'")

                # Determine the new status based on the new job site.
                if new_job_site.lower() == 'sick':
                    emp_role = employee.get('role', '').strip().lower()
                    if emp_role not in allowed_sick_roles:
                        print(f"        [INFO] Employee '{full_name}' with role '{employee.get('role', '')}' is not allowed to be marked as sick. Skipping update.\n")
                        continue
                    new_status = "Sick"
                else:
                    new_status = "On-site"

                # Update if either the job site or the status needs to change.
                if (old_job_site.lower() != new_job_site_key) or (employee.get('current_status', '').lower() != new_status.lower()):
                    old_status = employee.get('current_status', 'N/A')
                    employee['job_site'] = new_job_site
                    employee['current_status'] = new_status
                    relocation_record = {
                        'Employee Name': full_name,
                        'Old Job Site': old_job_site,
                        'New Job Site': new_job_site
                    }
                    relocated_employees.append(relocation_record)
                    print(f"        [INFO] Updated '{full_name}': Job Site from '{old_job_site}' to '{new_job_site}' and Status from '{old_status}' to '{new_status}'.\n")
                else:
                    print(f"        [INFO] No update required for '{full_name}'; already at '{new_job_site}' with status '{new_status}'.\n")
            else:
                print(f"        [WARNING] Job site '{new_job_site_raw}' for '{full_name}' not found in JSON 'job_sites'. Assigning 'Unassigned'.\n")
                new_job_site = "Unassigned"
                new_status = "On-site"
                if (old_job_site.lower() != new_job_site.lower()) or (employee.get('current_status', '').lower() != new_status.lower()):
                    old_status = employee.get('current_status', 'N/A')
                    employee['job_site'] = new_job_site
                    employee['current_status'] = new_status
                    relocation_record = {
                        'Employee Name': full_name,
                        'Old Job Site': old_job_site,
                        'New Job Site': new_job_site
                    }
                    relocated_employees.append(relocation_record)
                    print(f"        [INFO] Updated '{full_name}': Job Site from '{old_job_site}' to '{new_job_site}' and Status from '{old_status}' to '{new_status}'.\n")
                else:
                    print(f"        [INFO] No update required for '{full_name}'; already at '{new_job_site}' with status '{new_status}'.\n")
                unmatched_names.append(full_name)
        else:
            print(f"        [WARNING] Employee '{full_name}' not found in JSON data.\n")
            unmatched_names.append(full_name)

    # After processing CSV rows, mark any employee in the JSON not found in CSV as "Sick"
    # but only if their role is in the allowed list.
    for emp in employees:
        emp_key = emp.get('text', '').strip().lower()
        if emp_key not in csv_employee_names:
            emp_role = emp.get('role', '').strip().lower()
            if emp_role in allowed_sick_roles:
                old_status = emp.get('current_status', 'N/A')
                emp['current_status'] = "Sick"
                print(f"[INFO] Marking '{emp.get('text', '')}' as Sick (not detected in CSV).")
                relocation_record = {
                    'Employee Name': emp.get('text', ''),
                    'Old Job Site': emp.get('job_site', ''),
                    'New Job Site': emp.get('job_site', '')  # Job site remains unchanged.
                }
                relocated_employees.append(relocation_record)
            else:
                print(f"[INFO] Not marking '{emp.get('text', '')}' as Sick because role '{emp.get('role', '')}' is not allowed.")

    return unmatched_names, relocated_employees


def save_relocation_log(relocated_employees, log_path):
    """Save the list of relocated employees to a log file."""
    try:
        with open(log_path, 'w') as log_file:
            log_file.write("Relocation/Status Changes Log\n")
            log_file.write("=============================\n\n")
            for record in relocated_employees:
                log_file.write(f"Employee Name : {record['Employee Name']}\n")
                log_file.write(f"Old Job Site  : {record['Old Job Site']}\n")
                log_file.write(f"New Job Site  : {record['New Job Site']}\n")
                log_file.write("-----------------------------\n")
        print(f"[INFO] Relocation/status changes logged to '{log_path}'.")
    except Exception as e:
        print(f"[ERROR] Error saving relocation log: {e}")


def main(csv_path=DEFAULT_CSV_FILE_PATH):
    # Check if files exist
    if not os.path.exists(csv_path):
        print(f"[ERROR] CSV file not found at path: '{csv_path}'")
        sys.exit(1)
    if not os.path.exists(JSON_FILE_PATH):
        print(f"[ERROR] JSON file not found at path: '{JSON_FILE_PATH}'")
        sys.exit(1)

    # Load data
    csv_df = load_csv(csv_path)
    json_data = load_json(JSON_FILE_PATH)

    # Update employee locations and statuses.
    unmatched, relocated = update_employee_locations(csv_df, json_data)

    # Save updated JSON data.
    save_json(json_data, UPDATED_JSON_FILE_PATH)

    # Save relocation/status change log if there are any records.
    if relocated:
        save_relocation_log(relocated, CHANGES_LOG_PATH)
    else:
        print("\n[INFO] No employee relocations or status changes were made.")

    # Report unmatched names.
    if unmatched:
        print("\n[WARNING] Unmatched Employee Names:")
        for name in unmatched:
            print(f" - {name}")
    else:
        print("\n[INFO] All employee names matched successfully.")

    # Print a summary.
    if relocated:
        print(f"\n[INFO] Total Employees Updated: {len(relocated)}")
    else:
        print("\n[INFO] No updates to summarize.")


if __name__ == "__main__":
    # Allow overriding the CSV path via command-line argument
    csv_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CSV_FILE_PATH
    main(csv_path)
