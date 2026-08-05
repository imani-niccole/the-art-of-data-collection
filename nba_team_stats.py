"""
Data Collection | Final Project Milestone 1
Imani Candler | April 2, 2026
Using Selenium to pull stats information from NBA Team Stats  
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

options = Options()
options.add_argument("--start-maximized")

# for local chromedriver
#service = Service(executable_path = "/Users/inamicandler/Downloads/Art of Data Collection/chromedriver")
#driver = webdriver.Chrome(options=options, service=service)

driver = webdriver.Chrome(options=options)

# ===============================
# CONFIGURATION
# ===============================

URL = "https://www.nba.com/stats/teams/traditional?SeasonType=Regular+Season"
driver.get(URL)

# explicit wait
wait = WebDriverWait(driver, 10)

# ===============================
# DATA EXTRACTION
# ===============================
team_map = {
        'Atlanta Hawks': 'ATL', 'Boston Celtics': 'BOS', 'Brooklyn Nets': 'BKN',
        'Charlotte Hornets': 'CHA', 'Chicago Bulls': 'CHI', 'Cleveland Cavaliers': 'CLE',
        'Dallas Mavericks': 'DAL', 'Denver Nuggets': 'DEN', 'Detroit Pistons': 'DET',
        'Golden State Warriors': 'GSW', 'Houston Rockets': 'HOU', 'Indiana Pacers': 'IND',
        'LA Clippers': 'LAC', 'Los Angeles Lakers': 'LAL', 'Memphis Grizzlies': 'MEM',
        'Miami Heat': 'MIA', 'Milwaukee Bucks': 'MIL', 'Minnesota Timberwolves': 'MIN',
        'New Orleans Pelicans': 'NOP', 'New York Knicks': 'NYK', 'Oklahoma City Thunder': 'OKC',
        'Orlando Magic': 'ORL', 'Philadelphia 76ers': 'PHI', 'Phoenix Suns': 'PHX',
        'Portland Trail Blazers': 'POR', 'Sacramento Kings': 'SAC', 'San Antonio Spurs': 'SAS',
        'Toronto Raptors': 'TOR', 'Utah Jazz': 'UTA', 'Washington Wizards': 'WAS'
    }
def get_team_abbreviation(team_name):
    """Returns abbreviation or original name if not found in the map."""
    return team_map.get(team_name, team_name)     
try:
    
    #bypass cookies
    try:
        cookie_button = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
        cookie_button.click()
        print("Cookie banner clicked & closed")
    except:
        cookie_button_xpath = driver.find_element(By.XPATH, "//button[contains(text(), 'I Understand')]")
        cookie_button_xpath.click()
        print("Cookie banner not found or already closed")
    
    time.sleep(3) # pause after clicking cookies button
    
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table[class*='Crom_table']")))

    stats = []

    # finds all rows in table body, by css selector 
    items = driver.find_elements(By.CSS_SELECTOR, "table[class*='Crom_table'] tbody tr") 
    
    for item in items:
        try:
            # find all cells (td) in current row
            cells = item.find_elements(By.TAG_NAME, "td")
    
            # if it's not empty
            if len(cells) > 20: #ensure it's full data row
                team_full_name = cells[1].text.strip()
                stat = {
                    "Team Name": cells[1].text, # team name
                    "Team Abbr": get_team_abbreviation(team_full_name), #applied function here
                    "W": cells[3].text, # wins
                    "L": cells[4].text, # losses
                    "WIN%": cells[5].text, # win percentage
                    "REB": cells[19].text, # rebounds
                    "AST": cells[20].text, # assists
                }
                stats.append(stat)
        except Exception as item_error:
            print(f"Row extraction failed: {item_error}")
                     
    # convert to dataframe to view
    df = pd.DataFrame(stats)
    
    # 1. Define the mapping (usually best to keep this at the top of your script)
    team_map = {
        'Atlanta Hawks': 'ATL', 'Boston Celtics': 'BOS', 'Brooklyn Nets': 'BKN',
        'Charlotte Hornets': 'CHA', 'Chicago Bulls': 'CHI', 'Cleveland Cavaliers': 'CLE',
        'Dallas Mavericks': 'DAL', 'Denver Nuggets': 'DEN', 'Detroit Pistons': 'DET',
        'Golden State Warriors': 'GSW', 'Houston Rockets': 'HOU', 'Indiana Pacers': 'IND',
        'LA Clippers': 'LAC', 'Los Angeles Lakers': 'LAL', 'Memphis Grizzlies': 'MEM',
        'Miami Heat': 'MIA', 'Milwaukee Bucks': 'MIL', 'Minnesota Timberwolves': 'MIN',
        'New Orleans Pelicans': 'NOP', 'New York Knicks': 'NYK', 'Oklahoma City Thunder': 'OKC',
        'Orlando Magic': 'ORL', 'Philadelphia 76ers': 'PHI', 'Phoenix Suns': 'PHX',
        'Portland Trail Blazers': 'POR', 'Sacramento Kings': 'SAC', 'San Antonio Spurs': 'SAS',
        'Toronto Raptors': 'TOR', 'Utah Jazz': 'UTA', 'Washington Wizards': 'WAS'
    }

    # 2. Apply the mapping to a new column or overwrite the old one
    df['Team Abbr'] = df['Team Name'].map(team_map)
    
    if not df.empty:
        print("Yay! Successfully scraped the website. ")
        df.to_json("nba_team_stats.json", orient="records", indent=4)
        print("JSON file created: nba_team_stats.json")
    else:
        print("Could not successfully scrape website.")
    
except Exception as e:
    print("Error during extraction:", e)
    
driver.quit()