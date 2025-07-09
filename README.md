QUICK DISCLAIMER: This is the public version of an internal tool used to coordinate electricians, supervisors, and contractors in real-world field projects.

## FBoard – Visual Workforce Planning for Job Sites

FBoard is a lightweight, shareable planning board for coordinating field crews across construction job sites. Built for teams managing electricians, supervisors, and contractors, it lets you visually assign workers, add notes, filter by skill, and export job rosters—all from one interactive whiteboard.

Originally developed for internal field operations, this open version is easy to customize and share via platforms like OneDrive or Dropbox.

## ⚙️ How It Works

1. 🧍 Add employee profiles
2. 📌 Assign employees to job sites via drag-and-drop
3. 📝 Add sticky notes and job site info
4. 🔍 Search and filter workers by skill or status
5. 📊 Export your plan to Excel or share it as a live dashboard

## 🧪 Try It Out

1. Clone the repo  
2. Run `python main.py`  
3. Add job sites, employees, and try dragging them around  
4. Export to Excel with `jsonToExcel.py`  
5. (Optional) Run `run_dashboard.py` to host a local dashboard

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

```bash
pip install -r requirements.txt
```
Running the App
Simply run:
```bash
python main.py
```
The app will:
```bash
- Auto-generate an output.json file if not found.
- Launch the whiteboard GUI using Tkinter.
- Usage Overview
- Creating Job Sites
- Click “Add Job Site” to add a new job hub labeled Job Site X.
- Right-click the job name to rename or add an address.
- Delete a job site via the red “X” icon in the corner.
- Adding Employees
- Click “Add Employee” to fill out the employee profile form.
- Employees can be assigned by dragging them into boxes on job hubs.
```

<details>
<summary>📋 Available Roles</summary>

- PM (Project Manager)  
- GC (General Contractor)  
- Foreman  
- Superintendent  
- Electrician (Fire Alarm, Roughing, etc.)

</details>

Use the side panel to:
```bash
- Search by name
- Filter by certifications or skills
- Show all employees (even if assigned)
- Reset filters if something seems stuck
- Excel Export & Live Dashboard (New)
- FBoard now includes functionality to export your whiteboard into Excel and publish a live dashboard for team-wide access.
```
### 📤 Excel Export (for Email/Reporting)

Run:

```bash
python jsonToExcel.py
- Job Site Summary – Electrician totals per job site (by skill).
- Employees – All employee data (roles, phone, status, certifications, etc.).
- Employee List – Grouped by job site for easy crew viewing.
- This feature is ideal for internal reporting, emailing stakeholders, or archiving job site rosters.
```
Live Dashboard Server
Launch a live dashboard using **run_dashboard.py**, which:
```bash
- (Optional) Uses a web scraper to fetch the latest CSV from Traqspera.
- Converts CSV → JSON → Excel.
- Hosts a Dash-based web dashboard that includes:
- A bar graph of electrician distribution.
- Full job site crew listings.
- A request form for suggested changes.
```

Note:
**The run_dashboard.py script is currently tailored to our internal setup using Selenium for web scraping.
You must adjust this script if you're using your own CSV/JSON file or a different data source.
Comment out steps 1 and 2 to only utilize whiteboard functionality
If you wish to use the web scraping feature, you must also update credentials and paths accordingly.**

Remote Access via Ngrok

Share your live dashboard with others using Ngrok:
```bash
ngrok http 5000 # enter this into the ngrok console: https://ngrok.com/downloads/windows?tab=download
This makes your dashboard publicly accessible with a simple URL — perfect for remote supervisors, team leads, or clients who need read-only access.
```
## File Structure

FYI, example files in 3.21.2025 folder

FBoard/
```bash
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
```
## 🛠️ Customization

You can edit roles, colors, and layout by modifying:

- `draggable_box.py` – Controls how employee labels are shown
- `constants.py` – Defines role colors, box size, zoom behavior, spacing, etc.

## 📝 Notes

- Designed for shared use via OneDrive, Dropbox, etc.
- Zooming is experimental and may cause rendering issues
- Use the “Reload” button if graphical glitches occur

## 📄 License

This project is provided as-is for internal or educational use.  
No warranty or guarantee is provided.

Example data and run:

![bar-graph-3 21 2025(morning)](https://github.com/user-attachments/assets/879ad2ae-3f5d-46b6-b65d-4d81f45240dc)
![bar-graph-3 21 2025(morning)(2)](https://github.com/user-attachments/assets/6488c069-de1b-4997-b6e3-b38170d99829)
![Board-3 21(1)](https://github.com/user-attachments/assets/66d913e1-0d9e-4aa5-bcaa-17dd1a69a8eb)
![Board-3 21(2)](https://github.com/user-attachments/assets/99299feb-1e3e-40ec-88ab-18e5fa7fb53e)
