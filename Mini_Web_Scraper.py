"""
Imani Candler | 2.11.2026
Homework 4 - Mini Web Scraper
Objective: Create a mini web scraper that collects
strucutured country-level data from a static website using Python
"""

from bs4 import BeautifulSoup
import requests

# make http request to retrieve webpage
webpage = requests.get("https://www.scrapethissite.com/pages/simple/")
if webpage.status_code == 200:
    print("Response code is 200.") # confirm request was successful
    print()
# parse through the html response
soup = BeautifulSoup(webpage.text, "html.parser")
all_countries = soup.find_all("div", class_= "country")
# identify the repeated container that represents single country
countries = {} # empty dictionary
# col-md-4 country
# create for loop to find all country info for every country
for country in all_countries[:25]:
    name = country.find("h3").get_text(strip=True) # gets country name
    capital = country.find("span", class_= "country-capital") # gets country capital
    population = country.find("span", class_= "country-population") # gets country population
    area = country.find("span", class_= "country-area")

# extract country information, if country information is missing, return None so code won't crash
    countries[name] = {
    "Capital": capital.get_text(strip=True) if capital else None,
    "Population": population.get_text(strip=True) if population else None,
    "Area": area.get_text(strip=True) if area else None
}

# had to look up formatting. i wanted to output country info so that it was easy to read 
for name, information in countries.items():
    print(f"Country: {name}")
    print(f"Capital: {information["Capital"]}")
    print(f"Population: {information["Population"]}")
    print(f"Area: {information["Area"]}")
    print()
