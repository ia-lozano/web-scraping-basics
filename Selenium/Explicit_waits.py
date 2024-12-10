from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

website = 'https://www.audible.com/search?language=en_US'

# Setting up Chrome options
chrome_options = Options()
# chrome_options.add_argument('--headless')  # Uncomment if you want to run headless

# Setting up Chrome path using Service
service = Service(executable_path=ChromeDriverManager().install())

# Initializing the Driver with the service
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get(website)

# Handling pagination
pagination = driver.find_element(By.XPATH, '//*[@id="pagination-a11y-skiplink-target"]/div/div[2]/div/span/ul')
pages = pagination.find_elements(By.TAG_NAME, 'li')
last_page = int(pages[-2].text)
current_page = 1

book_title = []
book_author = []
book_length = []

while current_page <= last_page:
    # time.sleep(2)
    container = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="center-3"]/div/div/div/span[2]/ul')))
    # container = driver.find_element(By.XPATH, '//*[@id="center-3"]/div/div/div/span[2]/ul')
    products = WebDriverWait(container, 5).until(EC.presence_of_all_elements_located((By.XPATH, './li/div/div/div/div/div/div/span/ul')))
    # products = container.find_elements(By.XPATH, './li/div/div/div/div/div/div/span/ul')

    for product in products:
        book_title.append(product.find_element(By.XPATH, "./li/h3[contains(@class, 'bc-heading')]/a").text)
        book_author.append(product.find_element(By.XPATH, "./li[3]/span/a").text)
        book_length.append(product.find_element(By.XPATH, "./li[contains(@class, 'runtimeLabel')]/span").text)

    current_page += 1

    try:
        next_page = driver.find_element(By.XPATH,
                                    '//*[@id="pagination-a11y-skiplink-target"]/div/div[2]/div/span/ul/li[6]/span/a')
        next_page.click()
    except:
        pass

driver.quit()

df = pd.DataFrame({'title':book_title, 'author':book_author, 'runtime':book_length})
df.to_csv('books_xplctWaits.csv', index=False)