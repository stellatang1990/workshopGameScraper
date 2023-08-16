#desc: This script will scrape the steam store for game information
import selenium
from selenium import webdriver

# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

driver.get("https://steamcommunity.com/workshop/")
appRows = driver.find_element(By.CLASS_NAME, "workshopAppsRow")
print(appRows)
