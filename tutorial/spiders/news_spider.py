import scrapy
import urlparse
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
import re

class NewsSpider(CrawlSpider):
    name = 'news'
    allowed_domains = ['soha.vn']
    start_urls = [
        'http://soha.vn/'
    ]
    # rules = (
    #     Rule(LinkExtractor(restrict_xpaths=("//a"), allow=(r".*\-\d{17}.htm",)), callback='parseCategory'),
    # )

    def parse(self, response):
        '''Parse main page and extract categories links.'''
        hxs = HtmlXPathSelector(response)
        urls = response.xpath('//*[@class="page-menu"]/div/a/@href').extract()
        for url in urls:
            url = urlparse.urljoin(response.url, url)
            # self.log('Found category url: %s' % url)
            yield Request(url, callback = self.parse_category)

    def parse_category(self, response):
        '''Parse category page and extract links of the items.'''
        hxs = HtmlXPathSelector(response)
        links = hxs.select("//a/@href").extract()
        for link in links:
            itemLink = urlparse.urljoin(response.url, link)
            self.log('For category: %s' % response.url)
            if re.search(".*\-\d{17}.htm", itemLink):
                self.log('Found item link: %s' % itemLink)
                yield Request(itemLink, callback = self.parse_item)
            else:
                self.log('Link failed: %s' % itemLink)
            # yield Request(itemLink, callback = self.parseItem)

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        title = hxs.select('//*[@class="news-title"]/text()').extract()
        # self.logger.info('Hi, this is an item page! %s', response.url)
        # item = scrapy.Item()
        # item['id'] = response.xpath('//*[@class="news-title"]/text()').get()
        # item['name'] = response.xpath('//*[@class="clearfix news-content"]/p/text()').get_all()
        # item['url'] = response.url
        self.log(title)
        # return item