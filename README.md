## **FBoard**  
A simplified, shareable construction workforce planning board designed to manage manpower assignments across various job sites. It enables your team to assign, search, and track employee status visually on a virtual whiteboard.

This is the public version of an internal tool used to coordinate electricians, supervisors, and contractors in real-world field projects. It supports note-taking, zooming, and filtering features, and stores data in a simple `output.json` file that can be shared via cloud storage like OneDrive.

---

## Features

- Interactive drag-and-drop board with job site hubs and employee assignments.
- Visual tracking of employee roles: PM, GC, Foreman, Superintendent, Electrician.
- Add/Edit employee profiles with:
  - Name, role, skill level  
  - Certifications (editable via `draggable_box.py`)  
  - SST card status  
  - Electrician rank  
  - NJ/NY certifications  
  - Worker status (Journeyman or Contractor)  
  - Current status (On-site, Sick, Vacation)  
  - Phone number  
- Right-click to edit existing employees or rename job sites.
- Sticky note system for job sites, color-coded and hoverable.
- Search employees by name, role, certification, and skill level.
- Zoom functionality (Ctrl + Mouse Wheel) — currently experimental.
- Shared `output.json` file can be synced across team members.
- CSV-to-JSON conversion compatible (e.g. from Traqspera time tracking).
- **NEW**: Export to Excel and host a web dashboard for team collaboration.

---

## Getting Started

### Requirements

- Python 3.x  
- See `requirements.txt` for full package list  

Install dependencies:

pip install -r requirements.txt
Running the App
Simply run:

python main.py
The app will:

Auto-generate an output.json file if not found.
Launch the whiteboard GUI using Tkinter.
Usage Overview
Creating Job Sites
Click “Add Job Site” to add a new job hub labeled Job Site X.
Right-click the job name to rename or add an address.
Delete a job site via the red “X” icon in the corner.
Adding Employees
Click “Add Employee” to fill out the employee profile form.
Employees can be assigned by dragging them into boxes on job hubs.
Roles Available

PM (Project Manager)
GC (General Contractor)
Foreman
Superintendent
Electrician (including specialized types like Fire Alarm or Roughing)
Sticky Notes
Each job hub has a square icon beside its name.
Click the square to add a note.
Hover to view the note, or click again to edit/delete.
Searching & Filtering
Use the side panel to:

Search by name
Filter by certifications or skills
Show all employees (even if assigned)
Reset filters if something seems stuck
Excel Export & Live Dashboard (New)
FBoard now includes functionality to export your whiteboard into Excel and publish a live dashboard for team-wide access.

Excel Export
Run the jsonToExcel.py script to convert your current output.json into a structured Excel file:

Job Site Summary – Electrician totals per job site (by skill).
Employees – All employee data (roles, phone, status, certifications, etc.).
Employee List – Grouped by job site for easy crew viewing.
This feature is ideal for internal reporting, emailing stakeholders, or archiving job site rosters.

Live Dashboard Server
Launch a live dashboard using run_dashboard.py, which:

(Optional) Uses a web scraper to fetch the latest CSV from Traqspera.
Converts CSV → JSON → Excel.
Hosts a Dash-based web dashboard that includes:
A bar graph of electrician distribution.
Full job site crew listings.
A request form for suggested changes.
Note:
**The run_dashboard.py script is currently tailored to our internal setup using Selenium for web scraping.
You must adjust this script if you're using your own CSV/JSON file or a different data source.
Comment out steps 1 and 2 to only utilize whiteboard functionality
If you wish to use the web scraping feature, you must also update credentials and paths accordingly.**

Remote Access via Ngrok
Share your live dashboard with others using Ngrok:

ngrok http 5000 # enter this into the ngrok console: https://ngrok.com/downloads/windows?tab=download
This makes your dashboard publicly accessible with a simple URL — perfect for remote supervisors, team leads, or clients who need read-only access.

## File Structure

FYI, example files in 3.21.2025 folder

FBoard/

├── main.py                  # Entry point for the application  
├── whiteboard_online.py    # Core application logic and GUI  
├── draggable_box.py        # Logic for draggable employee boxes  
├── job_site_hub.py         # Logic for job site hubs  
├── constants.py            # Configuration and layout constants  
├── traqsperaCsvToJson.py   # Converts Traqspera CSVs into internal JSON format  
├── jsonToExcel.py          # Converts internal JSON into Excel  
├── dash_board.py           # Dash-based team dashboard UI  
├── run_dashboard.py        # End-to-end automation for live dashboard  
├── webScraper.py           # Internal web scraper (customized for Traqspera)  
├── output.json             # Auto-saved shared board state  
├── output.xlsx             # Excel export (created manually or via automation)  
├── requirements.txt        # Required Python packages  
└── README.md               # Project documentation  
Customization
To edit labels, roles, or visual cues:

draggable_box.py — for how employee labels are shown.
constants.py — to define role colors, spacing, zoom, etc.
Notes
Designed for shared use via cloud sync platforms like OneDrive.
Some graphical glitches may require using the “Reload” button.
Zooming is experimental and may cause rendering issues — use with caution.
License
This project is provided as-is for internal or educational use.
No warranty or guarantee is provided.

Example data and run:

![bar-graph-3 21 2025(morning)](https://github.com/user-attachments/assets/879ad2ae-3f5d-46b6-b65d-4d81f45240dc)
![bar-graph-3 21 2025(morning)(2)](https://github.com/user-attachments/assets/6488c069-de1b-4997-b6e3-b38170d99829)
![Board-3 21(1)](https://github.com/user-attachments/assets/66d913e1-0d9e-4aa5-bcaa-17dd1a69a8eb)
![Board-3 21(2)](https://github.com/user-attachments/assets/99299feb-1e3e-40ec-88ab-18e5fa7fb53e)
