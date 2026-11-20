from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def print_result(test, outcome):
    print(f"{test}: {outcome}")

# Configuration: use headless browser for automated testing (optional)
chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get("http://127.0.0.1:5000")

    # Test 1: Booking vehicle (should succeed)
    driver.find_element(By.NAME, "user_id").clear()
    driver.find_element(By.NAME, "user_id").send_keys("101")
    driver.find_element(By.NAME, "action").click()
    time.sleep(1)
    msg = driver.find_element(By.ID, "msg").text
    print_result("Test 1 (booking)", msg)  # Expect "Booking successful"

    # Test 2: Booking again (should fail)
    driver.refresh()
    driver.find_element(By.NAME, "action").click()
    time.sleep(1)
    msg = driver.find_element(By.ID, "msg").text
    print_result("Test 2 (booking again)", msg)  # Expect "Booking failed"

    # Test 3: Payment with valid method (should succeed)
    driver.refresh()
    driver.find_elements(By.NAME, "action")[1].click()
    time.sleep(1)
    msg = driver.find_element(By.ID, "msg").text
    print_result("Test 3 (payment)", msg)  # Expect "Payment successful"

    # Test 4: Payment with invalid method (should fail)
    driver.refresh()
    driver.find_element(By.NAME, "method").clear()
    driver.find_element(By.NAME, "method").send_keys("card")
    driver.find_elements(By.NAME, "action")[1].click()
    time.sleep(1)
    msg = driver.find_element(By.ID, "msg").text
    print_result("Test 4 (invalid payment method)", msg)  # Expect "Invalid payment method"

    # Test 5: Payment before booking (should fail) - Clear booking by refreshing server or resetting app; else omit new driver
    driver.refresh()
    driver.find_elements(By.NAME, "action")[1].click()
    time.sleep(1)
    msg = driver.find_element(By.ID, "msg").text
    print_result("Test 5 (payment before booking)", msg)


finally:
    driver.quit()
