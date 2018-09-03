import os
import requests
from parsel import Selector


def get_request(url):

    text = requests.get(url)

    return text.text


def main():

    url = 'http://rogerdudler.github.io/git-guide/'

    request_data = get_request(url)

    print(request_data)

if __name__ == '__main__':
    
    main()