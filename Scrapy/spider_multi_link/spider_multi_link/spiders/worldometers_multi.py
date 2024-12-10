import scrapy


class WorldometersMultiSpider(scrapy.Spider):
    name = "worldometers_multi"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["https://www.worldometers.info/world-population/population-by-country"]

    def parse(self, response):
        countries = response.xpath('//td/a')

        for country in countries:
            country_name = country.xpath('.//text()').get()
            link = country.xpath('.//@href').get()

            yield response.follow(url=link, callback=self.parse_country, meta={'country':country_name})

    def parse_country(self, response):
        country = response.request.meta['country']
        rows = response.xpath('//table[@class="table table-striped table-bordered table-hover table-condensed table-list"]/tbody/tr')
        for row in rows:
            year = row.xpath('.//td[1]/text()').get()
            population = row.xpath('.//td[2]/strong/text()').get()

            yield {
                'country': country,
                'year': year,
                'population': population,
            }

    # To write the info as a json file: scrapy crawl worldometers -o wpopulation.json