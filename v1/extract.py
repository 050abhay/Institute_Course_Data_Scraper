import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Initialize the list of institute codes
institute_codes = ['002','004','005','007','010','011','014','016','017','019','027','029','030','032','033','035','037','038','039','040','043','044','046','047','048','050','051','052','053','054','056','057','059','064','065','067','068','069','070','074','076','077','079','082','083','084','085','088','090','091','094','095','096','097','098','099','104','106','107','108','109','110','112','113','114','116','117','120','122','123','124','127','128','129','132','133','134','135','138','139','141','142','143','144','145','151','152','153','154','157','159','162','163','164','165','166','172','173','174','175','177','179','182','187','189','190','192','193','203','212','215','216','220','221','222','223','225','229','230','231','238','239','240','248','254','256','263','265','272','274','277','280','282','283','284','285','287','290','292','306','307','310','311','312','318','319','321','333','339','340','341','345','349','350','351','353','358','360','361','362','363','364','370','373','374','380','382','383','384','394','396','411','414','419','422','423','425','428','430','431','434','438','447','448','450','465','467','471','472','474','479','480','481','483','484','485','486','487','488','490','492','493','496','498','499','501','502','505','511','514','517','518','520','521','523','524','525','527','533','536','540','545','547','548','557','561','576','579','581','582','583','584','586','588','593','599','607','609','617','621','622','636','640','641','643','644','648','649','653','659','661','666','672','673','679','680','682','686','687','689','692','695','697','703','705','708','714','719','720','722','723','727','732','733','734','735','736','737','740','743','747','749','751','756','757','760','761','765','766','780','781','783','785','786','789','790','791','792','796','797','799','802','803','810','812','815','817','820','822','826','828','834','835','839','840','841','849','857','858','899','903','950','982','990','996','1069','1131','1134','1155','1156','1177','1186','1187','1188','1189','1190','1192','1193','1194','1195','1197','1198','1200','1201','1209','1211','1212','1213','1214','1215','1216','1217','1218','1219','1220']  # Add more as needed

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
