# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from..items import ExamplesItem

class ExamplesSpider(scrapy.Spider):
    name = 'examples'
    allowed_domains = ['matplotlib.org']
    start_urls = ['http://matplotlib.org/examples/index.html']

    def parse(self, response):
        le = LinkExtractor(restrict_xpaths='//div[@class="toctree-wrapper compound"]', deny='/index.html$')
        print(len(le.extract_links(response)))
        for link in le.extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse_example)

    def parse_example(self, response):
        href = response.xpath('//div[@class="section"]/p/a/@href').extract_first()
        url = response.urljoin(href)
        example = ExamplesItem()
        example['file_urls'] =[url]
        return example