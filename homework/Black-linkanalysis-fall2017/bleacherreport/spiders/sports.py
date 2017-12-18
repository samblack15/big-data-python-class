# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.exceptions import CloseSpider

class BleacherreportItem(scrapy.Item):
	parent_url = scrapy.Field()
	url = scrapy.Field()
	

class SportsSpider(CrawlSpider):
    name = 'sports'
    allowed_domains = ['www.bleacherreport.com']
    start_urls = ['http://www.bleacherreport.com/']
    
    rules = (
    Rule(LinkExtractor(allow=(), deny = "users"),
         callback="parse_item",
         follow=True),
    )

    page_count = 0

    def start_requests(self):
        requests = []
        for start_url in self.start_urls:
            requests.append(Request(url=start_url, headers={'Referer': start_url}))
        return requests

    def parse_item(self, response):
        if self.page_count > 30000:
            raise CloseSpider('Have scraped a sufficient number of pages')
        else:
            self.page_count += 1
        if self.page_count % 1000 == 0:
            print(self.page_count)
            print('URL: ' + url)
            print('Parent URL: ' + parent_url)
        url = response.url
        parent_url = response.request.headers.get('Referer', None).decode('utf-8')
        item = BleacherreportItem()
        item['parent_url'] = parent_url
        item['url'] = url
        yield item
