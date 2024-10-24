# Web Scraping with BeautifulSoup

This Python script is designed to scrape articles from portals like Klix.ba, specifically targeting the business category. It uses the `requests` library to fetch web pages and `BeautifulSoup` from `bs4` to parse the HTML content. 

## Code Summary

1. **Imports**: The script imports necessary libraries for web scraping, JSON handling, data manipulation, and HTML processing.

2. **Function: `get_article_links`**: 
   - This function takes a category URL as input and retrieves all relevant article links from that page.
   - It filters links that contain digits and hyphens, indicating they are likely articles rather than categories.

3. **Main Execution**:
   - The script sets the target category URL (`https://www.klix.ba/biznis`) and collects article links.
   - It iterates through each article link to extract various pieces of information such as:
     - Category (`kat`)
     - Publication date
     - Author(s)
     - Title and subtitle
     - Content body

4. **Data Storage**:
   - The extracted information is structured into a dictionary for each article, and a DataFrame is created using `pandas`.
   - Finally, the script saves the collected data in JSON and Excel formats.

## Usage

- Ensure that all required libraries (`requests`, `beautifulsoup4`, `pandas`, and `html`) are installed in your Python environment.
- Run the script in a Python environment to fetch and store article data.

## Notes

- The code is designed to handle potential missing data gracefully.
- Make sure to comply with the website's terms of service when scraping content.
