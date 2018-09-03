import os
import requests
from parsel import Selector


def get_request(url):

    text = requests.get(url).text
    return text


"""
    Main Method for running the logic
"""
def main():

    url = 'https://en.wikipedia.org/wiki/Main_Page'

    request_data = get_request(url)
    selector = Selector( text = request_data)
    print(len(request_data))
    #all_anchor_links = selector.css('a').xpath('@href').getall()
    #all_anchor_links = selector.css('a href*= http').xpath('//contains[@href, "https"]').getall()
    all_anchor_links = selector.css('a[href*= http]::attr(href)').getall()
    
    '''
    for link in all_anchor_links:
        print(link)
    '''
    #print(all_anchor_links[0])

"""
    Calling the main function
"""
if __name__ == '__main__':
    
    main()