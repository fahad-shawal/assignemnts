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
from .dataGetter import dataGetterClass as dgc


class OrsayspiderSpider(scrapy.Spider):

    dgc_class = dgc()
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
            yield scrapy.Request(response.urljoin(link), callback=self.parse_product_page, dont_filter=True)
        
    
    def parse_product_page(self, response):
        product_page_links = response.xpath(
            '//a[contains(@class, "thumb-link")]/@href'
        ).extract()

        for link in product_page_links:
            yield response.follow(link, callback=self.parse_product_details, dont_filter=True)
            
        load_more = response.xpath(
            '//div[contains(@class, "load-next-placeholder")]'
            ).extract_first()

        if load_more:
            next_items = dgc.get_next_count(self.dgc_class, response)
            temp = str(response.request.url).split(sep='?sz=')
            link = temp[0] + '?sz='+ str(next_items)
            yield scrapy.Request(link, callback=self.parse_product_page)

    def parse_product_details(self, response):
        item = {
            'brand' : 'orsay',
            'care' : dgc.get_care(self.dgc_class, response),
            'category' : dgc.get_category(self.dgc_class, response),
            'discription' : dgc.get_discription(self.dgc_class, response),
            'image-urls' : dgc.get_image_urls(self.dgc_class, response),
            'retailer-skus'  : dgc.get_retailer_skus( self.dgc_class, response),
            'name' : dgc.get_name(self.dgc_class, response),
            'skus' : {
                dgc.get_prod_id(self.dgc_class, response) : {
                'color' : dgc.get_selected_color(self.dgc_class, response),
                'price' : dgc.get_price(self.dgc_class, response),
                'currency' : dgc.get_currency(self.dgc_class, response),
                'size' : dgc.get_size(self.dgc_class, response)
                }
            },
            'url' : dgc.get_url(self.dgc_class, response)
        }
        color_list_link = response.xpath(
                            '//ul[contains(@class, "swatches color")]//a/@href'
                        ).extract()
        
        if response.url in color_list_link:
            color_list_link.remove(response.url)
        
        if len(color_list_link) > 1:
            link = color_list_link.pop()         
            req = response.follow(link, callback=self.get_skues)
            req.meta['item'] = item
            req.meta['link'] = color_list_link
            yield req
        else:
            yield item

    def get_skues(self, response):
        item = response.meta['item']
        link = response.meta['link']
        item_details = {
            'color' : dgc.get_selected_color(self.dgc_class, response),
            'price' : dgc.get_price(self.dgc_class, response),
            'currency' : dgc.get_currency(self.dgc_class, response),
            'size' : dgc.get_size(self.dgc_class, response)
            }
        item['skus'][dgc.get_prod_id(self.dgc_class, response)] = item_details
        item['image-urls'] += dgc.get_image_urls(self.dgc_class, response)
        
        if link:
            url = link.pop()
            req = scrapy.Request(url, callback=self.get_skues)
            req.meta['item'] = item
            req.meta['link'] = link
            yield req
        else:
            yield item