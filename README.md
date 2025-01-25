# FBoard
Public version of Plan Board.

Plan board made for tracking construction crew man power, and tracking their assignments. Allows for search for all added employees.

Run the main script to run the program. Will read from an 'output.json' file that will be created in your directory.

Plan Board V.05

Canvas that allows user to create jobs and assign employees to these jobs

There are 5 roles to assign employees to on a job
-PM
-GC
-Foreman
-Superintendent
-Electrician on site

'Add Employee' button:
-Opens add employee dialog, here enter their info:
  -Name
  -Role
  -Skill
    -Helper
    -Junior Mechanic
    -Mechanic
    -Sub Foreman
    -Certifications(editable in 'draggable_box.py'
    -Electrician Rank
    -SST card status
    -Worker Status (contractor or journeyman)
    -NJ or NY certified (both selectable)
    -Current Status
    -Phone Number
-This menu is accessible for any existing employee by right clcking them on the board.

'Add Job Site' button:
  -Adds job site with a name assigned as 'Job site x'
  -Name can be set by right clicking the text in the name.
  -Job sites can be deleted by using the x that is in the corner of each generated job hub

Recommended to follow actions like that with a 'Reload':
  -Reloads all whiteboard graphic elements
  -Reloading fixes issues related to all visual glitches

Notes, notated by square next to job name:
  -When clicking this, you open the note dialog, here you can enter text, and save it as a note
  -Jobs with saved notes will turn yellow, these are accessible in two ways:
  1. Clicking to see, which opens the note dialog
  2. Hovering over a yellow square for a moment, this will have a note open and show the note it contains.

Search functionality:
-By default, will show only unassigned employees. When clicking, employee is highlighted red on board.
-Can filter emeployees shown in the search box, filter by role, and skills
-Show all employees box:
  - This shows all employees, even if assigned to jobs. Will have to use this to search for through all employees.
-With any issues with search box, or filters being stuck, 'Reset Filters' button will fix all issues related to search box not showing proper results.
-Delete or copy employee
  -Select employee, then select desired function using delete or copy button.

Zooming out
-You can zoom out by holding 'Ctrl' + 'M_Wheel_Up' will zoom in, and the other way will zoom out.
-This is very glitched, and requires a reload after each zoom, recommended to not use, unless you can fix it.

Output.json
-You can edit this using any json editor, its pretty easy to understand, once you create your output.json, create an employee and a jobsite, and the format will be clear.

Currently at my company, we use this with the output.json on a shared one drive folder, so we can all access the board, pretty nifty, and inexpensive solution. I also use the clock in info we receive from 'traqspera' our clock in tool, and feed that into a csv into a converter for my json, and update employee statuses.

This is a barebone version of the whiteboard.
