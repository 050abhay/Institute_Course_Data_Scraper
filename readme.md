# Institute Course Data Scraper

## Description
The Institute Course Data Scraper is a Python-based web scraping application designed to collect and organize detailed information about various educational institutions and their offered courses from the AKTU (Dr. A.P.J. Abdul Kalam Technical University) website. Leveraging the power of Selenium for browser automation, this project efficiently retrieves data on institutes' names, course offerings, branches, and intake capacities.

## Key Features

- **Dynamic Data Retrieval**: The scraper constructs URLs based on a predefined list of institute codes, enabling efficient data extraction without manual intervention.
  
- **Course Information Compilation**: For each institute, the application navigates to the "Courses" tab, extracting relevant details from an organized HTML table, which includes course names, branch names, and intake values.
  
- **Data Structuring**: The collected data is structured in a pandas DataFrame, allowing for easy manipulation and analysis. The application ensures that unique course names are captured and organized, facilitating a clear presentation of the information.
  
- **Output to Excel**: The final dataset is exported to an Excel file, making it accessible for further analysis or reporting purposes.
  
- **Scalability**: The code is designed to accommodate additional institute codes, making it adaptable to future requirements as more institutions or courses may need to be added.

## Purpose
This project serves as an invaluable tool for educational administrators, researchers, and prospective students seeking comprehensive insights into the course offerings across various institutes affiliated with AKTU. By automating the data collection process, it significantly reduces the time and effort required to compile this information manually.
