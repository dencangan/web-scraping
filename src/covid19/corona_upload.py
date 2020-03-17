import pandas as pd
import os
from selenium import webdriver
import time

source_daily_confirmed = r"https://www.arcgis.com/sharing/rest/content/items/e5fd11150d274bebaaf8fe2a7a2bda11/data"
source_county = r"https://www.arcgis.com/sharing/rest/content/items/b684319181f94875a6879bbc833ca3a6/data"
source_nhsr = r"https://www.arcgis.com/sharing/rest/content/items/ca796627a2294c51926865748c4a56e8/data"

daily_file = "DailyConfirmedCases.xlsx"
county_file = "CountyUAs_cases_table.csv"
nhsr_file = "NHSR_Cases_table.csv"
default_download_dir = r"C:\Users\Dencan Gan\Downloads"

files = [daily_file, county_file, nhsr_file]

for file in files:
    file_dir = os.path.join(default_download_dir, file)

    if os.path.exists(file_dir):
        os.remove(file_dir)

driver = webdriver.Chrome()
driver.get(source_daily_confirmed)
driver.get(source_county)
driver.get(source_nhsr)
time.sleep(5)
driver.close()

for file in files:
    file_dir = os.path.join(default_download_dir, file)

    if os.path.exists(file_dir):
        print(f"{file} downloaded successfully!")



