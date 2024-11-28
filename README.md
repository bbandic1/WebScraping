# Web Scraping with BeautifulSoup

Python scripts are designed to scrape articles from portals like Klix.ba and Universitry PDF Archives. It uses the `requests` library to fetch web pages and `BeautifulSoup` from `bs4` to parse the HTML content. 

Adding to that, there is a Python script implemented with `Selenium` for Web scraping spacifically dynamic HTML code. Dynamic HTML code can't be scraped with `BeautifulSoup`.

A JSON Format Code is also included that is needed for the specific scraped data.

## Code Summary for Klix

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


