# main.py
import tkinter as tk
from tkinter import messagebox
import os
import sys
import json  # Import json to create the file if needed

def select_file():
    """Automatically set the file path to 'output.json' in the same directory.
    If the file does not exist, create an empty one with the required structure."""
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundled executable
        script_dir = os.path.dirname(sys.executable)
    else:
        # If the application is run as a normal script
        script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to 'output.json' in the same directory
    file_path = os.path.join(script_dir, 'output.json')

    # Check if the file exists
    if not os.path.isfile(file_path):
        try:
            # Define the initial structure expected by WhiteboardApp
            initial_data = {
                "employees": [],
                "job_sites": [],
                "scale": 1.0,
                "canvas_transform": [0, 0],
                "scroll_x": 0,
                "scroll_y": 0
            }
            # Create 'output.json' with the initial structure
            with open(file_path, 'w') as f:
                json.dump(initial_data, f, indent=4)
            messagebox.showinfo("Info", f"'output.json' was not found and has been created at:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create 'output.json'. Error: {e}\nThe application will close.")
            sys.exit(1)  # Exit the program if the file cannot be created

    return file_path


if __name__ == "__main__":
    # Automatically set mode to 'online' and use the default file path
    selected_mode = 'online'
    shared_file_path = select_file()

    # Import the appropriate WhiteboardApp based on the mode (fixed to 'online')
    try:
        from whiteboard_online import WhiteboardApp
    except ImportError as e:
        messagebox.showerror("Import Error", f"Failed to import WhiteboardApp. Error: {e}")
        sys.exit(1)

    # Initialize the main application window and run the WhiteboardApp
    root = tk.Tk()
    app = WhiteboardApp(root, shared_file_path)  # Pass the auto-selected file path here
    root.protocol("WM_DELETE_WINDOW", app.on_closing)  # Ensure proper closing
    root.mainloop()
