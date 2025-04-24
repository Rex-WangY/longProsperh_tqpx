# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# import re
# import json
# import pymysql
# from lxml import etree

# chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--ignore-certificate-errors')
# chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument('--log-level=3')   # Suppress warnings

# # url = 'https://finance.yahoo.com/quote/CNH=X/history/'

# # """ Use Selenium to fetch page source """
# # chrome_options = Options()
# # # chrome_options.add_argument("--headless")
# # driver = webdriver.Chrome(options=chrome_options)

# # try:
# #     driver.get(url)
# #     html = driver.page_source
# #     print(html)
# # finally:
# #     driver.quit()


# def get_page_source_selenium(url,chrome_options):
#     """ Use Selenium to fetch page source """
#     # chrome_options.add_argument("--headless")
#     driver = webdriver.Chrome(options=chrome_options)

#     try:
#         driver.get(url)
#         html = driver.page_source
#                 # Extract the HTML source
#         html = etree.HTML(html)
#     finally:
#         driver.quit()
#     return html

# def pattern_data(soup, regex_patterns):
#     rp = regex_patterns

#     pattern_usdcnh = rp.get("pattern_usdcnh")
#     pattern_symbol = rp.get("pattern_symbol")
#     pattern_time = rp.get("pattern_time")
#     pattern_price = rp.get("pattern_price")
#     pattern_change = rp.get("pattern_change")
#     pattern_change_percent = rp.get("pattern_change_percent")

#     usdcnh_match = re.search(pattern_usdcnh, soup, re.DOTALL)
#     if usdcnh_match:
#         usdcnh_text = usdcnh_match.group(0)

#         symbol_match = re.search(pattern_symbol, usdcnh_text).group(0).replace("\\", "")
#         print(symbol_match)

#         time_match = re.search(pattern_time, usdcnh_text).group(0).replace("\\", "")
#         json_str = "{" + time_match + "}"
#         data = json.loads(json_str)
#         raw_time = data['regularMarketTime']['raw']
#         fmt_time = data['regularMarketTime']['fmt']

#         price_match = re.search(pattern_price, usdcnh_text).group(0).replace("\\", "")
#         data = json.loads("{" + price_match + "}")
#         raw_price = data['regularMarketPrice']['raw']
#         fmt_price = data['regularMarketPrice']['fmt']

#         change_match = re.search(pattern_change, usdcnh_text).group(0).replace("\\", "")
#         data = json.loads("{" + change_match + "}")
#         raw_change = data['regularMarketChange']['raw']
#         fmt_change = data['regularMarketChange']['fmt']

#         change_percent_match = re.search(pattern_change_percent, usdcnh_text).group(0).replace("\\", "")
#         data = json.loads("{" + change_percent_match + "}")
#         raw_change_percent = data['regularMarketChangePercent']['raw']
#         fmt_change_percent = data['regularMarketChangePercent']['fmt'].replace('%', '')

#         return {
#             "symbol": "CNH=X",
#             "rawMarketTime": raw_time,
#             "fmtMarketTime": fmt_time,
#             "rawMarketPrice": float(raw_price),
#             "fmtMarketPrice": float(fmt_price),
#             "rawMarketChange": float(raw_change),
#             "fmtMarketChange": float(fmt_change),
#             "rawMarketChangePercent": float(raw_change_percent),
#             "fmtMarketChangePercent": float(fmt_change_percent)
#         }
#     else:
#         print("USDCNH JSON block not found.")
#         return None

# def save_to_mysql(data_dict, table_name="market_data"):
#     conn = pymysql

