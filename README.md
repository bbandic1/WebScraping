# **Introduction**

Data scraping is a technique for automatically collecting information from websites or documents. In this document, we will focus on web scraping (extracting data from websites) and PDF scraping (extracting text from PDF documents) using Google Colab.

For web scraping, we will use:

*   BeautifulSoup – for parsing static HTML.
*   Selenium – for interacting with dynamic web pages.

For PDF scraping, we will use:

*   pdfplumber – specialized for precise extraction of text and tables from PDFs, particularly scanned and complex documents.

Other libraries that may be useful:

*   PyMuPDF (fitz) – faster than pdfplumber, good for extracting structured text (two-column text).


# **Web Portals**

## BeautifulSoup

BeautifulSoup is a Python library used for extracting data from HTML and XML files. It is particularly useful for parsing static pages, where the HTML structure does not change dynamically. Unlike Selenium, which is used for interacting with content rendered through JavaScript, BeautifulSoup focuses on efficiently processing HTML that is already available.

### Fetching and Parsing HTML Content

To scrape a website, we first need to retrieve its HTML content. This is achieved using the requests library, which allows us to send HTTP requests and receive responses. Once we have the HTML, we can parse it using BeautifulSoup.

The steps are as follows:

1.   Send an HTTP request using requests.get() – This method sends a GET request to the URL, retrieving the HTML content of the page.
2.   Parse the HTML response using BeautifulSoup – After receiving the HTML, we pass it to BeautifulSoup to convert it into a structured format that can be easily traversed and queried.
3.   Choose the appropriate parser (e.g., html.parser, lxml, etc.) – The parser determines how the HTML is processed. html.parser is the default, but lxml can be used for faster parsing.




```python
from bs4 import BeautifulSoup
import requests

# Step 1: Send HTTP request
url = "https://example.com"
response = requests.get(url)

# Step 2: Parse HTML response
soup = BeautifulSoup(response.text, 'html.parser')

# Now you can start selecting elements, for example:
title = soup.title.text
print(title)
```

### Extracting Specific Elements

Once the HTML is parsed, we can extract specific elements using methods like find(), find_all(), and CSS selectors. These methods allow us to select elements based on their tags, attributes, or CSS selectors.

Methods for extracting elements:


*   find(): Returns the first occurrence of an element.
*   find_all(): Returns all matching elements as a list.
*   CSS Selectors (select()): Allows for more complex selection of elements using CSS-like syntax.


```python
# Extracting all links from the page
links = soup.find_all("a", href=True)
for link in links:
    print(link["href"])
```

### Handling Pagination

Some websites distribute content across multiple pages. To scrape all pages, we need to navigate through them dynamically until we reach the last page.

Here's an example approach:


```python
page_num = 1

while True:
    # Construct the URL for the current page
    page_url = f"https://example.com/page/{page_num}/"
    response = requests.get(page_url)

    # Check if the page exists by verifying the status code
    if response.status_code != 200:
        break  # Stops if the page does not exist

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, "html.parser")

    # Process the page content here (e.g., extract data)

    page_num += 1  # Move to the next page
```

### Debugging

Scraping often requires troubleshooting due to dynamic elements, encoding issues, or missing data. Here are some key strategies for debugging:

*   **Inspecting the HTML Structure:** Use Developer Tools (F12 in Chrome, right-click > Inspect) to locate the elements before scraping. This allows you to view the structure of the HTML and ensure you're targeting the right elements.
*   **Checking for Missing Elements:** If find() returns None, it means the element was not found. Double-check if the element exists on the page and if you're using the correct tag, class, or attribute in your search.
*   **Handling Encoding Issues:** Some pages may require decoding, especially if they contain special characters or are not UTF-8 encoded. Use response.content.decode("utf-8") if you encounter issues with non-standard encodings.



Example for debugging:


```python
print(soup.prettify())  # Prints the structured HTML for inspection
```

## Selenium

Selenium is a powerful tool for web scraping, particularly useful when dealing with dynamic content that requires JavaScript execution. Unlike BeautifulSoup, which only parses static HTML, Selenium allows direct interaction with web pages, including clicking buttons, scrolling, and filling out forms.

