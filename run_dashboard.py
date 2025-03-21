from webScraper import run_scraper
from traqsperaCsvToJson import main as convert_csv_to_json
from jsonToExcel import convert_json_to_excel
import dash_board


def main():
    # Step 1: Download the CSV and get its file path
    csv_path = run_scraper()
    print(f"[INFO] CSV downloaded to: {csv_path}")

    # Step 2: Convert the CSV to JSON using the downloaded file
    convert_csv_to_json(csv_path)

    # Step 3: Convert JSON data to Excel
    convert_json_to_excel(json_file="output.json", excel_file="output.xlsx")

    # Step 4: Launch the dashboard for shared viewing (server stays up)
    dash_board.run_dashboard()


if __name__ == "__main__":
    main()