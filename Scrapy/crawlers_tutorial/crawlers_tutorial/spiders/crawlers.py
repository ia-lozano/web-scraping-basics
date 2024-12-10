import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

'''
How to get started with a crawler??
1. Open your terminal and write "scrapy genspider -l", this will print the types of templates for spiders.
2. Generate the template that you need: "scrapy genspider -t [templanteName] [spiderName] [domain i.e: website.com]"
'''

class CrawlersSpider(CrawlSpider):
    name = "crawlers"
    # Base domain
    allowed_domains = ["subslikescript.com"]
    # Full url of the website that you actually want to scrape
    #start_urls = ["https://subslikescript.com/"]

    # Scraping only movies with an X
    start_urls = ["https://subslikescript.com/movies_letter-X"]

    '''
    # Uncomment this code block to change User-Agent
    user_agent = 'User-Agent from your browser'
    def start_request(self):
        yield scrapy.Request(url='https://subslikescript.com/movies_letter-X', headers={
            'user-agent':self.user_agent, 
        })
    '''

    # TO CHANGE USER AGENT add proces_request='set_user_aget' to the first rule

    # You can do it with a regular expression
    # rules = (Rule(LinkExtractor(allow=r"/movie/[A-Za-z0-9_-]+-\d+"), callback="parse_item", follow=True),)

    # Or with xpath

    rules = (Rule(LinkExtractor(restrict_xpaths="//ul[@class='scripts-list']/li/a"), callback="parse_item", follow=True),
             Rule(LinkExtractor(restrict_xpaths="(//a[@rel='next'])[1]")),) # Handling pagination (2nd rule)

    '''
    # Uncomment this bloc to set User-Agent
    def set_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
        return request
    '''

    def parse_item(self, response):
        article = response.xpath("//article[@class='main-article']")
        transcript_list = article.xpath("./div[@class='full-script']/text()").getall()
        transcript_string = ' '.join(transcript_list)

        yield {
            'title':article.xpath("./h1/text()").get(),
            'plot':article.xpath("./p/text()").get(),
            # Uncomment to use with MongoDB
            #'script':article.xpath("./div[@class='full-script']/text()").getall(),
            'script':transcript_string,
            'url':response.url,
            #'user-agent':response.request.headers['User-Agent'],
        }

