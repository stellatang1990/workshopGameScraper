import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

driver.get("https://steamcommunity.com/workshop/?browsesort=Alphabetical&browsefilter=Alphabetical&p=1")

# Get the total number of pages
totalNumPages = driver.find_elements(By.CLASS_NAME, "workshop_apps_paging_pagelink")[-1].text
print(totalNumPages)

gameUrls = list()

# Iterate through all pages 
for i in range(1, int(totalNumPages)):
    time.sleep(0.1)

    while True:
        try:
            gameList = driver.find_elements(By.CLASS_NAME, "app")
            print("Page:", i)
            for game in gameList:
                gameUrls.append(game.get_attribute("onclick")[19:-1])
            print(len(gameUrls))

            # Click the next page button
            if i != int(totalNumPages) and len(gameList) % 8 == 0:
                driver.find_element(By.ID, "workshop_apps_btn_next").click()

            break  # Exit the loop if the actions were successful

        except selenium.common.exceptions.StaleElementReferenceException:
            print("StaleElementReferenceException occurred. Refreshing elements.")
            continue  # Retry locating the elements

# Print the final results
print(len(gameUrls))
print(gameUrls)

# Quit the driver
driver.quit() 
