"""
Imani Candler
March 3, 2026

Selenium Data Extraction Pipeline Lab
Starter File

Instructions:
You will build a dynamic scraper using Selenium.

DEFAULT SITE:
Quotes to Scrape (JS Version)
https://quotes.toscrape.com/js/

OPTIONAL +10 EXTRA CREDIT:
1. Real Python Fake Jobs Board
   https://realpython.github.io/fake-jobs/
2. eBay search results (choose a keyword)
   https://www.ebay.com/

In Part 1:
- Set up Selenium
- Navigate to the site
- Identify elements
- Extract structured data into a list of dictionaries

In Part 2:
- Clean your data
- Convert to pandas DataFrame
- Perform basic analysis
- Export to CSV and JSON
"""

# ===============================
# IMPORTS
# ===============================

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from webdriver_manager.chrome import ChromeDriverManager ########## This depends on your setup ##########
import pandas as pd
import time

# ===============================
# DRIVER SETUP
# ===============================

options = Options()
options.add_argument("--start-maximized")

########## This depends on your setup ##########
#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
service = Service(executable_path = "/Users/inamicandler/Downloads/Art of Data Collection/chromedriver")
driver = webdriver.Chrome(options=options, service=service)
# ===============================
# CONFIGURATION
# ===============================

URL = "https://realpython.github.io/fake-jobs/"
# Change URL above if attempting extra credit site.

driver.get(URL)

# implement explicit wait, pauses execution until specific condition becomes true
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.ID, "ResultsContainer")))


# ===============================
# PART 1: DATA EXTRACTION
# ===============================

records = []
try:
    # INSERT CODE TO COLLECT DATA HERE
    # instead of the class name should i do the id container?
    #wait.until(EC.presence_of_element_located((By.CLASS_NAME, "columns is-multiline")))
    #items = driver.find_elements(By.CLASS_NAME, "columns is-multiline")

    # find where the job descriptions are held individually
    items = driver.find_elements(By.CLASS_NAME, "card-content")
    
    for item in items:
        try:
            # learned that instead of title is-5 or subtitle is-6 company as the company name, needs a single class name so title and company
            # if i wanted to use the full unique class name, i would use css_selector with "." replacing the spaces
            job_title = item.find_element(By.CLASS_NAME, "title").text
            company_name = item.find_element(By.CLASS_NAME, "company").text
            job_location = item.find_element(By.CLASS_NAME, "location").text
            job_posting = item.find_element(By.TAG_NAME, "time").text.strip() # don't forget parentheses with .strip()
            
            record = {
            # FILL IN FIELDS HERE
            "Job Title": job_title,
            "Company": company_name,
            "Location": job_location,
            "Date": job_posting
            }
            records.append(record)
        
        except Exception as item_error:
            print(f"Item extraction failed: {item_error}")

except Exception as e:
    print("Error during extraction:", e)

driver.quit()

# ===============================
# PRINT RAW OUTPUT
# ===============================
# extracts first 5 records
print("Extracted Records (first 5):")
for r in records[:5]:
    print(r)
    print() # a space to break up each dictionary

# ===============================
# PART 2 (TO COMPLETE LATER)
# ===============================

"""
TODO FOR PART 2:

1. Convert records to pandas DataFrame.
2. Clean/transform columns if needed.
3. Perform at least 2 summary analyses.
4. Export dataset to:
   - CSV file/ JSON file
5. Print confirmation message after saving files.
"""
