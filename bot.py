from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import pandas as pd
from io import StringIO
from googletrans import Translator
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
import os
cusoptions = webdriver.ChromeOptions()
myoptions = webdriver.ChromeOptions()

prefs = {
  "translate_whitelists": {"en":"hi"},
  "translate":{"enabled":True}
}
myoptions.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=myoptions)


# Set PostgreSql Uri
engine = create_engine(os.getenv('URI'))
# Open the website
driver.get('https://pay2igr.igrmaharashtra.gov.in/eDisplay/propertydetails')


# Selecting Appropriate Values
year_dropdown = driver.find_element(By.NAME, 'years')
year_dropdown.send_keys('2023')
time.sleep(1)
district_dropdown = driver.find_element(By.NAME, 'district_id')
district_dropdown.send_keys("मुंबई उपनगर")
time.sleep(1)
taluka_dropdown = driver.find_element(By.NAME, 'taluka_id')
taluka_dropdown.send_keys("अंधेरी")
time.sleep(1)
village_dropdown = driver.find_element(By.NAME, 'village_id')
village_dropdown.send_keys("बांद्रा")
searbox = driver.find_element(By.NAME, 'free_text')
searbox.send_keys("2023")



# Captcha Reading
key = 'captcha'
script = f'return sessionStorage.getItem("{key}");'
result = driver.execute_script(script)
taluka_dropdown = driver.find_element(By.NAME, 'captcha')
taluka_dropdown.send_keys(result)


# Searching ...
taluka_dropdown = driver.find_element(By.ID, 'submit')
taluka_dropdown.click()
time.sleep(3)

pagination = driver.find_element(By.NAME, 'tableparty_length')
pagination.send_keys("50")

# Getting table data after search
table_element = driver.find_element(By.ID,'tableparty')
table_html = table_element.get_attribute('outerHTML')
table_html_io = StringIO(table_html)
df = pd.read_html(table_html_io)
df = pd.DataFrame(df[0])


translator = Translator()
def translate_to_english(cell_value):
  try:
    return translator.translate(cell_value, src='mr', dest='en').text
  except Exception as e:
    return str(e)
df.columns = df.columns.map(translate_to_english)

# Cleaning and changing Df Column Names to readable format
columns_to_drop = ['Anu no.']
columns_to_drop_existing = [col for col in columns_to_drop if col in df.columns]
if columns_to_drop_existing:
    df = df.drop(columns=columns_to_drop_existing)
df.rename(columns={'Anu': 'Sr.No'}, inplace=True)
df.rename(columns={'List no.1': 'Document Link'}, inplace=True)
df.columns.values[4] = 'Buyer Name'
df.columns.values[5] = 'Seller Name'
df['Document no.'] = df['Document no.'].astype(str)
df['Year'] = pd.to_datetime(df['Year'])
df['Year'] = df['Year'].dt.strftime('%Y-%m-%d')


df_english = df.map(translate_to_english)
soup = BeautifulSoup(table_html, 'html.parser')

a_tag = soup.find_all('a')
links = []
for tag in a_tag:
    links.append("https://pay2igr.igrmaharashtra.gov.in" + tag.get('href'))
df_english['Document Link'] = links



table_name = 'scrapped_data'
column_mapping = {
   'Document no.' : 'doc_no',
   'Type of documentation' : 'doc_type',
   'Well.Ni.Office' : 'office_circle',
   'Year' : 'year',
   'Buyer Name' : 'buyer_name',
   'Seller Name': 'seller_name',
   'Other information' : 'other_info',
   'Document Link' : 'doc_link'
}
df_english.rename(columns=column_mapping, inplace=True)
df_english.to_sql(table_name, engine, if_exists='replace', index=False)

# Close the database connection
engine.dispose()

df_english.to_csv("EnlgishScrapedData.csv")



input('Press Enter to close the browser...')