# if __name__=="__main__":
#     # Define the URL and regex patterns
#     url = 'https://finance.yahoo.com/quote/CNH=X/history/'
#     regex_patterns = {
#     "pattern_usdcnh": "<script\\s+data-sveltekit-fetched=\"\"\\s+data-ttl=\"1\"[\\s\\S]*?<\\/script>", 
#     "pattern_symbol": "\\\\\"symbol\\\\\":\\\\\".*?\\\\\"",
#     "pattern_time" : "\\\\\"regularMarketTime\\\\\":\\{.*?\\}",
#     "pattern_price": "\\\\\"regularMarketPrice\\\\\":\\{.*?\\}",
#     "pattern_change": "\\\\\"regularMarketChange\\\\\":\\{.*?\\}",
#     "pattern_change_percent": "\\\\\"regularMarketChangePercent\\\\\":\\{.*?\\}"
#     }
#     # Get the page source using Selenium
#     page_source = get_page_source_selenium(url,chrome_options)
#     regularMarketPrice = '//*[@id="nimbus-app"]/section/section/section/article/section[1]/div[2]/div[1]/section/div/section/div[1]/div[1]/span/text()'
#     regularMarketChange = '//*[@id="nimbus-app"]/section/section/section/article/section[1]/div[2]/div[1]/section/div/section/div[1]/div[2]/span/text()'
#     regularMarketChangePercent = '//*[@id="nimbus-app"]/section/section/section/article/section[1]/div[2]/div[1]/section/div/section/div[3]//span/text()'
#     marketPrice = page_source.xpath(regularMarketPrice)
#     marketChange = page_source.xpath(regularMarketChange)
#     marketChangePercent = page_source.xpath(regularMarketChangePercent)



#     # # Extract data using regex patterns
#     # data_dict = pattern_data(page_source, regex_patterns)
#     # print(data_dict)
#     # # Save to MySQL database
#     # # if data_dict:
#     # #     save_to_mysql(data_dict)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re # Keep re just in case, though not strictly needed for the main XPath part
import json # Keep json just in case
import pymysql
from lxml import etree
import time # Import time for potential waits

# --- Selenium Configuration ---
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--log-level=3')  # Suppress warnings
# Add a user-agent to potentially avoid some blocking
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")


# --- Function to Get Page Source using Selenium ---
def get_page_source_selenium(url, chrome_options):
    """
    Use Selenium to fetch page source and return parsed lxml tree.
    Includes a small wait to allow dynamic content to load.
    """
    driver = webdriver.Chrome(options=chrome_options)
    try:
        print(f"Fetching page: {url}")
        driver.get(url)
        # Add a small implicit wait or a time.sleep if needed
        # Depending on the page's dynamic loading, you might need to wait
        # for specific elements to appear using WebDriverWait
        time.sleep(3) # Simple sleep, consider WebDriverWait for robustness

        html = driver.page_source
        print("Page fetched successfully.")
        # Extract the HTML source and parse with lxml
        tree = etree.HTML(html)
        return tree
    except Exception as e:
        print(f"Error fetching page source: {e}")
        return None
    finally:
        driver.quit()

# --- Function to Extract Data using XPath ---
def extract_data_xpath(tree):
    """
    Extracts financial data from the lxml tree using XPath.
    Targets visible elements on the Yahoo Finance quote page.
    """
    if tree is None:
        return None

    # --- Define XPath expressions ---
    # These XPaths are based on your original code and typical Yahoo Finance structure.
    # They might need adjustment if Yahoo Finance changes its layout.
    # Targeting the main price, change, and percentage change elements.
    xpath_price = '//*[@id="nimbus-app"]/section/section/section/article/section[1]/div[2]/div[1]/section/div/section/div[1]/div[1]/span/text()'
    xpath_change = '//*[@id="nimbus-app"]/section/section/section/article/section[1]/div[2]/div[1]/section/div/section/div[1]/div[2]/span/text()'
    xpath_change_percent_alt = '//*[@id="nimbus-app"]/section/section/section/article/section[1]/div[2]/div[1]/section/div/section/div[1]/div[3]/span/text()' 

    # XPath for market time (often near the price or change)
    # This might be less reliably available via XPath than price/change
    # Let's try to find it near the price section
    xpath_market_time = '//*[@id="nimbus-app"]/section/section/section/article/section[1]/div[2]/div[1]/section/div/section/div[2]/span/span/text()' # Example XPath, verify on page

    print("Attempting to extract data using XPath...")

    try:
        # Get elements using XPath
        price_elements = tree.xpath(xpath_price)
        change_elements = tree.xpath(xpath_change)
        # Try the alternative change percent xpath first, fall back if needed
        change_percent_elements = tree.xpath(xpath_change_percent_alt)
        time_elements = tree.xpath(xpath_market_time)


        # Extract text and clean up
        # Use [0] to get the first element if the list is not empty
        raw_price = price_elements[0].strip() if price_elements else None
        raw_change = change_elements[0].strip().replace('+','') if change_elements else None
        raw_change_percent = change_percent_elements[0].strip().replace('(', '').replace(')', '').replace('+', '').replace('%','') if change_percent_elements else None
        raw_time_text = time_elements[0].strip() if time_elements else None # This might need further parsing
        print(raw_price, raw_change, raw_change_percent, raw_time_text)

        # Convert to float, handle potential None values
        fmt_price = float(raw_price) if raw_price else None
        fmt_change = float(raw_change) if raw_change and raw_change != '-' else 0.0 # Handle '-' for no change
        fmt_change_percent = float(raw_change_percent) if raw_change_percent and raw_change_percent != '-' else 0.0 # Handle '-'

        # For time, cleaning it up depends on its format. Yahoo often shows
        # something like "At close: 7:00PM UTC-4". You might need regex here
        # if you want to parse it into a specific datetime object.
        # For simplicity, returning the raw text for now.
        fmt_time = raw_time_text # Keep as string for now

        # Check if essential data was found
        if fmt_price is None:
             print("Warning: Could not find price using XPath.")
             return None # Or return partial data if acceptable

        print("Data extracted successfully.")

        return {
            "symbol": "CNH=X", # Hardcoded symbol
            "fmtMarketTime": fmt_time,     # Processed time (currently same as raw)
            "fmtMarketPrice": fmt_price,
            "fmtMarketChange": fmt_change,
            "fmtMarketChangePercent": fmt_change_percent
        }

    except Exception as e:
        print(f"Error during XPath data extraction: {e}")
        return None

