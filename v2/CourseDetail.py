import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Load institute codes from the Excel file
input_file = './college_data.xlsx'  # Update this to your actual file path

# Load institute codes from the Excel file and ensure Inst_Code is read as string
df_codes = pd.read_excel(input_file, dtype={'Inst_Code': str})
institute_codes = df_codes['Inst_Code'].tolist()  # Already in string format


# Dictionary to store the data
data = {}

# Initialize headers with 'Inst_Code' and 'Inst_Name'
headers = ['Inst_Code', 'Inst_Name']

# Set up the ChromeDriver path and options
driver_path = '../chromedriver.exe'
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

for inst_code in institute_codes:
    url = f"https://erp.aktu.ac.in/WebPages/KYC/CollegeDetailedInformation.aspx?Inst={inst_code}%20%20&S=25"
    driver.get(url)

    time.sleep(3)  # Adjust sleep time if needed

    # Extract the institute name
    inst_name = driver.find_element(By.ID, 'ContentPlaceHolder1_lblCollegeName').text.strip()

    # Find the 'Courses' tab and switch to it
    driver.find_element(By.XPATH, "//a[@href='#courses']").click()
    time.sleep(2)  # Wait for tab to load

    # Extract the table data
    table = driver.find_element(By.ID, 'ContentPlaceHolder1_grdCoursesCourse')
    rows = table.find_elements(By.TAG_NAME, 'tr')

    # Initialize a dictionary for this institute
    row_data = {'Inst_Code': inst_code.zfill(3), 'Inst_Name': inst_name}

    # Process each row in the table
    for row in rows[1:]:
        cols = row.find_elements(By.TAG_NAME, 'td')
        course_name = cols[0].text.strip()
        branch_name = cols[1].text.strip()
        intake_value = int(cols[3].text.strip())

        # Abbreviate the course names
        if 'Master of Computer Applications' in course_name:
            course_name = 'MCA'
        elif 'Masters of Business Administration' in course_name:
            course_name = 'MBA'
        elif 'Bachelor of Technology' in course_name:
            course_name = 'B.Tech'
        elif 'Master of Technology' in course_name:
            course_name = 'M.Tech'

        # Concatenate course name and branch name
        header = f"{course_name} - {branch_name}"

        # Add header if it's not already in headers
        if header not in headers:
            headers.append(header)

        # Fill the intake value under the correct header
        row_data[header] = intake_value

    # Add the row data to the main data dictionary
    data[inst_code] = row_data

# Convert data to DataFrame
df = pd.DataFrame.from_dict(data, orient='index', columns=headers)

# Save the DataFrame to Excel
output_file = 'institutes_data.xlsx'
df.to_excel(output_file, index=False)

print(f"Data saved to {output_file}")

# Close the browser
driver.quit()