### Selection of Headless Browser

When using Selenium, we need a browser for web navigation. There are two ways to run a headless browser:

1.  Using Google Colab or Jupyter Notebook

  *   Colab provides a pre-configured environment where we can use a headless browser without manual installation.
  *   It simplifies working with Selenium for beginners without requiring browser setup on their system.
  *   Required dependencies can be installed directly in the notebook using:







```python
!apt-get update
!apt-get install -y chromium-chromedriver
```

2. Installing the Browser Locally (PyCharm, VS Code, etc.)

    *   Install the appropriate WebDriver in a version that matches your browser version (e.g., ChromeDriver for Chrome).
    *   This method requires manually configuring the WebDriver and specifying the exact path.
    *   A significantly longer setup process compared to direct usage within Colab.

### Configuring a Headless Browser

The following snippet shows how to set up Selenium if you are using Chromium:


```python
# Needed importi
pip install selenium

!apt-get install chromium-browser
!apt-get install chromium-chromedriver

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
```

Use this WebDriver definition:


```python
def web_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--verbose")
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("--window-size=1920, 1200")
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    return driver

# Create the WebDriver
driver = web_driver()

# Static starting URL
static_url = "https://example.com"
driver.get(static_url)

# Page load verification
print("Učitana stranica:", driver.title)
```

### Selenium Functionalities

#### 1. Finding and Interacting with Elements

We use find_element or find_elements to locate elements:


```python
button = driver.find_element(By.ID, "submit-button")  # Find by ID
button.click()  # Click on button
```

Locator Strategies:

*   By.ID - Find by unique ID.
*   By.CLASS_NAME - Find elements by class.
*   By.XPATH - Use XPath expression for complex queries.
*   By.CSS_SELECTOR - Select elements using a CSS selector.



#### 2. Handling Dynamic Content

Web pages often load elements dynamically. Selenium allows waiting for an element using WebDriverWait:


```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "content")))
```

#### 3. Scrolling and Pagination

Some pages load content only when scrolling to the bottom:


```python
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
```

For pagination, we can find and click the "Next" button:


```python
next_button = driver.find_element(By.LINK_TEXT, "Next")
next_button.click()
```

#### 4. Handling Popups, Alerts, and iFrames

If a popup window appears:


```python
alert = driver.switch_to.alert
alert.accept()  # Click on 'OK'
```

For working with iFrames:


```python
driver.switch_to.frame("iframe_id")
```

# **PDF**

PDFs are a versatile format for storing and sharing documents, but extracting text from them can present unique challenges. Unlike structured HTML pages, PDFs do not always store text in a logical reading order, and their layout can vary significantly.

Challenges of Extracting Text from PDFs


1.   Variability in Text Structure

  *   Some PDFs store text in a simple, linear format, making extraction easier.
  *   Others may store text in a way that does not reflect the visual structure, requiring additional processing.

2.   Multi-Column Layout

  *   Some PDFs format text into two or more columns. A naive extraction method might read text across columns instead of processing one column at a time, resulting in messy content.
  *   Solving this issue may require specialized tools or custom logic to correctly recognize and separate columns.

3.   Text Content

  *   Some PDFs contain actual text that can be programmatically extracted.
  *   Others are image-based (scanned documents), requiring optical character recognition (OCR) tools such as Tesseract to convert images into text.


Each of these tools has its advantages, and the choice depends on the complexity of the PDF being processed. In some cases, it may be necessary to combine multiple approaches to achieve optimal results.

By understanding these challenges and using the right tools, it is possible to efficiently extract useful data from PDFs, even when dealing with complex formats.

## pdfplumber

Here, we will explore pdfplumber, a powerful Python library for extracting text and tables from PDFs.

### Setting up pdfplumber

To start using pdfplumber, install it if you haven't already:


```python
pip install pdfplumber
```

Then, import the necessary libraries:


```python
import pdfplumber
```

### Opening and Extracting Text from a PDF

To open a PDF and extract text from each page:


