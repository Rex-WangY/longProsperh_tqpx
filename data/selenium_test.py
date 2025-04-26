from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException # Import specific exceptions

# Optional: for automatically managing chromedriver executable
from webdriver_manager.chrome import ChromeDriverManager

# Set up the WebDriver (assuming ChromeDriver is in your PATH or managed by webdriver_manager)
# service = Service('/path/to/chromedriver') # If not using webdriver_manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

url = 'https://finance.yahoo.com/quote/CNH=X/'
refresh_interval_seconds = 15 # Refresh every 60 seconds
max_refreshes = 10 # Or loop indefinitely, or based on time


# Define the XPath for the specific price element
xpath_price_element = '//*[@id="nimbus-app"]/section/section/section/article/section[1]/div[2]/div[1]/section/div/section/div[1]/div[1]/span'

try:
    driver.get(url)
    print(f"Navigated to {url}")

    for i in range(max_refreshes):
        print(f"\n--- Refresh Cycle {i+1} ---")

        try:
            # --- Wait for the specific price element to be present and visible ---
            # Using the corrected XPath
            print("Waiting for price element to be visible...")
            price_element = WebDriverWait(driver, 20).until( # Increased wait time just in case
                EC.visibility_of_element_located((By.XPATH, xpath_price_element))
            )
            print("Price element is visible.")

            # --- Extract the text from the price element ---
            extracted_price = price_element.text
            print(f"Extracted Price: {extracted_price}")

                # You would typically process/store the data here
                # save_to_database(extracted_data)
                # append_to_file(extracted_data)

        except TimeoutException:
            print(f"Timeout waiting for the price element ({xpath_price_element}). Page might not have loaded correctly or structure changed.")
            # You might choose to break the loop or continue to the next refresh
            # break # Uncomment to stop on timeout
        except NoSuchElementException:
             print(f"Price element not found with the specified XPath ({xpath_price_element}). Page structure may have changed.")
             # You might choose to break the loop or continue
             # break # Uncomment to stop if element is never found
        except Exception as e:
             print(f"An unexpected error occurred during data extraction in cycle {i+1}: {e}")
             # You might choose to break the loop or continue
             # break # Uncomment to stop on other errors


        # --- Prepare for the next refresh ---
        if i < max_refreshes - 1: # Don't wait after the last cycle
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