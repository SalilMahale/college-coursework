from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Download & get path of ChromeDriver
driver_path = ChromeDriverManager().install()
print("ChromeDriver path is:", driver_path)

# Create a Service object using this path
service = Service(driver_path)

# Launch Chrome using this service
driver = webdriver.Chrome(service=service)
driver.get("https://www.google.com")
print(driver.title)
driver.quit()
