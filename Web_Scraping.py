"""@author: Shreyas_Chaudhari"""

import os
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

# Load configuration from JSON file
def get_config(file_path):
    with open(file_path, "r") as fp:
        config = json.load(fp)
    return config

# Get URLs of search results for a given company, select dropdown option for consignee search
def get_urls(driver, base_url, company):
    driver.get(base_url)    
    dropdown = Select(driver.find_element(By.NAME, "search-field-1"))
    dropdown.select_by_value('consignee')
    search_bar = driver.find_element(By.ID, "input-box")
    search_bar.send_keys(company)
    search_button = driver.find_element(By.ID, "search-button")
    search_button.click()
    # Extract search result URLs from page source
    search_items = driver.find_elements(By.CLASS_NAME, 'search-item')
    return [link.get_attribute('.href') for item in search_items for link in item.find_elements(By.TAG_NAME, 'a')]


# Get details from a given URL using specified field XPaths
def get_info(driver, url, fields):
    driver.get(url)
    return [driver.find_element(By.XPATH, xpath).get_attribute('innerHTML') if driver.find_elements(By.XPATH, xpath) else None for _, xpath in fields.items()]


# Main function to execute web scraping process,create Pandas dataframe from output list and export to CSV file.
def main():
    config = get_config(r'./Config.json')
    output = []
    # Initialize webdriver and loop through each company to scrape data
    with webdriver.Chrome() as driver:
        for company in config['companies']:
            urls = get_urls(driver, config['base_url'], company)[:config['no_of_urls']]
            for url in urls:
                details = get_info(driver, url, config['fields'])
                details.insert(0, company)
                output.append(details)
    output_df = pd.DataFrame(output,
                             columns=['searched Importer', 'Shipper', 'Consignee', 'Notify party', 'Bill Landing Number',
                                      'Vessel Name', 'Voyage No', 'Place of receipt', 'Port of Landing',
                                      'Port of Discharge', 'No of Pieces', 'Gross Weight', 'Arrival Date'])
    output_df.to_csv(os.path.join(r'C:\Users\Shreyas_Chaudhari\Assign_3', 'Assignment3.csv'), index=False)
    return output_df

if __name__ == '__main__':
    output = main()


#========================================================================================================================
"""{
    "base_url": "https://portexaminer.com/",
    "companies": [
                "Ford Motor Company",
                "Toyota",
                "Tesla Motors",
                "Mercedes-Benz",
                "General Motors"],
    "no_of_urls": 1,
    "fields":{
                "shipper" : "//*[@id='shipper']/div/div/h1/a/span",
                "consignee" :  "//*[@id='consignee']/div/div/h1/a/span",
                "notify_party" : "//*[@id='notify-1']/div/div/b/span",
                "bill_landing_no" :"//*[@id='details']/div/div/div/div[1]/div",
                "vessel_name":"//*[@id='details']/div/div/div/div[2]/div",
                "voyage_no":"//*[@id='details']/div/div/div/div[3]/div",
                "place_of_receipt":"//*[@id='details']/div/div/div/div[4]/div/span",
                "port_of_landing":"//*[@id='details']/div/div/div/div[5]/div/span",
                "port_of_discharge":"//*[@id='details']/div/div/div/div[6]/div/span",
                "no_of_pieces":"//*[@id='details']/div/div/div/div[8]/div",
                "gross_weight":"//*[@id='details']/div/div/div/div[9]/div/div",
                "arrival_date":"//*[@id='details']/div/div/div/div[11]/div/time"
                }
}"""
