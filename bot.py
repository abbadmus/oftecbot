import requests
from time import sleep
from random import choice
from bs4 import BeautifulSoup
import pandas as pd


url = "https://www.doogal.co.uk/UKPostcodes"

df = pd.read_csv('postcodes.csv')

df = df[df["In Use?"] == "Yes"]

df = df.drop_duplicates(subset=['Postcode area'], keep='first')

# Change 'output_file.xlsx' to your desired output file name.
df.to_csv('postcodes unique.csv', index=False)

# # Send an HTTP GET request to the URL and parse the HTML
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'html.parser')

# # Locate the table on the webpage using a CSS selector
# # Replace 'table_selector' with the selector that matches your table
# table_selector = 'table.table.table-responsive.table-hover#tech-results'
# table = soup.select_one(table_selector)

# if table:
#     # Use Pandas to read the HTML table and convert it into a DataFrame
#     df = pd.read_html(str(table))[0]

#     # Now you have the table data in a Pandas DataFrame
#     # You can access and manipulate the data as needed
#     print(df)
# else:
#     print("Table not found on the webpage.")
