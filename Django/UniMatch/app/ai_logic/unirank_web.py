import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the URL to fetch the current ranking list
url = 'https://www.4icu.org/zm/'  

# define file path to save the list when the url is not responding
unirank_file = "Django/UniMatch/app/ai_logic/csvdocs/unirank_list.csv"

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
    #save_to_csv(universities,unirank_file)
    return universities

# Function to save the data to a CSV file
def save_to_csv(data, filename):
    df = pd.DataFrame(data, columns=['Rank', 'University', 'Town'])
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

#get the ranking list upto a certain number
def get_rank_list(number_of_universities):
    html_content = fetch_page_content(url)
    universities_info = parse_universities(html_content)
    #get the specified number
    def slice_dict(d, n):
        return dict(list(d.items())[:n])

    universities = slice_dict(universities_info, number_of_universities)
    
    return universities


#get the list of all the universities
def get_rank_list_all():
    html_content = fetch_page_content(url)
    universities = parse_universities(html_content)
    return universities