```python
with pdfplumber.open("example.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

This method extracts text from each page, but some PDFs may require additional processing due to complex structures.

### Extracting Text from Specific Pages

If you need data from only a specific page, you can access it using its index (starting from 0):


```python
with pdfplumber.open("example.pdf") as pdf:
    first_page = pdf.pages[0]
    text = first_page.extract_text()
    print(text)
```

### Extracting Tables

Many PDFs contain tables, and pdfplumber allows direct extraction of data from them:


```python
with pdfplumber.open("example.pdf") as pdf:
    first_page = pdf.pages[0]
    tables = first_page.extract_table()
    print(tables)
```

This function returns a list of rows, where each row is a list of cell values.

### Handling Non-Standard Text Layouts

Some PDFs use embedded fonts, images, or unusual text layouts, which may require additional data cleaning:


```python
with pdfplumber.open("example.pdf") as pdf:
    for page in pdf.pages:
        words = page.extract_words()
        print(words)
```

The extract_words() function can help when text extraction is inconsistent.

## PyMuPDF

PyMuPDF (fitz) is a powerful library for working with PDFs. It provides advanced functionalities for handling complex layouts, such as multi-column text structures. Therefore, it is an excellent alternative to pdfplumber when dealing with PDFs that are not linearly structured.

### Setting up PyMuPDF


```python
import fitz  # PyMuPDF
```

### Extracting Text from a PDF

PyMuPDF allows efficient extraction of text from each page of a PDF document:


```python
doc = fitz.open("example.pdf")
for page in doc:
    text = page.get_text()
    print(text)
```

### Extracting Metadata

Metadata can provide useful information about the PDF document:


```python
doc = fitz.open("example.pdf")
metadata = doc.metadata
print(metadata)
```

### Handling Multi-Column Layouts

One of the advantages of PyMuPDF is the ability to extract text while preserving the column structure. Instead of reading the text linearly, it can be extracted block by block.


```python
doc = fitz.open("example.pdf")
for page in doc:
    blocks = page.get_text("blocks")
    for block in blocks:
        print(block)
