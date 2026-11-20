from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Set your driver path
driver_path = None  # set to your chromedriver path, or leave None to let Selenium Manager find it

# Create Service object
service = Service(executable_path=driver_path)

# Initialize the Chrome driver with the service object
driver = webdriver.Chrome(service=service)

# The rest of your code remains the same...
url = 'vehicle_management.html'

try:
    driver.get(url)
    time.sleep(1)  # Wait for page to load
    
    print("Test ran successfully!")

finally:
    driver.quit()
