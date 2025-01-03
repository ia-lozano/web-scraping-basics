from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time


chrome_options = Options()
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(options=chrome_options, service=service)

name = 'Alejand81002615'
email = 't.g.alg@hotmail.com'
key = 'biohazard666'
topic = 'el bananero'

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
time.sleep(2)

# Executing JavaScript code as a string
# driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
for i in range(10):
    driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
    time.sleep(2)

# Scrolling to the bottom with a while loop
# NOTE: Be aware that the scrolling could be "infinite" with this method
'''
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight;)")
    time.sleep(5)
    new_height = driver.execute_script("return document.doby.scrollHeight")
    if new_height == last_height:
        break
    else:
        last_height = new_height
'''

time.sleep(10)