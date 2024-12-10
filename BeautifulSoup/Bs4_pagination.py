from bs4 import BeautifulSoup
import requests
import time

root = 'https://www.subslikescript.com'
website = f'{root}/movies_letter-A'
result = requests.get(website)
content = result.text
soup = BeautifulSoup(content, 'lxml')
# print(soup.prettify())

# Extracting from multiple pages
pagination = soup.find('ul', class_='pagination')
pages = pagination.find_all('li', class_='page-item')
last_page = pages[-2].text  # We don't need the last element of the pagination list

links = []
for page in range(1, int(last_page) + 1)[:2]:
    result = requests.get(f'{website}?page={page}')
    content = result.text
    soup = BeautifulSoup(content, 'lxml')

    box = soup.find('article', class_='main-article')
    # print(box)

# Iterating through the list returned from find_all to get all the links
    for link in box.find_all('a', href=True):
        links.append(link['href'])
        time.sleep(1)

    print(len(links))

    for link in links:
        try:
            # Extracting the full transcripts link per link
            result = requests.get(f'{root}/{link}')
            content = result.text
            soup = BeautifulSoup(content, 'lxml')
            # By coincidence, the root page and the transcript pages have the same box
            box = soup.find('article', class_='main-article')

            # Generating text files
            title = box.find('h1').get_text()
            transcript = box.find('div', class_='full-script').get_text(strip=True, separator='\n')
            '''
            try:
                with open(f'{title}.txt', 'w') as file:
                    file.write(transcript)

            except UnicodeError:
                print(f'UnicodeError in {title}.txt, file could not be generated')
            '''
        except:
            print(f'{website} link not working')

