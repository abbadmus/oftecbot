from seleniumbase import Driver
import time
import csv

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains


from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

list_postcode = []

driver = Driver(uc=True)

# Specify the path to your CSV file
# Replace with the actual path to your CSV file
csv_file_path = 'postcodes unique.csv'

# Read the CSV file and extract the "Postcode" column
with open(csv_file_path, mode='r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        postcode = row['Postcode']
        list_postcode.append(postcode)

# Print the list of postcodes
print(list_postcode)


def get_eacch_postcode(postcode, driver):

    driver.get("https://www.oftec.org/find-technician")

    # Locate the <select> element by its id
    select_element = Select(driver.find_element(By.ID, "SearchType"))

    # Select the option by its visible text
    select_element.select_by_visible_text(
        "Find a technician by the type of work you require")

    # Locate the <select> element by its id
    select_element = Select(driver.find_element(By.ID, "TypeOfWork"))

    # Select the option by its visible text
    select_element.select_by_visible_text("Installation work")
    driver.click("#SelectedWork1-0")

    driver.type("#postcode", postcode)

    driver.click("#singlebutton")

    # Set an explicit wait with a timeout (e.g., 10 seconds)
    wait = WebDriverWait(driver, 6)

    # time.sleep(3)
    wait.until(EC.presence_of_element_located(
        (By.XPATH,  "//tr[@class='rows']")))

    # Find all the rows that need to be clicked
    rows_to_click = driver.find_elements(By.XPATH, "//tr[@class='rows']")

    # Create a list to store the extracted data
    company_details_list = []

    # Iterate through each row, click on it, and extract company details
    print(len(rows_to_click))

    for index, row in enumerate(rows_to_click):
        try:

            print(index)
            # if len(company_details_list) == 5:
            #     break
            # Wait for the element to be clickable
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(row)
            )

            element.click()
            # time.sleep(3)
            wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR,  "th.tlabel + th")))

            # Extract company details
            company_name = driver.find_element(
                By.CSS_SELECTOR, "th.tlabel + th").text
            company_name = company_name.split("\n")[0].strip()

            company_address = driver.find_element(
                By.XPATH, "//td[@class='tlabel'][contains(text(), 'Address')]/following-sibling::td").text
            company_address = company_address.strip().replace("\n", " ")

            company_telephone = driver.find_element(
                By.XPATH, "//td[@class='tlabel'][contains(text(), 'Telephone')]/following-sibling::td").text
            company_telephone = company_telephone.strip()

            company_email = driver.find_element(
                By.XPATH, "//td[@class='tlabel'][contains(text(), 'Email')]/following-sibling::td/a").get_attribute("href")
            company_email = company_email.strip()

            # Append the extracted data to the list
            company_details_list.append({
                "Company Name": company_name,
                "Address": company_address,
                "Telephone": company_telephone,
                # Remove "mailto:" from the email
                "Email": company_email.replace("mailto:", "")
            })

            time.sleep(2)
        except ElementClickInterceptedException as e:
            # Handle the exception gracefully
            print(f"ElementClickInterceptedException: {e}")

    csv_file_path = f"company details {postcode}.csv"

    # Write the extracted data to the CSV file
    with open(csv_file_path, "w", newline="", encoding="utf-8") as csv_file:
        fieldnames = company_details_list[0].keys()
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Write the data rows
        for company_details in company_details_list:
            writer.writerow(company_details)

    print(f"Company details have been saved to {csv_file_path}")
    time.sleep(3)


for code in list_postcode[:2]:
    get_eacch_postcode(code, driver)

time.sleep(1000)
