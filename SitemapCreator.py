'''
Created on Aug 8, 2013

@author: rajath
'''
import urllib
from BeautifulSoup import BeautifulSoup

MAIN_URL = r'http://daringfireball.net'

relevant_urls = []
result_urls = []
url_dict = {}

def cleanup_urls(relevant_urls):
    for url in relevant_urls:
        if url.startswith('/'):
            url = MAIN_URL + url
        elif '#' in url or not url.startswith(MAIN_URL):
            continue
        result_urls.append(url)
    return list(set(result_urls))
    
url_list = []

links = []

def get_links(url):
    data = urllib.urlopen(url).read()
    soup = BeautifulSoup(data)
    urls = soup.findAll('a')
    for url in urls:
        url = str(url)
        attr = 'href="'
        href = url[url.find(attr) + len(attr) : url.find('"', url.find(attr) + len(attr))]
        href = str(href)
        links.append(href)
    return links

def extract_links(url):
#     open_url
#     get all links
    links = get_links(url)
#     clean up all the links
    clean_urls = cleanup_urls(links)
    url_dict[url] = clean_urls
    for link in clean_urls:
        if url_dict.has_key(link):
            continue
        else:
            extract_links(link)
    return

extract_links(MAIN_URL + '/')

print len(url_dict)
print url_dict