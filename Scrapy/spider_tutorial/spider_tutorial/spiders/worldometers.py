import scrapy


class WorldometersSpider(scrapy.Spider):
    name = "worldometers"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["https://www.worldometers.info/world-population/population-by-country"]

    def parse(self, response):
        # title = response.xpath('//h1/text()').get()
        # countries = response.xpath('//td/a').getall()
        countries = response.xpath('//td/a')

        for country in countries:
            country_name = country.xpath('.//text()').get()
            link = country.xpath('.//@href').get()

            # For absolute links you could use this workaround (not recommended)
            # absolute_url = f'https://www.worldometers.info/{link}'

            # Another way to do this is:
            # absolute_url = response.urljoin(link)

            # yield scrapy.Request(url=absolute_url)

            # Best way to do this:
            # yield response.follow(url=link)

            yield {
                'country_name':country_name,
                'link':link,
        }
'''
            yield {
                'titles':title,
                'countries':countries,
        }
'''

# Once you've configured your parse() function and the yield dictionary
# Go to your Scrapy Env and run: scrapy crawl 'project name' (worldometers in this case)

# To activate the shell use the command: scrapy shell

