import requests
from bs4 import BeautifulSoup
import re

# URL of the EduRank page for Zambian universities
url = 'https://edurank.org/geo/zm/'

def get_universities(limit=None):
    # Send a request to the URL
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all university blocks
    universities = soup.find_all('div', class_='block-cont pt-4 mb-4')
    
    university_list = []
    
    # Loop through the university blocks and extract information
    for uni in universities:
        # Extract university name and remove the rank prefix
        name_tag = uni.find('h2', class_='h4 font-weight-bold text-center')
        university_name = name_tag.get_text(strip=True) if name_tag else 'N/A'
        university_name = university_name.split('.', 1)[-1].strip()  # Remove everything before the first '.'
        
        # Extract rank in Zambia
        rank_tag = uni.find('span', class_='text-color-def')
        rank_in_country = rank_tag.get_text(strip=True) if rank_tag else 'N/A'
        

        # Extract world rank
        world_rank_tag = uni.find('div', class_='uni-card__rank').find_next_sibling('div')
        world_rank_text = world_rank_tag.get_text(strip=True) if world_rank_tag else 'N/A'

        # Use regex to extract the number
        world_rank_match = re.search(r'#(\d+)', world_rank_text)
        world_rank = world_rank_match.group(1) if world_rank_match else 'N/A'

        
        # Extract town
        town_tag = uni.find('a', href=lambda x: x and 'geo/' in x)
        town = town_tag.get_text(strip=True) if town_tag else 'N/A'
        
        # Add university details to the list
        university_list.append({
            'name': university_name,
            'rank': rank_in_country,
            'world_rank': world_rank,
            'town': town
        })
    
    # Return the specified number of universities or all if limit is None
    return university_list if limit is None else university_list[:limit]

# Example usage
if __name__ == "__main__":
    top_5_universities = get_universities(limit=5)
    all_universities = get_universities()

    print("Top 5 Universities:")
    print(top_5_universities)

    print("\nAll Universities:")
    print(all_universities)
