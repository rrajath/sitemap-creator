'''
Created on Aug 8, 2013

@author: rajath
'''
import urllib
from BeautifulSoup import BeautifulSoup
from MultiThread import MultiThreadIt
from multiprocessing.pool import ThreadPool

MAIN_URL = r'http://daringfireball.net'

relevant_urls = []
result_urls = []
url_dict = {}
url_list = []
links = []

# Remove unnecessary URLs. Keep only those URLs that are in the same domain.
# Discard rest of the URLs.
def cleanup_urls(relevant_urls):
    for url in relevant_urls:
        if url.startswith('/'):
            url = MAIN_URL + url
        elif '#' in url or not url.startswith(MAIN_URL):
            continue
        result_urls.append(url)
    return list(set(result_urls))

# Given a URL, fetch all the links in that web page.
def get_links(url):
    global href
    print "Entered Get_Links()"
    data = urllib.urlopen(url).read()
    soup = BeautifulSoup(data)
#     urls = soup.findAll('a')
    for url in soup('a'):
        href = str(url['href'])
        if href.startswith('/'):
            href = MAIN_URL + href
        elif '#' in href or not href.startswith(MAIN_URL):
            continue
        result_urls.append(href)
        
#         url = str(url)
#         attr = 'href="'
#         href = url[url.find(attr) + len(attr) : url.find('"', url.find(attr) + len(attr))]
#         href = str(href)
#         links.append(href)
    return result_urls

# This function gets the list of out-links for a URL.
# For each link, it makes a list of out-links and add them to dictionary.
def extract_links(url):
    global href
    print "Entered Extract_Links()"
    try:
        # Get all links
        links = get_links(url)
        # Clean up all the links
        clean_urls = links # cleanup_urls(links)
        url_dict[url] = clean_urls
        for link in clean_urls:
            if url_dict.has_key(link):
                continue
            else:
                extract_links(link)
    except KeyError:
        print href
    print "Completed..."
    return url_dict

# extract_links(MAIN_URL + '/')
url_dicts = ThreadPool(32).apply_async(extract_links, (MAIN_URL + '/',)).get()

print len(url_dict)
print url_dict