from gc import callbacks

import scrapy
from scrapy import FormRequest


class LoginSpiderSpider(scrapy.Spider):
    name = "login_spider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/login"]

    def parse(self, response):
        csrf_token = response.xpath("//input[@name='csrf_token']/@value").get()
        yield FormRequest.from_response(
            response,
            formxpath = '//form',
            formdata = {
                'csrf_token':csrf_token,
                'username': 'admin',
                'password': 'addmin',
            },
            callback = self.after_login
        )

    def after_login(self, response):
        if response.xpath("//a[@href='/logout']/text()").get():
            print('Successfully logged in')
