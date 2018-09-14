
import json

class dataGetterClass(object):

    def __init__(self):
        pass
    
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
        color_list = []
        for item in response.xpath('//ul[contains(@class, "swatches color")]//a/@title').extract():
            color_list.append(item.split('-')[-1])
        
        return color_list

    def get_selected_color(self, response):
        return response.xpath(
                '//li[contains(@class, "attribute")]//span[contains(@class, "selected-value")]/text()'
        ).extract_first()
        

    def get_currency (self, response):
        # css -> div[class*="current"] *> span[class*="country-currency"]::text
        return response.xpath(
                    '//div[contains(@class, "current")]'
                + '//span[contains(@class, "country-currency")]/text()'
            ).extract_first()

    def get_price (self, response):
        # css -> div[class="product-price"] > span::text
        price = response.xpath(
                    '//div[contains(@class,"product-price")]/span/text()'
                ).extract_first()
        if price:
            return price.strip()
        return "0"

    def get_size (self, response):
        # css -> ul[class*="swatches size"] > li[class*="selected"] > a::text
        size = response.xpath(
                    '//ul[contains(@class, "swatches size")]'
                + '/li[contains(@class, "selected")]/a/text()'
                ).extract_first()
        
        if size:
            return size.rstrip()
        return "0"
    
    def get_prod_id(self, response):
        data = response.xpath(
            '//div[contains(@class, "js-product-content-gtm")]/@data-product-details'
            ).extract_first()
        data = json.loads(data)
        return data['idListRef12']
    
    def get_retailer_skus(self, response):
        data = response.xpath(
            '//div[contains(@class, "js-product-content-gtm")]/@data-product-details'
            ).extract_first()
        if data:
            data = json.loads(data)
            return data['idListRef6']
        else:
            return '0000'

    def get_shown_count(self, response):
        return int (
            response.xpath(
                '//div[contains(@class, "load-more-progress-label")]/span/text()'
                ).extract_first()
            )

    def get_next_count(self, response):
        return int (
                float(response.xpath(
                    '//div[contains(@class, "load-next-placeholder")]/@data-quantity'
                    ).extract_first()
                )
            )

    def get_url (self, response):
        return response.request.url