# pip install:
# - bs4, requests, lxml (bs4 needs an external parser)


"""
Beautiful Soup: Steps before scraping a website

1. Fetch the pages (obtained a response object)

2. Page content: content = result.text

3. Create soup: soup = BeautifulSoup(content, "lxml")

"""

from bs4 import BeautifulSoup
import requests

# Finding elements with BeautifulSoup:
# soup.find(id = "specific_id") -> find() returns an element
# soup.find('tag', class_ = "class_name")
# soup.find_all("tag_name") -> find_all() returns a list

website = 'https://subslikescript.com/movie/Titanic-120338'
result = requests.get(website)
content = result.text

soup = BeautifulSoup(content, 'lxml')
# print(soup.prettify())

box = soup.find("article", class_ = "main-article")
title = box.find("h1").get_text()
transcript = box.find("div", class_ = "full-script").get_text(strip=True, separator='\n')
print(title)
print(transcript)

with open(f'{title}.txt', 'w') as file:
    file.write(transcript)