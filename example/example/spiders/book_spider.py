from unicodedata import name
from matplotlib.pyplot import cla
import scrapy
from scrapy.linkextractors import LinkExtractor
from example.items import BookItem
import logging


class BooksSpider(scrapy.Spider):

    name = 'books'

    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        # self.log("your log information")
        for sel in response.css('article.product_pod'):
            book = BookItem()
            name = sel.xpath('./h3/a/@title').extract_first()

            price = sel.css('p.price_color::text').extract_first()
            book['name'] = name
            book['price'] = price
            yield book

        # next_url = response.css(
        #     'ul.pager li.next a::attr(href)').extract_first()
        le = LinkExtractor(restrict_css='ul.pager li.next')
        links = le.extract_links(response)
        if links:
            next_url = links[0].url
            yield scrapy.Request(next_url, callback=self.parse)

        # if next_url:
        #     next_url = response.urljoin(next_url)
        #     yield scrapy.Request(next_url, callback=self.parse)
