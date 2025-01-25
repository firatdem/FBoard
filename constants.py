# Example ROLE_COLORS definition
ROLE_COLORS = {
    "PM": "blue",
    "GM": "green",
    "Foreman": "orange",
    'Super': "blue",  # Add this line
    "Electrician": "red",
    "Fire Alarm Electrician": "purple",
    "Roughing Electrician": "yellow",
    # Add other roles as needed
}


VERTICAL_SPACING = 150  # Constant vertical spacing between rows // CHANGED FROM 300
ELECTRICIAN_BOX_HEIGHT = 730  # Height of the electrician box
JOB_HUB_WIDTH = 900  # Width of the job site hub
JOB_HUB_HEIGHT = 1100  # Height of the job site hub
BOX_HEIGHT = 70  # Height of the non-electrician boxes // CHANGED FROM 90
DEFAULT_EMPLOYEE_X = 1200  # Where non-assigned employees get placed
DEFAULT_EMPLOYEE_Y = -3300
GRID_SIZE = 30
DRAG_DELAY = 200  # Delay in milliseconds
JOB_HUB_HEIGHT_COLLAPSED = 250
MAX_COLUMNS = 8  # Maximum number of columns for job site hubs
DEFAULT_ZOOM_SCALE = 0.225  # Adjust this value as needed (e.g., 1.0, 1.5, 0.75)

