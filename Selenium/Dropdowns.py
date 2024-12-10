from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
import time

website = 'https://www.adamchoi.co.uk/overs/detailed'

# Set up Chrome options (if needed)
chrome_options = Options()
# chrome_options.add_argument('--headless')  # Uncomment if you want to run headless

# Set up ChromeDriver path using Service
service = Service(executable_path=ChromeDriverManager().install())

# Initialize the driver with the service
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get(website)

all_matches_button = driver.find_element(By.XPATH, '//label[@analytics-event="All matches"]')
all_matches_button.click()

# Dealing with dropdown menus
dropdown = Select(driver.find_element(By.ID, 'country'))
dropdown.select_by_visible_text('Spain')

# Dealing with the page loading the content
time.sleep(5)

matches = driver.find_elements(By.XPATH, '//tr[@class="ng-scope isNotHighlightedRow" or @class="ng-scope isHighlightedRow"]')

date =[]
home_team = []
score = []
away_team = []

for match in matches:
    date.append(match.find_element(By.XPATH, './td[1]').text) # Context //tr/td[1]
    home_team.append(match.find_element(By.XPATH, './td[2]').text)
    score.append(match.find_element(By.XPATH, './td[3]').text)
    away_team.append(match.find_element(By.XPATH, './td[4]').text)

# Validating data
print(all(len(lst) == len(date) for lst in[home_team, score, away_team]))

df = pd.DataFrame({'date':date, 'home_team':home_team, 'score':score, 'away_team':away_team})
# df.to_csv('matches_Spain.csv', index=False)
print(df)

# Pause the script until user presses Enter
input("Press Enter to close the browser...")
driver.quit()  # This will close the browser when you press Enter
