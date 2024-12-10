import scrapy



class HandlingPaginationSpider(scrapy.Spider):
    name = "handling_pagination"
    allowed_domains = ["www.audible.com"]
    start_urls = ["https://www.audible.com/search"]

    # Changing User-Agent
    def start_requests(self):
        yield scrapy.Request(url='https://www.audible.com/search', callback=self.parse,
                       headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'})

    def parse(self, response):
        product_container = response.xpath('//*[@id="center-3"]/div/div/div/span[2]/ul/li')

        for product in product_container:
            book_author = product.xpath('.//div/div[1]/div/div[2]/div/div/span/ul/li[contains(@class, "authorLabel")]/span/a/text()').getall()
            book_title = product.xpath('.//div/div/div/div/div/div/span/ul/li/h3/a/text()').get()
            book_runtime = product.xpath('.//div/div[1]/div/div[2]/div/div/span/ul/li[contains(@class, "runtimeLabel")]/span/text()').get()

            yield {
                'title':book_title,
                'author':book_author,
                'runtime':book_runtime,
                'User-Agent':response.request.headers['User-Agent']
            }

        # Handling pagination
        # NOTE that: the website might forbid the use of robots....
        # Go to settings.py and add:
        # ROBOTSTXT_OBEY = False
        pagination = response.xpath('//ul[contains(@class, "pagingElements")]')
        next_page_url = pagination.xpath('.//li/span[contains(@class, "nextButton")]/a/@href').get()

        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            self.log(f"Next page URL: {next_page_url}")
            yield response.follow(url=next_page_url, callback=self.parse,
                                  headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'})
        else:
            self.log("No next page found.")

# Change the User-Agent
# 1. run: scrapy shell 'https://www.website.com/whatever'
# 2. run: request.headers > there you'll see a dictionary with a 'User-Agent':Scrapy
# 3. Go to your browser and inspect to open the dev tools
# 4. Into the dev tools, go to Network and reload the page
# 5. Filter by html and select any element
# 6. Scroll down to the Request Headers part
# 7. Find your User-Agent and copy it