```

This approach ensures that text from separate columns does not mix, maintaining the logical flow of the document.

### Extracting Text by Regions

Sometimes it is necessary to extract text from specific areas of a page.


```python
doc = fitz.open("example.pdf")
page = doc[0]  # First page
rect = fitz.Rect(50, 50, 400, 400)  # Defines a rectangular region
text = page.get_text("text", clip=rect)
print(text)
```

By specifying coordinates, we can target specific parts of the PDF for more precise data extraction.

## Processing Extracted PDF Text

Once text has been successfully extracted from a PDF, it often requires additional processing to make it usable for datasets. The extracted text may contain unwanted elements such as headers, footers, page numbers, references, or formatting inconsistencies. This section discusses common issues and provides strategies for cleaning and structuring the text.

### Common Issues in Extracted Text

#### 1. Unwanted Metadata

The extracted text might contain metadata such as journal names, issue numbers, or document titles, which are often unnecessary for analysis. These elements should be removed to retain only the relevant content.

#### 2. Headers and Footers

Headers often contain journal names, article titles, or section labels, while footers may include references, issue numbers, or horizontal dividers. These elements can be removed using pattern recognition techniques.

#### 3. Page Numbers

Page numbers often appear at the top or bottom of the extracted text. If they consistently appear as standalone numbers on a line, they can be removed using regular expression-based filtering.

#### 4. References and Citations

References in academic texts follow various formats, including:

*   Numerical references: [2] or 2. at the beginning or end of sentences.
*   Author and year references: (Kazaz 2016: 7), (Kelly et al., 2004), (Hastings & Jacob, 2016).
*   Combined references: (..., number) (...:number).




Regular expression-based filtering can be used to remove these references while ensuring that relevant numerical values like years remain intact.

#### 5. Section Titles and Subtitles

Section titles (e.g., 1.1. Introduction, III. Methods, Conclusion) often appear as standalone lines and can be recognized through structured numbering or common keywords (Introduction, Summary, Conclusion). These elements can be removed or reformatted as needed.

#### 6. Content in Foreign Languages

Some extracted texts may include content in multiple languages. If the article contains sections written in a language other than the target language (e.g., English summaries in a document mostly written in BHS), these sections should be identified and removed.

#### 7. Formatting Issues

Newlines (\n) can cause unnecessary breaks in the extracted text, fragmenting sentences. The text should be reformatted to ensure a smooth flow without artificial line breaks.

### Processing Steps


1. Remove metadata (e.g., journal names, issue numbers).

2. Clean headers and footers (using pattern recognition).

3. Eliminate page numbers (if they appear as standalone numbers).

4. Filter references and citations (using regular expressions while preserving relevant data).

5. Identify and remove section titles (standalone numbered titles or common keywords).

6. Remove content in foreign languages (based on recognized language patterns).

7. Reformat the text to ensure a continuous flow without unnecessary line breaks.



# **Example of The Required Data Structure for a Specific Project**

When processing data, it is crucial to ensure that the data follows a structured and consistent format. This enables easier analysis, storage, and retrieval. Below is the required format to be followed when organizing the extracted text.

## Formatting Rules

1. Each article must begin with <***> to separate instances.

2. Metadata must follow a specific naming convention and be listed in the exact order. Do not change the names.

  Order:

    *   NEWSPAPER:
    *   DATE:
    *   CATEGORY:
    *   HEADING:
    *   TITLE:
    *   SUBTITLE:
    *   PAGE:
    *   AUTHOR(S):

3. If any metadata is missing, use N/A instead of leaving it empty.

4. A new line (\n) must be added after the metadata section before the article text begins.

5. Follow the correctly formatted text.

6. Another new line (\n) must be added after the article text before the next <***> separator.

7. Preserve the spaces and formatting exactly as extracted, ensuring readability and consistency.

It is recommended to save your collected data as a .json file and then generate the .txt document from the .json file. This approach ensures better data structure, easier manipulation, and future-proofing for any further analysis or processing.

# **Important Note**

When scraping, each process is unique. Even if you have prior experience, every website, portal, or document has a different structure. HTML can be static or dynamic, and accessing specific data may require different steps, such as navigating through multiple links or interacting with calendars. Therefore, scraping is not a simple copy & paste process; you must analyze the structure of each page and create code tailored to it. This guide is generalized to help you develop a flexible approach to scraping, rather than relying on static examples.

## Limitations and Best Practices in Google Colab

Google Colab provides a free Python environment, but it comes with limitations that must be considered when performing web scraping or working with large datasets.

### 1. Execution Time Limitations

* The free version of Colab has a maximum execution time of 12 hours.

* Any process that exceeds this time will be automatically terminated.

* The actual duration depends on resource usage. If a process uses a large amount of CPU or RAM, the session may end earlier (e.g., after 10 hours instead of 12).

* You should monitor the session duration by checking the RAM & Disk section in Colab, which shows the estimated remaining time.

* Even if Colab estimates 60+ hours, free sessions will always end after 12 hours, regardless of the displayed time.

### 2. Monitoring Resource Usage

* You should monitor RAM and CPU usage to ensure the session operates efficiently.

* Avoid leaving the runtime unattended for long periods. Check periodically to ensure the scripts are progressing correctly.

* If possible, break long-running scraping tasks into smaller batches to avoid sudden interruptions.

### 3. Managing Connection and Request Limitations

Web scraping involves sending repeated requests to websites, which can sometimes cause connection errors or timeouts. Some websites limit the number of requests and temporarily block access if too many requests are sent within a short period.


To prevent this:
  *  Implement delays between requests using time.sleep().
  * Use try-except blocks to catch errors and retry after a delay.
  * Randomize intervals between requests to avoid sending multiple requests at fixed intervals, which may be flagged as automated traffic.

### 4. Best Practices

* Do not leave scripts running unattended for long hours. Check periodically to ensure no errors have occurred.
* Create logs and check them frequently to see if the script is functioning as expected.
* Handle unexpected interruptions in a way that allows for retries, and save intermediate results whenever possible.
