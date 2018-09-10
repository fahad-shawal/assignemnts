# -*- coding: utf-8 -*-
#############################################################################
#                                                                           #
# This File is Created By : Fahad Shawal                                    #
# File Version : 1.0                                                        #
# Logic Followed : From url "http://www.orsay.com/de-de/produkte/" the      #
#                  parse() method will fetch the anchor links of all the    #
#                  sub category pages and pass each link to the method      #
#                  parse_page_product() where link of each product will     #
#                  be fetch and again each link will be passed to the       #
#                  parse_product_details() to extract the product info.     #
#                                                                           #
#                  If there are more products then are not shown on product #
#                  category page then a new link will be generated          #
#                  as link +  ?sz=[some-value] to get other remaining       #
#                  products.                                                #
#                                                                           #
#############################################################################

import scrapy
import logging


class OrsayspiderSpider(scrapy.Spider):
    name = 'orsayspider'
    allowed_domains = ['orsay.com']
    start_urls = ['http://www.orsay.com/de-de/produkte/']

    def parse(self, response):
        """
        links List to follow from main page to next 
        products page
        """
        main_page_links = response.xpath(
            '//a[contains(@class, "navigation-link level-3")]/@href'
                        ).extract()
        
        for link in main_page_links:
            yield response.follow(link, callback=self.parse_product_page)
    
    def parse_product_page(self, response):
        product_page_links = response.xpath(
            '//a[contains(@class, "thumb-link")]/@href'
        ).extract()

        for link in product_page_links:
            yield response.follow(link, callback=self.parse_product_details)
        
        shown = int (
            response.xpath(
                '//div[contains(@class, "load-more-progress-label")]/span/text()'
                ).extract_first()
            )
        total = int (
            response.xpath(
                '//div[contains(@class, "pagination")]/div//b/text()'
                ).extract_first()
            )
        
        if shown < total:
            
            temp = str(response.request.url).split(sep='?')
            link = temp[0] + '?sz=' + str(shown+72)
            logging.error(link)
            yield response.follow(link, callback=self.parse_product_page)

    def parse_product_details(self, response):
        yield {
            'brand' : 'orsay',
            'care' : self.get_care(response),
            'category' : self.get_category(response),
            'discription' : self.get_discription(response),
            'image-urls' : self.get_image_urls(response),
            'name' : self.get_name(response),
            'skus' : {
                'color' : self.get_color(response),
                'currency' : self.get_currency(response),
                'price' : self.get_price(response),
                'size' : self.get_size(response), 
            },
            'url' : self.get_url(response)
        }

    def get_care(self, response):
        # css -> div[class*="product-metrial"] > p::text 
        return response.xpath(
                    '//div[contains(@class, "product-material")]/p/text()'
                ).extract()
    
    def get_category(self, response):
        # css -> a[class="breadcrumb-element-link"]:nth-last-child(2) > span::text
        return response.xpath(
            '//a[contains(@class, "breadcrumb-element-link")][last()]/span/text()'
        ).extract_first()

    def get_discription (self, response):
        # css -> div[class*="with-gutter"]::text
        return response.xpath(
            '//div[contains(@class,"with-gutter")]/text()'
        ).extract()
    
    def get_image_urls (self, response):
        # css -> img[class*="productthumbnail"]::attr(src)
        return response.xpath(
            '//img[contains(@class,"productthumbnail")]/@src'
        ).extract()
    
    def get_name (self, response):
        # css -> h1[class="product-name"]::text
        return response.xpath(
                    '//h1[contains(@class,"product-name")]/text()'
                ).extract_first()

    def get_color (self, response):
        # css -> li[class="attribute"] > div > span:nth-last-child(1)::text
        return response.xpath(
                '//li[contains(@class, "attribute")]/div/span[last()]/text()'
                ).extract_first()

    def get_currency (self, response):
        # css -> div[class*="current"] *> span[class*="country-currency"]::text
        return response.xpath(
                  '//div[contains(@class, "current")]'
                + '//span[contains(@class, "country-currency")]/text()'
            ).extract_first()

    def get_price (self, response):
        # css -> div[class="product-price"] > span::text
        return str.strip(
            response.xpath(
                    '//div[contains(@class,"product-price")]/span/text()'
                ).extract_first()
            )

    def get_size (self, response):
        # css -> ul[class*="swatches size"] > li[class*="selected"] > a::text
        return str.strip(
            response.xpath(
                  '//ul[contains(@class, "swatches size")]'
                + '/li[contains(@class, "selected")]/a/text()'
                ).extract_first()
            )

    def get_url (self, response):
        return response.request.url

    