# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor  # 导入LinkExtractor，它位于scrapy.linkextractors模块。
from ..items import BookItem


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        le = LinkExtractor(restrict_css='article.product_pod h3')
        for link in le.extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse_book)
        #todo LinkExtractor每天看一下
        #创建一个LinkExtractor对象，使用一个或多个构造器参数描述提取规则，这里传递给restrict_css参数一个CSS选择器表达式。它描述出下一页链接所在的区域（在li.next下）。
        le = LinkExtractor(restrict_css='ul.pager li.next')
        #调用LinkExtractor对象的extract_links方法传入一个Response对象，该方法依据创建对象时所描述的提取规则，在Response对象所包含的页面中提取链接，最终返回一个列表，其中的每一个元素都是一个Link对象，即提取到的一个链接。
        links = le.extract_links(response)
        if links:
            #由于页面中的下一页链接只有一个，因此用'links[0]'获取Link对象，Link对象的url属性便是链接页面的绝对url地址（无须再调用response.urljoin方法），用其构造Request对象并提交。
            next_url = links[0].url
            yield scrapy.Request(next_url, callback=self.parse)

    def parse_book(self, response):
        book = BookItem()
        sel = response.css('div.product_main')
        book['name'] = sel.xpath('./h1/text()').extract_first().strip()
        book['price'] = sel.css('p.price_color::text').extract_first()
        book['review_rating'] = sel.css('p.star-rating::attr(class)') \
            .re_first('star-rating ([A-Za-z]+)')

        sel = response.css('table.table.table-striped')
        book['upc'] = sel.xpath('(.//tr)[1]/td/text()').extract_first()
        book['stock'] = sel.xpath('(.//tr)[last()-1]/td/text()') \
            .re_first('\((\d+) available\)')
        book['review_num'] = sel.xpath('(.//tr)[last()]/td/text()').extract_first()

        yield book
