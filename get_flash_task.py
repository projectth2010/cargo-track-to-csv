import requests
import csv
from bs4 import BeautifulSoup

# Replace <<code>> with your specific code
url_template = "https://api.flashexpress.com/web/proof/view/{}"
tracking_codes = ["UTPN1WK45", "SAM1370T90"]  # Add more codes if needed

# Open the CSV file in write mode
with open("tracking_data.csv", mode="w", newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    # Write the header for the table, this should be updated based on the expected table structure
    writer.writerow(["Tracking Code", "Column1", "Column2", "Column3"])  # Update column names as necessary

    # Iterate over each tracking code
    for code in tracking_codes:
        url = url_template.format(code)
        try:
            # Send GET request to the URL
            response = requests.get(url)
            response.raise_for_status()  # Raise an error if the request fails

            # Parse the response content with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the table (you may need to adjust the selector based on the table structure)
            table = soup.find('table')

            if table:
                # Process the rows in the table
                for row in table.find_all('tr'):
                    columns = row.find_all('td')
                    # If there are columns in this row, write them to the CSV file
                    if columns:
                        row_data = [code] + [col.get_text(strip=True) for col in columns]
                        writer.writerow(row_data)
            # No table found: skip writing to CSV
        except requests.exceptions.RequestException as e:
            # Log error messages, but skip writing to CSV
            print(f"Error with tracking code {code}: {e}")

print("Data has been saved to tracking_data.csv (excluding entries with no table found)")
