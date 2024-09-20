from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Initialize the WebDriver
driver = webdriver.Chrome()

# Open the website
driver.get("https://kyc.aktu.ac.in/")

# Maximize window and wait for the page to load
driver.maximize_window()
wait = WebDriverWait(driver, 15)

# Step 1: Check if page contains iframe and switch to it
try:
    # Wait and switch to iframe if present (adjust iframe locator if needed)
    iframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
    driver.switch_to.frame(iframe)
    print("Switched to iframe.")
except Exception:
    print("No iframe found or switching to iframe failed.")

# Step 2: Select "Bachelor of Technology" from the "All Courses" dropdown
try:
    # Wait for the dropdown to be visible and clickable
    course_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-id="ddlCourses"]')))
    
    # Click to open the dropdown
    course_dropdown.click()
    print("Dropdown for courses clicked.")
    
    # Wait for and select "Bachelor of Technology" option
    btech_option = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Bachelor of Technology"]')))
    btech_option.click()
    print("Bachelor of Technology selected.")

    # Pause to allow the institute list to load after selecting the course
    time.sleep(3)
    
except Exception as e:
    print(f"Error selecting course: {e}")

# Step 3: Extract college codes and names from the "All Institutes" section
college_data = []

try:
    # Wait for the institute dropdown to be clickable
    institute_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-id="ddlInstitute"]')))
    
    # Click to open the dropdown
    institute_dropdown.click()
    print("Dropdown for institutes clicked.")

    # Extract the options from the dropdown
    institutes = driver.find_elements(By.XPATH, '//ul[@class="dropdown-menu inner"]/li/a/span[@class="text"]')

    for institute in institutes:
        text = institute.text
        if text.strip() and "All Institutes" not in text:
            code, name = text.split(maxsplit=1)
            college_data.append((code.strip(), name.strip()))
    
    print(f"Extracted {len(college_data)} institutes.")

except Exception as e:
    print(f"Error extracting institute data: {e}")

# Close the driver after extraction
driver.quit()

# Step 4: Store the extracted college data in an Excel file
if college_data:
    # Create a DataFrame from the extracted data
    df = pd.DataFrame(college_data, columns=["Inst_Code", "Inst_Name"])

    # Save the DataFrame to an Excel file
    df.to_excel("college_data.xlsx", index=False)
    print("College data saved to college_data.xlsx")
else:
    print("No data to save.")
