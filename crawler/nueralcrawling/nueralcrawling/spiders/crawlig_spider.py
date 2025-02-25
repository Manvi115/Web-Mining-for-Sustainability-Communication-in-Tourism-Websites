import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class MySpider(CrawlSpider):
    name = 'myspider'
    #allowed_domains = ['.]
    start_urls = ['https://wbtourismgov.in']

    rules = (
        Rule(LinkExtractor(allow='wbtourismgov'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        self.logger.info('Crawled URL: %s', response.url)
        yield {
            'url': response.url,
        }