# --- Function to Save Data to MySQL ---
def save_to_mysql(data_dict, table_name="market_data"):
    """
    Saves extracted data to a MySQL database.
    Requires database connection details.
    """
    if data_dict is None:
        print("No data to save.")
        return

    # --- Database Connection Details (REPLACE WITH YOUR OWN) ---
    db_config = {
        'host': 'your_db_host',
        'user': 'your_db_user',
        'password': 'your_db_password',
        'database': 'your_db_name',
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor # Optional: returns results as dictionaries
    }

    conn = None
    try:
        print(f"Connecting to database '{db_config['database']}' on '{db_config['host']}'...")
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        print("Database connection successful.")

        # SQL INSERT statement - Adjust column names based on your table schema
        # Ensure your table 'market_data' has columns like symbol, rawMarketTime, etc.
        sql = f"""
        INSERT INTO `{table_name}` (
            `symbol`, `rawMarketTime`, `fmtMarketTime`,
            `rawMarketPrice`, `fmtMarketPrice`,
            `rawMarketChange`, `fmtMarketChange`,
            `rawMarketChangePercent`, `fmtMarketChangePercent`
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Prepare the data tuple in the correct order
        data_tuple = (
            data_dict.get('symbol'),
            data_dict.get('fmtMarketTime'),
            data_dict.get('fmtMarketPrice'),
            data_dict.get('fmtMarketChange'),
            data_dict.get('fmtMarketChangePercent')
        )

        print("Executing INSERT query...")
        cursor.execute(sql, data_tuple)
        conn.commit()
        print("Data saved successfully.")

    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        if conn:
            conn.rollback() # Roll back the transaction on error
    except Exception as e:
        print(f"An unexpected error occurred during database save: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Database connection closed.")


# --- Main Execution Block ---
if __name__ == "__main__":
    # Get the page source using Selenium and parse with lxml
    # Note: The history page might not have the live quote data elements
    # Let's change the URL to the main quote page for live data extraction
    url_quote = 'https://finance.yahoo.com/quote/CNH=X/'
    page_tree = get_page_source_selenium(url_quote, chrome_options)

    # Extract data using XPath
    market_data = extract_data_xpath(page_tree)

    # Print extracted data
    if market_data:
        print("\n--- Extracted Market Data ---")
        for key, value in market_data.items():
            print(f"{key}: {value}")
        print("-----------------------------")

        # Save to MySQL database (uncomment and configure db_config above)
        # print("\nAttempting to save data to database...")
        # save_to_mysql(market_data)
    else:
        print("\nFailed to extract market data.")