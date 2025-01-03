# pip install selenium
# pip install webdriver_manager
# pip install 'urllib3<2.0'
# pip install pandas

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Chrome options
chrome_options = Options()
# chrome_options.add_argument('--headless')

# Set up ChromeDriver path using Service
service = Service(executable_path=ChromeDriverManager().install())

# Initialize the driver with the service
driver = webdriver.Chrome(service=service, options=chrome_options)

def get_tweet(element):
    try:
        user = element.find_element(By.XPATH, './/span[contains(text(), "@")]').text
        article = element.find_element(By.XPATH, './/div[@data-testid="tweetText"]').text
        tweets_data = [user, article]
    except:
        tweets_data = ['user-not-found', 'empty-article']
    return tweets_data

def login_in(name, email, key, topic):
    """
    :param name: tweeter username
    :param email: email, just in case the page asks for verification (could also be the phone number)
    :param key: tweeter password
    :param topic: topic of interest to scrape
    :return: pandas dataframe
    """
    website = 'https://x.com/i/flow/login'
    driver.get(website)
    driver.maximize_window()
    time.sleep(2)
    # Login in
    username = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@autocomplete="username"]'))
    )
    username.send_keys(name)
    next_button = driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]')
    next_button.click()
    time.sleep(5)

    # If X asks for verification:
    verify = driver.find_elements(By.XPATH,'//input[@data-testid="ocfEnterTextTextInput"]')
    if verify:
        verify = driver.find_element(By.XPATH,'//input[@data-testid="ocfEnterTextTextInput"]')
        verify.send_keys(email)
        verify_button = driver.find_element('//button[@data-testid="ocfEnterTextNextButton"]')
        verify_button.click()
        time.sleep(5)

    password = driver.find_element(By.XPATH, '//input[@autocomplete="current-password"]')
    password.send_keys(key)

    login_button = driver.find_element(By.XPATH, '//button[@data-testid="LoginForm_Login_Button"]')
    login_button.click()

    time.sleep(5)
    search_bar = driver.find_element(By.XPATH, '//input[@role="combobox"]')
    search_bar.send_keys(topic)
    time.sleep(2)

    select_first = driver.find_element(By.XPATH, '//div[@data-testid="typeaheadResult"][1]')
    select_first.click()

    time.sleep(5)
    tweets = driver.find_elements(By.XPATH, '//article[@role="article"]')

    users = []
    articles = []
    tweet_ids = set()

    scrolling = True
    while scrolling:
        tweets = driver.find_elements(By.XPATH, '//article[@role="article"]')
        for tweet in tweets:
            tweet_list = get_tweet(tweet)
            tweet_id = ''.join(tweet_list)
            if tweet_id not in tweet_ids:
                tweet_ids.add(tweet_id)
                users.append(tweet_list[0])
                articles.append(" ".join(tweet_list[1].split()))


        driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
        time.sleep(2)

        # Terminating while loop after a fixed number of scraped tweets
        if len(tweet_ids) >= 100:
            scrolling = False

    driver.quit()
    df_tweets = pd.DataFrame({'user': users, 'article': articles})
    df_tweets.to_csv('tweets.csv', index=False)
    return df_tweets


login_in('', '', '', '')
