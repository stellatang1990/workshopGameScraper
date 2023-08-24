import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Returns a list of game URLs from the Steam Workshop
def getGameUrls(driver):
    urls = list()
    
    # Get the total number of pages
    totalNumPages = int(driver.find_elements(By.CLASS_NAME, "workshop_apps_paging_pagelink")[-1].text)

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

# Returns a list of items from the game's page
def getItems(driver, tabUrl):
    items = list()
    #Navigate to the tab
    driver.get(tabUrl + '1')
    # Get the total number of pages
    try:
        totalNumPages = int(driver.find_elements(By.CLASS_NAME, 'pagelink')[-1].text)
        print(totalNumPages)
    except selenium.common.exceptions.NoSuchElementException:
        return items
    except IndexError:
        return items
    #loop through all pages
    for i in range(1, totalNumPages + 1):
        while True:
            try:
                urlList = driver.find_elements(By.CLASS_NAME, "ugc")
                if len(urlList) == 0:
                    print('No items found')
                    return items
                hold = list()
                for item in urlList:
                    hold.append(item.get_attribute("href"))
                print(len(hold))

                # time.sleep(0.3)
                items.extend(hold)
                print(len(items))
                print('going to page:',i + 1)
                driver.get(tabUrl + str(i + 1))
                break
            except selenium.common.exceptions.StaleElementReferenceExceptin:
                print("StaleElementReferenceException occurred. Refreshing elements and retrying.")
                continue  # Retry locating the elements

    return items

def sendToDB(gameName='N/A',gameId='N/A',gameLink='N/A',noItems='N/A',noRTUItems='N/A',itemName='N/A',createdBy='N/A',itemSize='N/A',postedTime='N/A',updatedTime='N/A',itemDesc='N/A',isCurated='N/A',isRTU='N/A',noUniqVis='N/A',noFavs='N/A',noSubs='N/A',reviews='N/A',df=pd.read_csv('workshopGameScraper/workshopDB.csv')):
    df = df.append({'gameName': gameName,'gameId':gameId,'gameLink':gameLink,'noItems':noItems,'noRTUItems':noRTUItems,'itemName':itemName,'createdBy':createdBy,'itemSize':itemSize,'postedTime':postedTime,'updatedTime':updatedTime,'itemDesc':itemDesc,'isCurated':isCurated,'isRTU':isRTU,'noUniqVis':noUniqVis,'noFavs':noFavs,'noSubs':noSubs,'reviews':reviews}, ignore_index=True)
    df.to_csv('workshopGameScraper/workshopDB.csv', index=False)

# Create a new instance of the Chrome driver
driver = webdriver.Chrome()
df = pd.read_csv('workshopGameScraper/workshopDB.csv')
driver.get("https://steamcommunity.com/workshop/?browsesort=Alphabetical&browsefilter=Alphabetical&p=1")


#gets the total number of games
totalNumGames = driver.find_element(By.XPATH, "//*[@id=\"workshop_apps_total\"]").text
#gets rid of the ',' in the number
totalNumGames = int(totalNumGames[0:1] + totalNumGames[2:])

# gameUrls = getGameUrls(driver, totalNumPages)
gameUrls = ['https://steamcommunity.com/app/1856190/workshop/']

for game in gameUrls:
    driver.get(game)
    browseTab = driver.find_element(By.XPATH, '//*[@id="responsive_page_template_content"]/div[1]/div[1]/div[3]/div/div[2]/div[2]/a')
    # Gets a list of all the links in the browse tab and grabs the ones that are links
    browseList = [x + '&p=' for i, x in enumerate(browseTab.get_attribute('data-dropdown-html').split('\"')) if i % 2 == 1]
    for tabLink in browseList:
        driver.get(tabLink)
        print(tabLink)  
        gameItems = getItems(driver, tabLink)
        print(gameItems)
        print(len(gameItems))
    



# Print the final results
# print(len(gameUrls))
# print(totalNumGames)

# Quit the driver
driver.quit() 
