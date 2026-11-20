from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# --- Setup ---
driver = webdriver.Chrome()  # Make sure chromedriver is installed and in PATH
driver.maximize_window()

# Open the local HTML file (your website)
driver.get("bookmyvehicle.html")  # Change to your HTML file path
print("✅ Website loaded successfully")

# --- Verify Page Title ---
WebDriverWait(driver, 5).until(lambda d: "BookMyVehicle" in d.title)
print("✅ Title check passed:", driver.title)

# --- Verify Navigation Bar ---
nav_links = WebDriverWait(driver, 5).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".nav-btn"))
)
assert len(nav_links) >= 3
print("✅ Navigation bar loaded")

# Function to handle booking flow
def book_vehicle(vehicle_type, brand, model, vehicle_no, start, end, pay_method):
    # Click the appropriate button
    btn_xpath = f"//button[contains(text(), 'Book a {vehicle_type.capitalize()}')]"
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, btn_xpath))
    ).click()

    # Wait for modal inputs to appear
    brand_input = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "inpBrand"))
    )
    model_input = driver.find_element(By.ID, "inpModel")
    vehicle_input = driver.find_element(By.ID, "inpVehNo")
    start_date = driver.find_element(By.ID, "inpStart")
    end_date = driver.find_element(By.ID, "inpEnd")
    check_btn = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.ID, "toCheck")))


    # Fill form
    brand_input.clear(); brand_input.send_keys(brand)
    model_input.clear(); model_input.send_keys(model)
    vehicle_input.clear(); vehicle_input.send_keys(vehicle_no)
    start_date.clear(); start_date.send_keys(start)
    end_date.clear(); end_date.send_keys(end)

    # Click Check Availability
    check_btn.click()
    time.sleep(1)

    # Wait for the modal to update and check for "Available"
    modal = WebDriverWait(driver, 5).until(
    EC.visibility_of_element_located((By.ID, "modal"))
)
    available = "Available" in modal.text
    if not available:
        print(f"❌ {vehicle_type.capitalize()} not available, skipping payment")
        return False

    # Proceed to payment
    proceed_btn = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.ID, "proceedPayment")))

    proceed_btn.click()
    time.sleep(0.5)

    if pay_method.lower() == "cash":
        # Wait for and click "Continue"
        confirm_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "confirmPay"))
        )
        confirm_btn.click()
        # Now wait for and click "Generate report"
        gen_report = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "genRpt"))
        )
        gen_report.click()
    
    elif pay_method.lower() == "upi":
        # Wait for the payment modal and select UPI before clicking Continue
        try:
            pmethod = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "pmethod"))
            )
            from selenium.webdriver.support.ui import Select
            Select(pmethod).select_by_visible_text("Pay by UPI")
            time.sleep(0.5)  # Give time for modal to update
        except Exception as e:
            print("⚠️ Could not select UPI payment method:", e)
        # Now click Continue
        confirm_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "confirmPay"))
        )
        confirm_btn.click()
        # Wait for Paid button and click it
        paid_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "paidBtn"))
        )
        paid_btn.click()
        # Wait for Generate report button and click it
        gen_report = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "genRpt2"))
        )
        gen_report.click()
    print(f"✅ {vehicle_type.capitalize()} booking completed with {pay_method} payment")

# --- Book a Car ---
book_vehicle(
    vehicle_type="car",
    brand="Hyundai",
    model="i20 Sportz",
    vehicle_no="MH12AB1234",
    start="2025-10-27",
    end="2025-10-29",
    pay_method="cash"
)
# --- Handle alert if present ---
try:
    WebDriverWait(driver, 3).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()
    print("✅ Alert closed after car booking")
except:
    pass
# --- Book a Bike ---
# Go back to Home if SPA uses sections
home_nav = driver.find_element(By.CSS_SELECTOR, '.nav-btn[data-target="home"]')
home_nav.click()
time.sleep(1)

book_vehicle(
    vehicle_type="bike",
    brand="Yamaha",
    model="FZ-X",
    vehicle_no="MH14XY9876",
    start="2025-11-01",
    end="2025-11-03",
    pay_method="upi"
)

# --- Handle alert if present after bike booking ---
try:
    WebDriverWait(driver, 3).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()
    print("✅ Alert closed after bike booking")
except:
    pass

# --- Verify Reports Section ---
reports_nav = driver.find_element(By.CSS_SELECTOR, '.nav-btn[data-target="reports"]')
reports_nav.click()
time.sleep(1)

reports = driver.find_elements(By.CLASS_NAME, "report-item")
assert len(reports) >= 1
print(f"✅ {len(reports)} report(s) generated and visible in Reports section")

# --- Done ---
print("🎯 Automated End-to-End Testing Completed Successfully")
driver.quit()
