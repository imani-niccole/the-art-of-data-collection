"""
CIS 470 — HTML Scraping Lab (Part 1)
Planning & Page Analysis Starter File

Goal:
- Explore the Books to Scrape website
- Identify URL patterns for pagination
- Retrieve at least ONE page successfully
- Inspect the raw HTML (no parsing required yet)

Website:
https://books.toscrape.com/index.html
"""

import requests

""" QUESTION: Noticed that the BASE_URL and first_page url have the same 500 characters outputted.
    For this assignment, I used the GET request for first_page url, I believe, so if I need to fetch 
    multiple pages, I can. Why is this the case? 
"""

BASE_URL = "https://books.toscrape.com/"

def fetch_page(url):
    """
    TODO: Send a GET request to the given URL and return the response text.
    """
    
    # instead of BASE_URL, goes to the specific address, beyond page 1
    response = requests.get(url)
    return response.text


def main():
    # TODO (Part 1):
    # 1. Identify the URL for the first page you want to scrape
    # 2. Call fetch_page on that URL
    # 3. Print the first 500 characters of the HTML to confirm it worked


    # page for the first page i want to scrape
    # catalogue/page-1.html is the pattern which will be used for looping
    first_page = "https://books.toscrape.com/catalogue/page-1.html"
    
    # have to call fetch_page on first page
    content = fetch_page(first_page)
     
    print ("---- First 500 characters of HTML ----")
    print (content[:500]) # print the first 500 characters, saw from lecture 9


""" at first program wasn't running without these two lines. 
    gemini told me that this tells me that this tells the
    script to run the main function when executing the file.
    also noticed this in lecture 5 notebook.
"""
if __name__ == "__main__":
    main()
