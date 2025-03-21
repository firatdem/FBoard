from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import glob
from dotenv import load_dotenv, dotenv_values

# 🔹 Load environment variables from .env file
load_dotenv()
config = dotenv_values("C:/Users/Work/PycharmProjects/PlanBoard/.env")  # Adjust path

USERNAME = config.get("USER-NAME")  # Fetch username safely
PASSWORD = config.get("PASSWORD")  # Fetch password safely


def setup_driver():
    """Configure and return a Selenium WebDriver instance (headless mode)."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")  # Enable headless mode, disable for debugging
    options.add_argument("--disable-gpu")  # Helps with rendering issues
    options.add_argument("--window-size=1920x1080")  # Set screen size for consistency
    driver = webdriver.Chrome(options=options)
    return driver


def login(driver, wait):
    """Logs into the Trimble portal using Selenium."""
    driver.get("https://usecorp.traqspera.com/timesheets")

    # Enter username
    email_input = wait.until(EC.presence_of_element_located((By.ID, "username-field")))
    email_input.send_keys(USERNAME)
    email_input.send_keys(Keys.TAB)
    time.sleep(1)

    # Click 'Next' button
    next_button = wait.until(EC.element_to_be_clickable((By.ID, "enter_username_submit")))
    next_button.click()
    print("Email entered and 'Next' button clicked.")
    time.sleep(5)

    # Enter password
    password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.RETURN)
    print("Password entered and login submitted.")
    time.sleep(5)


def navigate_to_exports(driver, wait):
    """Navigates to the Exports dropdown and clicks 'Employee Locations'."""
    # Click 'Timesheet Summary' button
    timesheet_summary_button = wait.until(EC.element_to_be_clickable((By.ID, "pay-period-summary-react")))
    timesheet_summary_button.click()
    time.sleep(5)

    # Click the 'Exports' dropdown
    exports_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "exports_dropdown")))
    exports_dropdown.click()
    time.sleep(5)

    # Click 'Employee Locations' export option
    employee_locations_option = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Employee Locations')]")))
    employee_locations_option.click()
    time.sleep(5)
    print("'Employee Locations' export clicked.")


def get_most_recent_csv(download_dir, pattern="Employee-Locations-*.csv"):
    """
    Searches for CSV files in the download_dir that match the given pattern.
    Returns the path to the most recently modified file.
    """
    files = glob.glob(os.path.join(download_dir, pattern))
    if not files:
        raise Exception(f"No CSV files matching pattern '{pattern}' found in {download_dir}")
    most_recent_file = max(files, key=os.path.getmtime)
    return most_recent_file


def run_scraper():
    """Runs the full automation process: Login -> Navigate -> Export,
       then returns the path to the most recently downloaded CSV file."""
    driver = setup_driver()
    wait = WebDriverWait(driver, 10)

    try:
        login(driver, wait)
        navigate_to_exports(driver, wait)
    finally:
        driver.quit()
        print("Browser closed.")

    # Define the Downloads folder and CSV pattern
    download_dir = r'C:\Users\Work\Downloads'
    downloaded_csv = get_most_recent_csv(download_dir, pattern="Employee-Locations-*.csv")
    print(f"Downloaded CSV: {downloaded_csv}")
    return downloaded_csv


if __name__ == "__main__":
    csv_path = run_scraper()
    print(f"Most recent CSV downloaded: {csv_path}")
