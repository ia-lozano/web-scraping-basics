from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
from x_login import login_in

login_in('alejand81002615', 't.g.alg@hotmail.com', 'biohazard666' )

website = 'https://x.com/search?q=python&src=typed_query'

# Chrome options
chrome_options = Options()
# chrome_options.add_argument('--headless')

# Set up ChromeDriver path using Service
service = Service(executable_path=ChromeDriverManager().install())

# Initialize the driver with the service
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get(website)

time.sleep(5)

def get_tweet(element):
    try:
        user = element.find_element(By.XPATH, './/span[contains(text(), "@")').text
        article = element.find_element(By.XPATH, './/div[@lang="en"]').text
        tweets_data = [user, article]
    except:
        tweets_data = ['user-not-found', 'empty-article']
    return tweets_data

tweets = driver.find_elements(By.XPATH, '//article[@role="article"]')

users = []
articles = []

for tweet in tweets:
    tweet_list = get_tweet(tweet)
    users.append(tweet_list[0])
    articles.append(" ".join(tweet_list[1].split()))

driver.quit()
df_tweets = pd.DataFrame({'user':users, 'article':articles})
df_tweets.to_csv('tweets.csv', index = False)
