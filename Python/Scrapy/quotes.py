# -*- coding: utf-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'  # name to genspider command
    allowed_domains = ['toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        self.log('I just Visited:' + response.url)
        
        # next page  fetch detail
        urls = response.css('div.qoute > span > a::attr(href').extract()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_detail)

        #simple fetching
        for quote in response.css('div.quote'):
            item = {
                    'author_name':quote.css('small.author::text').extract_first(),
                    'text':quote.css('span.text::text').extract_first(),
                    'tag':quote.css('a.tag::text').extract()
            }
            yield item

        # pagination
        next_page_url = response.css('li.next > a::attr(href)').extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_detail(self, response):
        yield{
            'name':response.css('h3.author_title::name').extract_first(),
            'birth_datz':response.css('span.author-born-date::text').extract_first(),
        }