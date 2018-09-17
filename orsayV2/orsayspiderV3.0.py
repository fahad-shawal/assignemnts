# -*- coding: utf-8 -*-

#############################################################################
#                                                                           #
# This File is Created By : Fahad Shawal                                    #
# File Version : 2.0                                                        #
# Logic Followed : From url "http://www.orsay.com/de-de/produkte/" the      #
#                  parse() method will fetch the anchor links of all the    #
#                  products shown on this page. After that it will look     #
#                  for load more button if available then add 72 to the     #
#                  to the previous link and follow the page to get more     #
#                  product page.                                            #
#                                                                           #
#                  All the links will be stores in global list "urls_list"  #
#                  from where the show_list method will pop single url      #
#                  and extract the info from the page.                      #
#                                                                           #
#############################################################################

import scrapy
import logging
from .dataGetter import dataGetterClass as dgc
from scrapy.linkextractors import LinkExtractor


class Orsayspider2Spider(scrapy.Spider):
    
    dgc_class = dgc()
    name = 'orsayspider2'
    allowed_domains = ['orsay.com']
    start_urls = ['http://www.orsay.com/de-de/produkte/']
    urls_list = []
    items = {}
    counter = 0

    def parse(self, response):
        
        self.urls_list += response.xpath(
            '//a[contains(@class, "thumb-link")]/@href'
        ).extract()

        load_more = response.xpath(
            '//div[contains(@class, "load-next-placeholder")]'
            ).extract_first()

        if load_more:
            next_items = dgc.get_next_count(self.dgc_class, response)
            temp = str(response.request.url).split(sep='?sz=')
            link = temp[0] + '?sz='+ str(next_items)
            yield scrapy.Request(url=link, callback=self.parse)
        else:
            req = scrapy.Request(url='http://www.orsay.com'
                                        +self.urls_list.pop(), 
                                callback=self.show_list
                            )
            req.meta['item'] = {}
            yield req
            
    def show_list(self, response):

        items = response.meta['item']
        retailer_skus = dgc.get_retailer_skus( self.dgc_class, response)
        
        if retailer_skus in items:
            items[retailer_skus]['skus'].update(
                    { 
                    dgc.get_prod_id(self.dgc_class, response) : self.get_skus(response)
                }
            )

        elif retailer_skus != '0000':
            color_list_link = response.xpath(
                            '//ul[contains(@class, "swatches color")]//a/@href'
                        ).extract()
            
            if response.url in color_list_link:
                color_list_link.remove(response.url)

            self.urls_list += [
                temp.replace('http://www.orsay.com', '') 
                    for temp in color_list_link
                ]    
            self.urls_list = list(set(self.urls_list))
            self.counter +=1
            self.log('unique Items : '+str(self.counter))
            items.update({retailer_skus :  self.get_item(response)})
       
        else:
            pass
        
        #for link in self.urls_list:
        if self.urls_list:
            self.log(str(len(self.urls_list))+'\n')
            req = scrapy.Request(url='http://www.orsay.com'
                                        +self.urls_list.pop(), 
                                callback=self.show_list, 
                                dont_filter=True)
            req.meta['item'] = items
            yield req
        else:
            yield items
            self.log('\nTotal Items : '+str(len(items.items())))
        

    def get_skus(self, response):
        return {
            'color' : dgc.get_selected_color(self.dgc_class, response),
            'price' : dgc.get_price(self.dgc_class, response),
            'currency' : dgc.get_currency(self.dgc_class, response),
            'size' : dgc.get_size(self.dgc_class, response)
            }
    
    def get_item(self, response):
        return {
            'brand' : 'orsay',
            'care' : dgc.get_care(self.dgc_class, response),
            'category' : dgc.get_category(self.dgc_class, response),
            'discription' : dgc.get_discription(self.dgc_class, response),
            'image-urls' : dgc.get_image_urls(self.dgc_class, response),
            'retailer-skus' : dgc.get_retailer_skus(self.dgc_class, response),
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