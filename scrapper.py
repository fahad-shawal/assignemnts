import os
import time
import requests
import threading
import concurrent.futures
from parsel import Selector
from concurrent.futures import ThreadPoolExecutor


def get_request(url):

    try:
        
        print("Process ID : ", os.getpid(), 
                "Featching Data from : ", url)
        text = requests.get(url).text

    except ConnectionError:
        
        print("No Connection Found!")
        text = ""
    
    else:
        
        return text


'''
    Method for Tasks Done Cocurrently using thread pool executer
'''
def concurren_execution(all_anchor_links,co_requests,max_url_visit):

    sum = 0
    print("\n--------- Start Process in concurrently ---------\n")
    
    start = time.time()
    with ThreadPoolExecutor(max_workers = 
                                co_requests) as executor:
                
            for link in all_anchor_links:
            
                future = executor.submit(get_request,link)
                print("--Got Data from : ", link, )
                sum += len(future.result())
    
    print("\n Time Taken is : ", round(time.time()-start, 2), "\n")
    
    return sum/max_url_visit


'''
    Method for Tasks Done in Parallel using Process pool executer
'''
def parallel_execution(all_anchor_links,co_requests,max_url_visit):

    sum = 0
    print("\n--------- Start Process in Parallel ---------\n")
    
    start = time.time()
    with concurrent.futures.ProcessPoolExecutor(max_workers = 
                                     co_requests) as executor:
        
        for link in all_anchor_links:
        
            future = executor.submit(get_request, link)
            print("--Got Data from : ", link)
            sum += len(future.result())
    
    print("\n Time Taken is : ", round(time.time()-start, 2), "\n")
        
    return sum/max_url_visit


"""
    Main Method for running the logic
"""
def main():

    try:
    
        co_requests = int( 
            input( "Enter the Number of CoCurrent Requests : ")
            )

        #download_delay = int(input("Input the Download dealy : "))
        
        max_url_visit = int( 
            input( "Input the Maximum Number of URLs to Visit : ")
            )
    
    except ValueError: 

        print( "****** Wrong Input, Must Input a Number ******")
    
    else:

        url = 'https://en.wikipedia.org/wiki/Main_Page'

        request_data = get_request( url)

        try:
            
            selector = Selector( text = request_data)
        
        except ValueError:
            
            print(" Tags Not Found. ")
        
        else:
            
            all_anchor_links = selector.css( 
                'a[href*= http]::attr(href)').getall()[0:max_url_visit]

            value = concurren_execution( all_anchor_links, 
                                            co_requests, 
                                            max_url_visit)
            
            print("Average Size of the page :", value)
            
            
            value = parallel_execution( all_anchor_links, 
                                            co_requests, 
                                            max_url_visit)
            
            print("Average Size of the page :", value)



"""         
    Calling the main function
"""
if __name__ == '__main__':
    
    main()