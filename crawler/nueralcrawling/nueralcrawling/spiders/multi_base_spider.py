import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import pandas as pd
import os

df =  pd.read_csv(r'C:\college\web mining project\crawler2\crawler2\tourism_links.csv')
config_dict = dict()
for i in range(df.shape[0]):
    config_dict[i] = {}
    config_dict[i]['name'] = df.loc[i,'name']
    config_dict[i]['start_url'] = df.loc[i, 'url']
    config_dict[i]['rule'] = df.loc[i, 'rule']
# Configuration dictionary with base URLs and their corresponding rules
# config_dict = {
#     0: {'name': 'example1', 'start_url': 'http://example.com', 'rule': 'example'},
#     1: {'name': 'example2', 'start_url': 'http://example.org', 'rule': 'org'},
# }


class MultiBaseSpider(CrawlSpider):
    name = 'multibasespider'
    #allowed_domains = ['.com', '.in']  # Adjust as necessary

    # Initialize start_urls from the config dictionary
    start_urls = [config_dict[i]['start_url'] for i in config_dict]

    custom_settings = {
        'DEPTH_LIMIT': 2
    }

    def __init__(self, *args, **kwargs):
        super(MultiBaseSpider, self).__init__(*args, **kwargs)
        self.rules = []
        self.start_urls_config = {}

        # Create rules and set up start_urls_config
        for i in config_dict:
            rule = Rule(LinkExtractor(allow=config_dict[i]['rule']), callback='parse_item', follow=True)
            self.rules.append(rule)
            self.start_urls_config[config_dict[i]['start_url']] = config_dict[i]['name']

        self._compile_rules()

    def start_requests(self):
        for start_url in self.start_urls:
            feed_uri = f"{self.start_urls_config[start_url]}_output.csv"
            self.custom_settings['FEEDS'] = {
                feed_uri: {
                    'format': 'csv',
                    'encoding': 'utf8',
                    'store_empty': False,
                    'indent': 4,
                }
            }
            yield scrapy.Request(start_url, self.parse_start_url, meta={'feed_uri': feed_uri})

    def parse_start_url(self, response):
        self._compile_rules()
        return self.parse(response)

    def parse_item(self, response):
        yield {
            'url': response.url,
        }

    def parse(self, response):
        """Override parse method to dynamically set custom settings."""
        self.settings.attributes['FEEDS'].value = {
            response.meta['feed_uri']: {
                'format': 'csv',
                'encoding': 'utf8',
                'store_empty': False,
                'indent': 4,
            }
        }
        return self.parse_item(response)

