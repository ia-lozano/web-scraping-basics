from bs4 import BeautifulSoup
import requests
import time

root = 'https://www.subslikescript.com'
website = f'{root}/movies'
result = requests.get(website)
content = result.text
soup = BeautifulSoup(content, 'lxml')
# print(soup.prettify())

box = soup.find('article', class_ = 'main-article')
# print(box)

# Iterating through the list returned from find_all to get all the links
links = []
for link in box.find_all('a', href = True):
    links.append(link['href'])
    time.sleep(1)

print(len(links))

for link in links:
    # Extracting the full transcripts link per link
    website = f'{root}/{link}'
    result = requests.get(website)
    content = result.text
    soup = BeautifulSoup(content, 'lxml')
    # By coincidence, the root page and the transcript pages have the same box
    box = soup.find('article', class_ = 'main-article')

    # Generating text files
    title = box.find('h1').get_text()
    transcript = box.find('div', class_ = 'full-script').get_text(strip=True, separator='\n')



# I'm not generating all the .txt files everytime i run the script...
'''
    try:
        with open(f'{title}.txt', 'w') as file:
            file.write(transcript)

    except UnicodeError:
        print(f'UnicodeError in {title}.txt, file could not be generated')
'''