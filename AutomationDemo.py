from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize WebDriver
browser_driver = webdriver.Chrome()  # Make sure you have ChromeDriver in your PATH

try:
    # Step 1: Navigate to Amazon India
    browser_driver.get("https://www.amazon.in/")

    # Step 2: Verify landing on the correct page
    assert "Amazon" in browser_driver.title
    print("Landed on the correct page")
    print(f"Page Title: {browser_driver.title}")
    print(f"Page URL: {browser_driver.current_url}")

    # Step 3: Search for "mobile"
    search_input_field = browser_driver.find_element(By.ID, "twotabsearchtextbox")
    search_input_field.send_keys("mobile")
    search_input_field.send_keys(Keys.RETURN)

    # Step 4: Select 4 stars under customer review filter
    WebDriverWait(browser_driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//i[@class='a-icon a-icon-star-medium a-star-medium-4']"))).click()

    # Step 5: Select the price range between ₹10,000 - ₹20,000
    browser_driver.get(
        "https://www.amazon.in/s?k=mobile&crid=1I1F2B7PGKJSV&qid=1725027060&rnid=1318502031&sprefix=mobil%2Caps%2C206&ref=sr_nr_p_36_0_0&low-price=10000&high-price=20000")
    WebDriverWait(browser_driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//i[@class='a-icon a-icon-star-medium a-star-medium-4']"))).click()

    # Wait for the page to load with filtered results
    time.sleep(3)

    # Step 6: Open the first search result in a new tab
    first_search_item = WebDriverWait(browser_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "(//div[@data-component-type='s-search-result'])[1]//h2/a")))
    first_product_url = first_search_item.get_attribute('href')

    # Use JavaScript to open the product link in a new tab
    browser_driver.execute_script(f"window.open('{first_product_url}');")

    # Switch to the new tab
    browser_driver.switch_to.window(browser_driver.window_handles[1])

    # Step 7: Add to cart
    cart_button_element = WebDriverWait(browser_driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='add-to-cart-button' and @name='submit.add-to-cart' and @title='Add to Shopping Cart' and @type='submit' and @value='Add to Cart']")))
    cart_button_element.click()

    # Step 8: Go to cart button
    view_cart_element = WebDriverWait(browser_driver, 10).until(
        EC.element_to_be_clickable((By.XPATH,
                                    "//input[@class='a-button-input' and @type='submit' and @aria-labelledby='attach-sidesheet-view-cart-button-announce']"))
    )
    view_cart_element.click()

    # Wait to ensure cart is updated
    time.sleep(3)

    # Step 9: Print confirmation message
    print("Product added to cart successfully.")

except Exception as err:
    print(f"An error occurred: {err}")

finally:
    # Close the browser
    browser_driver.quit()
