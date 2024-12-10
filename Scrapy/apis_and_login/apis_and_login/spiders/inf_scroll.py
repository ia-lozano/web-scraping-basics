import scrapy
import json

class InfScrollSpider(scrapy.Spider):
    name = "inf_scroll"
    allowed_domains = ["quotes.toscrape.com"]
    # As we are working with an API, get the following link from your browser:
    # for Google Chrome: inspect > network tab > Fetch/XHR > Headers tab > Copy Request URL
    start_urls = ["https://quotes.toscrape.com/api/quotes?page=1"]

    def parse(self, response):
        json_response = json.loads(response.body)
        # Use the name of the key that holds the data that you need to scrape
        quotes = json_response.get('quotes')
        for quote in quotes:
            yield {
                'author': quote.get('author').get('name'),
                'tags': quote.get('tags'),
                'quotes': quote.get('text'),
            }

        # Handling pagination
        has_next = json_response.get('has_next')
        if has_next:
            next_page_number = json_response.get('page') + 1
            yield scrapy.Request(
                url = f'https://quotes.toscrape.com/api/quotes?page={next_page_number}',
                callback = self.parse
            )