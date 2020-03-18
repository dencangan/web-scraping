"""
Updates new data on COVID19 in the UK
"""

import pandas as pd
from arctic import Arctic
import json
import os
from selenium import webdriver
import time

source_daily_confirmed = r"https://www.arcgis.com/sharing/rest/content/items/e5fd11150d274bebaaf8fe2a7a2bda11/data"
source_county = r"https://www.arcgis.com/sharing/rest/content/items/b684319181f94875a6879bbc833ca3a6/data"
source_nhsr = r"https://www.arcgis.com/sharing/rest/content/items/ca796627a2294c51926865748c4a56e8/data"

daily_file = "DailyConfirmedCases.xlsx"
county_file = "CountyUAs_cases_table.csv"
nhsr_file = "NHSR_Cases_table.csv"

# Change this to your Chrome default download directory
default_download_dir = r"C:\Users\Dencan Gan\Downloads"

files = [daily_file, county_file, nhsr_file]

# If you've already have the files, remove them
for file in files:
    file_dir = os.path.join(default_download_dir, file)

    if os.path.exists(file_dir):
        os.remove(file_dir)

# Starting up selenium...
driver = webdriver.Chrome()
driver.get(source_daily_confirmed)
driver.get(source_county)
driver.get(source_nhsr)
time.sleep(5)
driver.close()

# Check files are there
for file in files:
    file_dir = os.path.join(default_download_dir, file)

    if os.path.exists(file_dir):
        print(f"{file} downloaded successfully!")


# Data frames
df_daily = pd.read_excel(os.path.join(default_download_dir, daily_file))
df_county = pd.read_csv(os.path.join(default_download_dir, county_file))
df_nhsr = pd.read_csv(os.path.join(default_download_dir, nhsr_file))

# Arctic storage
# Secret credentials stored locally
mongo_credentials = json.load(open(r"C:\Users\Dencan Gan\Credentials\credentials.json"))["mongodb"]

# Connect to arctic database
a = Arctic(f"mongodb+srv://{mongo_credentials['username']}:{mongo_credentials['password']}@personaldatabase-rgdhs.azure.mongodb.net/test?retryWrites=true&w=majority")
covid19_lib = a["covid19"]

# Upload data
covid19_lib.write("daily_cases", df_daily)
covid19_lib.write("country_cases", df_county)
covid19_lib.write("nhsr_cases", df_nhsr)


