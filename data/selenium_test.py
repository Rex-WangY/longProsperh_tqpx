from selenium.common.exceptions import TimeoutException, NoSuchElementException # Import specific exceptions
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import time

# Optional: for automatically managing chromedriver executable

# --- Selenium Configuration ---
chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--log-level=3')  # Suppress warnings
# Add a user-agent to potentially avoid some blocking
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")


# Set up the WebDriver (assuming ChromeDriver is in your PATH or managed by webdriver_manager)
# service = Service('/path/to/chromedriver') # If not using webdriver_manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)


def extract_data(url,refresh_interval_seconds=60):
    
    # Define the XPath for the specific price element
    xpath_price = '//*[@id="nimbus-app"]/section/section/section/article/section[1]/div[2]/div[1]/section/div/section/div[1]/div[1]/span'
    xpath_change = '//*[@id="nimbus-app"]/section/section/section/article/section[1]/div[2]/div[1]/section/div/section/div[1]/div[2]/span'
    xpath_change_percent_alt = '//*[@id="nimbus-app"]/section/section/section/article/section[1]/div[2]/div[1]/section/div/section/div[1]/div[3]/span' 
    xpath_time = '//*[@id="nimbus-app"]/section/section/section/article/section[1]/div[2]/div[1]/section/div/section/div[2]/span/span'

    try:
        driver.get(url)
        print(f"Navigated to {url}")

        while True:
            print("# ------- WHILE LOOP STARTED ------- #")

            try:
                # --- Wait for the specific price element to be present and visible ---
                # Using the corrected XPath
                print("Waiting for price element to be visible...")
                WebDriverWait(driver, 10).until(
                    EC.all_of(
                        EC.visibility_of_element_located((By.XPATH, xpath_price)),
                        EC.visibility_of_element_located((By.XPATH, xpath_change)),
                        EC.visibility_of_element_located((By.XPATH, xpath_change_percent_alt)),
                        EC.visibility_of_element_located((By.XPATH, xpath_time))
                    )
                )
                print("element is visible.")

                # ------ MARKET PRICE ELEMENT AND EXTRACT ------ #
                price_element = driver.find_element(By.XPATH, xpath_price)
                extracted_price = price_element.text
                print(f"Extracted Price: {extracted_price}")
                
                # ------ MARKET PRICE CHANGE ELEMENT AND EXTRACT ------ #
                change_element = driver.find_element(By.XPATH, xpath_change)
                extracted_change = change_element.text
                print(f"Extracted Price: {extracted_change}")
                
                # ------ MARKET PRICE CHANGE PERCENT ELEMENT AND EXTRACT ------ #
                change_percent_element = driver.find_element(By.XPATH, xpath_change_percent_alt)
                extracted_changePercent = change_percent_element.text
                print(f"Extracted Price: {extracted_changePercent}")
                
                # ------ MARKET DATE ELEMENT AND EXTRACT ------ #
                time_element = driver.find_element(By.XPATH, xpath_time)
                extracted_time = time_element.text
                print(f"Extracted Price: {extracted_time}")
                
                # # --- Extract the text from the price element ---
                
                # # Extract text and clean up
                raw_price = extracted_price if float(extracted_price) else None
                raw_change = extracted_change.replace('+','') if extracted_change else None
                raw_change_percent = extracted_changePercent.replace('+','').replace('(','').replace('%','').replace(')','') if extracted_changePercent else None
                raw_time = extracted_time if extracted_time else None # This might need further parsing
                # print(raw_price, raw_change, raw_change_percent, raw_time)

                    # You would typically process/store the data here
                    # save_to_database(extracted_data)
                    # append_to_file(extracted_data)

            except TimeoutException:
                print(f"Timeout waiting for the price element ({xpath_price}). Page might not have loaded correctly or structure changed.")
                # You might choose to break the loop or continue to the next refresh
                # break # Uncomment to stop on timeout
            except NoSuchElementException:
                print(f"Price element not found with the specified XPath ({xpath_price}). Page structure may have changed.")
                # You might choose to break the loop or continue
                # break # Uncomment to stop if element is never found
            except Exception as e:
                print(f"An unexpected error occurred during data extraction in cycle: {e}")
                # You might choose to break the loop or continue
                # break # Uncomment to stop on other errors


            # --- Prepare for the next refresh ---
            print(f"Waiting {refresh_interval_seconds} seconds before refreshing...")
            time.sleep(refresh_interval_seconds)
            driver.refresh()
            print("Page refreshed.")

    except Exception as e:
        print(f"An error occurred during the main process: {e}")

    finally:
        # --- Clean up ---
        print("Closing browser.")
        driver.quit()

if __name__ == "__main__":
    
    url_quote = 'https://finance.yahoo.com/quote/CNH=X/'
    refresh_interval_seconds = 15 # Refresh every 60 seconds
    extract_data(url_quote,refresh_interval_seconds)