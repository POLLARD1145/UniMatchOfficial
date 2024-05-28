import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the URL (replace with the actual URL)
url = 'https://www.4icu.org/zm/'  # Replace with the actual URL

# Function to fetch the page content
def fetch_page_content(url):
    response = requests.get(url)
    response.raise_for_status()  # Check that the request was successful
    return response.text

# Function to parse the page content and extract universities and their rankings
def parse_universities(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', class_='table-hover')
    universities = []

    if table is None or table.tbody is None:
        print("No table found on the page.")
        return universities

    for row in table.tbody.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) < 3:
            continue  # Skip rows that don't have enough columns

        rank = cells[0].text.strip()
        name = cells[1].text.strip()
        town = cells[2].text.strip()
        universities.append((rank, name, town))

    return universities

# Function to save the data to a CSV file
def save_to_csv(data, filename):
    df = pd.DataFrame(data, columns=['Rank', 'University', 'Town'])
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

# Main function to orchestrate the scraping
def main():
    html_content = fetch_page_content(url)
    universities = parse_universities(html_content)
    save_to_csv(universities, 'zambia_universities.csv')

if __name__ == '__main__':
    main()
