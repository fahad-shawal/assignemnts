import os
import requests
from requests.exceptions import *
from parsel import Selector
from concurrent.futures import ThreadPoolExecutor
import threading


def get_request(url):

    try:
        print("Featching Data from : ", url)
        text = requests.get(url).text
    
    except ConnectionError:
        print("No Connection Found!")
        text = ""
    
    else:
        return text


"""
    Main Method for running the logic
"""
def main():

    try:
    
        co_requests = int(input("Enter the Number of CoCurrent Requests : "))
        download_delay = int(input("Input the Download dealy : "))
        max_url_visit = int(input("Input the Maximum Number of URLs to Visit : "))
    
    except ValueError: 

        print("****** Wrong Input, Must Input a Number ******")
    
    else:

        url = 'https://en.wikipedia.org/wiki/Main_Page'

        request_data = get_request(url)

        try:
            selector = Selector( text = request_data)
        
        except ValueError:
            print(" Tags Not Found. ")
        
        else:
            all_anchor_links = selector.css('a[href*= http]::attr(href)').getall()[0:max_url_visit]
            sum = 0            
            
            with ThreadPoolExecutor(max_workers = co_requests) as executor:
                for link in all_anchor_links:
                    #sum += len(get_request(link))
                    future = executor.submit(get_request,link)
                    print("Got Data from : ", link)
                    sum += len(future.result())
        
            print("Average Size of the page :", sum/max_url_visit)
            #print(all_anchor_links[0])

"""
    Calling the main function
"""
if __name__ == '__main__':
    
    main()