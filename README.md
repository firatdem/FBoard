
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

---

## Getting Started

### Requirements

- Python 3.x
- See `requirements.txt` for full package list

Install dependencies:

pip install -r requirements.txt
Running the App
Simply run:

bash
Copy
Edit
python main.py
The app will:

Auto-generate an output.json file if not found.
Launch the whiteboard GUI using tkinter.
Usage Overview
Creating Job Sites
Click “Add Job Site” to add a new job hub labeled Job site X.
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

## File Structure

FBoard/
├── main.py                  # Entry point for the application

├── whiteboard_online.py    # Core application logic and GUI

├── draggable_box.py        # Logic for draggable employee boxes

├── job_site_hub.py         # Logic for job site hubs

├── constants.py            # Configuration and layout constants

├── output.json             # Auto-saved shared board state

├── requirements.txt        # Required Python packages

└── README.md               # Project documentation

**Customization**
To edit skill labels or add new certifications, modify:
draggable_box.py — for how labels are shown
constants.py — to define new role colors
**Notes**
The app was designed to be shared via OneDrive so multiple users can see updates to output.json.
Some graphical glitches may require a “Reload” using the provided button.
Zooming is experimental and may require a manual reload to fix rendering issues.
**License**
This project is provided as-is for internal or educational use. No warranty or guarantee is provided.
