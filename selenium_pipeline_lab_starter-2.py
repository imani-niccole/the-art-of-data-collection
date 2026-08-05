"""
Imani Candler
March 3, 2026
Part 2 submitted March 11, 2026
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
# extracts all data in records (changed from part 1)
print("Extracted Records")
for r in records[:5]:
    print(r)
    print() # a space to break up each dictionary

# ===============================
# PART 2 
# ===============================
"""
created if/else statement since i need confirmation 
message for file exportation
"""

# using DataFrame, convert records
if records: # if the records exists, do the following:
    df = pd.DataFrame(records)
    df.head()
    df.info() # inspect dataset
    
    print("----- DATA ANALYSIS + EXPORT -----\n")
# exploratory analysis
    print("----- Missing Values -----\n")
    print(f"There are: {df.isna().sum()} missing values") # handling missing values

    print("\n----- Summary Analysis -----\n")
    
    print("\n----- Job Titles -----\n")
    print(df["Job Title"].value_counts()) # count total number of jobs listed
    
    print("\n----- Jobs by Location -----\n")
    location_counts = df.groupby("Location").size().reset_index(name="Job Count") # want to group locations and count how many jobs per location
    print(location_counts)
    
    
    file = "SeleniumLab4_Part2.csv"
    df.to_csv(file, index=False)
    print(f"\nFile exported to {file} successfully!")
    
else:
    print("Records was not found")
