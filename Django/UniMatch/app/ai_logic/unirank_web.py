import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Define the URL to fetch the current ranking list
url = 'https://www.4icu.org/zm/'

# Define the relative file path to save the list when the URL is not responding
unirank_file = os.path.join('app', 'ai_logic', 'csvdocs', 'unirank_list.csv')

# Function to fetch the page content
def fetch_page_content(url):
    response = requests.get(url)
    response.raise_for_status()  # Check that the request was successful
    return response.text

# Function to parse the page content and extract universities and their rankings
def parse_universities(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', class_='table-hover')
    universities = {"rank": [], "name": [], "town": []}

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

        universities["rank"].append(rank)
        universities["name"].append(name)
        universities["town"].append(town)

    return universities

# Function to save the data to a CSV file
def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

# Function to load university data from a CSV file
def load_from_csv(filename, number_of_universities):
    try:
        df = pd.read_csv(filename)
        return df.head(number_of_universities).to_dict(orient='list')
    except FileNotFoundError:
        print("No local file found to load universities.")
        return {"rank": [], "name": [], "town": []}

# Get the ranking list up to a certain number
def get_rank_list(number_of_universities):
    try:
        html_content = fetch_page_content(url)
        universities_info = parse_universities(html_content)
        save_to_csv(universities_info, unirank_file)  # Save to CSV for future offline access
        # Limit to the specified number of universities
        limited_universities = {k: v[:number_of_universities] for k, v in universities_info.items()}
        return limited_universities
    except requests.RequestException as e:
        print(f"Error fetching data from URL: {e}")
        # Attempt to load from CSV if the URL fetch fails
        return load_from_csv(unirank_file, number_of_universities)

# Get the list of all universities
def get_rank_list_all():
    try:
        html_content = fetch_page_content(url)
        universities = parse_universities(html_content)
        save_to_csv(universities, unirank_file)  # Save to CSV for offline access
        return universities
    except requests.RequestException as e:
        print(f"Error fetching data from URL: {e}")
        return load_from_csv(unirank_file, float('inf'))  # Load all universities from CSV

# Example usage:
if __name__ == "__main__":
    top_5_universities = get_rank_list(5)
    print("Top 5 Universities:")
    print(top_5_universities)

    all_universities = get_rank_list_all()
    print("All Universities:")
    print(all_universities)
