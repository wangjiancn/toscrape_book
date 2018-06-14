# -*- coding: utf-8 -*-
import scrapy
from ..items import BookItem


class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ["books.toscrape.com"]
    start_urls = ['http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html']
    # start_urls = ['https://search.jd.com/Search?keyword=%E8%B6%85%E6%9E%81%E6%9C%AC&enc=utf-8&wq=%E8%B6%85%E6%9E%81%E6%9C%AC']

    def parse(self, response):
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
        # goods = jdItem()
        # for good in response.css('div.gl-warp'):
        # goods['price']= response.xpath(
        #     '//*[@id="default"]/div/div/div/div/section/div[2]/ol/li[1]/article/div[2]/p[1]/text()').extract()
        # goods['name'] = response.xpath('//*[@id="default"]/div/div/div/div/section/div[2]/ol/li[1]/article/h3/a/text()').extract()
        # jd['comments'] = response.xpath('//*[@id="J_comment_6405102"]').extract()
        # jd['boss'] = response.xpath('//*[@id="J_pro_6405102"]/i').extract()
