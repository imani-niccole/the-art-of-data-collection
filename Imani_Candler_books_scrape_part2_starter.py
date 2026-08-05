"""
Imani Candler | 2.12.2026

CIS 470 — HTML Scraping Lab (Part 2)
Implementation with Requests & Beautiful Soup

Goal:
- Scrape AT LEAST 5 pages from Books to Scrape
- Extract title, rating, price, and stock status
- Store results as a list of dictionaries
- Print results in a table-style format

Website:
https://books.toscrape.com/index.html
"""

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"
START_PAGE = "index.html"
NUM_PAGES = 10

def fetch_page(page_number):
    """
    Send a GET request to the given URL and return the response text.
    """
    # Taken from Part 1 submission and lecture 9 slides
    url = f"{BASE_URL}catalogue/category/books_1/page-{page_number}.html"
    
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url,headers=headers, timeout=5)
        response.raise_for_status() # check status code to see if page exists
        return response.text
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return None
        
def parse_books(html):
    """
    Given HTML for a page, return a list of dictionaries.
    Each dictionary represents one book.
    """
     # TODO (Part 2):
    # 1. Locate all book containers on the page
    # 2. For each book:
    #    - Extract title
    #    - Extract rating
    #    - Extract price
    #    - Determine in-stock status
    # 3. Use None if any field is missing
    # 4. Append each book dictionary to books

    soup = BeautifulSoup(html, "html.parser")
    book_list = [] # empty list to store the scraped book data
    book_container = soup.find_all("article", class_= "product_pod") # book info is held within the product pod
    
    # watched youtube video to help format rating and availability status 
    # googled, it was suggested to turn for loop to handle just tags, THEN handle Nones
    #for book in soup.find_all("article", class_="product_pod"):
    for item in book_container:
        title_tag = item.h3.a if item.h3 else None
        price_tag = item.find("p", class_= "price_color")
        rating_tag = item.find("p", class_= "star-rating")
        status_tag = item.find("p", class_= "instock availability")# without .strip() formatting is not cleanwhich literally says "in stock", should i check this text instead?
       
       # handling missing values, assign None
        full_title = title_tag["title"] if title_tag else None
        price = price_tag.text.strip() if price_tag else None
        
        # needed help! w/o if statement, final formatted shifted with long book titles
        # adding if statement makes everything format nicely (somehow formatting was still wonky)
        if full_title:
            words = full_title.split() # splits whitespace
            if len(words) > 6: # i wanted book titles longer than 6 words to be split
                title = " ".join(words[:5]) + "..." # add elipsis to the end of the book title
            else:
                title = full_title
        else:
            title = None
       
       # different handling since it's a class name
       # we need the second element of the string, so used ["class"][1]
        rating = rating_tag["class"][1] if (rating_tag and len(rating_tag["class"]) > 1) else None
       
        status = status_tag.text.strip() if status_tag else None
       
    
        book_data = {
            "Title": title,
            "Rating": rating,
            "Price": price,
            "Status": status
        }
        book_list.append(book_data) # add dictionary key and values into list
    return book_list # return the list of scraped book data


def print_table(books):
    """
    TODO: Print book data in a simple table format.
    """

    # Insert Code Here
    # found formatting on geeksforgeeks
    header_format = "{:<50} {:<10} {:<10} {:<20}"
    
    # print names of the columns
    print (header_format.format("TITLE", "RATING", "PRICE", "STATUS"))
    print ("-" * 90) # border that separates header from data
    
    for book in books:
        # pull values from each dictionary (list of dictionaries!)
        title = (book["Title"][:47] + "..") if len(book["Title"]) > 47 else book["Title"]
        rating = book["Rating"]
        price = book["Price"]
        status = book["Status"]
        
        print (header_format.format(title, rating, price, status)) # print data

def main():
    all_books = []

    # TODO (Part 2):
    # Loop over page numbers 1 through NUM_PAGES
    # Construct each page URL
    # Fetch HTML
    # Parse books
    # Extend all_books

    # Insert Code Here

    # Loop over page numbers 1 through NUM_PAGES
    print()
    print("Hello, let's scrape!")
    print (f"Starting scraping process for {NUM_PAGES} pages!") # correctly prints that I want to scrape 10 pages!
    
    for page_num in range(1, NUM_PAGES + 1):
        #print("hello!") will print 10 times loll
        # FETCH
        html = fetch_page(page_num)
        
        # PARSE BOOKS
        page_books = parse_books(html)
        
        # EXTEND all_books
        all_books.extend(page_books)
            
    print(f"Total books collected: {len(all_books)}") # should collect 200 books!
    print()
    print_table(all_books) # passes the list of dictionaries from def(print_table)


if __name__ == "__main__":
    main()
