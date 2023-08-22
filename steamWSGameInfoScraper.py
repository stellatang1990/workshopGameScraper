import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Returns a list of game URLs from the Steam Workshop
def getGameUrls(driver, totalNumPages):
    urls = list()

    for i in range(totalNumPages):
        while True:
            try:
                gameList = driver.find_elements(By.CLASS_NAME, "app")
                activePage = int(driver.find_element(By.CSS_SELECTOR, "#workshop_apps_links > span.workshop_apps_paging_pagelink.active").text)
                print("Current Page(IDE):", i + 1)
                print("Current Page(Browser):", activePage)
                
                urlList = list()
                # Get the URLs of every game in workshop
                for game in gameList:
                    urlList.append(game.get_attribute("onclick")[19:-1])
                print(len(urlList))
                # Click the next page button
                if activePage == i + 1:
                    urls.extend(urlList)
                    print(len(urls))
                    driver.find_element(By.ID, "workshop_apps_btn_next").click()
                    time.sleep(0.3)
                    break  # Exit the loop if the actions were successful
            except selenium.common.exceptions.StaleElementReferenceException:
                print("StaleElementReferenceException occurred. Refreshing elements and retrying.")
                continue  # Retry locating the elements

    return urls

# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

driver.get("https://steamcommunity.com/workshop/?browsesort=Alphabetical&browsefilter=Alphabetical&p=1")

# Get the total number of pages
totalNumPages = driver.find_elements(By.CLASS_NAME, "workshop_apps_paging_pagelink")[-1].text
print(totalNumPages)

gameUrls = getGameUrls(driver, totalNumPages)

# Print the final results
print(len(gameUrls))

# Quit the driver
driver.quit() 
