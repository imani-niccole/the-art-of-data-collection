"""
Imani Candler | 2.25.2026

CIS 470 — HW 5 Mini Web Scraper
Create own mini scraper using requests
Scraped Wikipedia for list of teallest buildings by country

NOTE: Make sure terminal window is maximized, 
otherwise building name will not be displayed (look like ellipses)
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_page():
    url = "https://en.wikipedia.org/wiki/List_of_tallest_buildings_by_country"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status() # check status code to see if page exists
        return response.text
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return None
    
    
# parsing function
def tall_buildings(html):
    if not html:
        return None
    
    soup = BeautifulSoup(html, "html.parser")
    
# find desired table
    tb = soup.find("table", {"class": "wikitable"}) # considered the base class "wikitable," learned that this is the easiest way instead of whole class name
    data_list = []
    
# error prevention for missing table
    if not tb:
        print("Table could not be found")
        return None
    
    # create for loop to find the building information (modeled after previous hw)
    for row in tb.find_all("tr")[1:]:
        cells = row.find_all(["td", "th"])
        
        # the number of columns exceeds 4 (only wanting the first few columns)
        if len(cells) >= 4:
            
        # for each column we just want the listed text (.get_text(strip=True))
        # country name found in first column of table
            country = cells[0].get_text(strip=True)
        
        # building name found in third column
            building = cells[2].get_text(strip=True)
        
        # height found in fourth column of table
            height = cells[3].get_text(strip=True)
        
        building_data = {
            "Country": country,
            "Building Name": building,
            "Height": height   
        }
        data_list.append(building_data) # adds building info into a list of dictionaries


    return pd.DataFrame(data_list)

if __name__ == "__main__":
    """
    set_option lines are taken from gemini. my original output
    printed the columns and rows, but did "..." ellipses for long names/info
    i want to print the row regardless of how long it is
    """
    html_stuff = fetch_page() # call function for .get
    df = tall_buildings(html_stuff) # pass html into parsing tall_buildings function
    
    if df is not None:
        pd.set_option('display.max_rows', None)
        pd.set_option("display.width", 1000)
        print(df.head(101)) # controls the row count (will print first 100 rows)
    else:
        print("no data")