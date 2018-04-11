from bs4 import BeautifulSoup
import requests

def wiki_crawler(target):
    req = requests.get('https://en.wikipedia.org/w/index.php?search='+target)
    if req.status_code == 404:
        return None, None
    soup = BeautifulSoup(req.content,'html.parser')
    isSearch=None
    if soup.find('h1') is not None:
        isSearch = soup.find('h1').getText()
    if isSearch is not None and isSearch.find("Search results")!=-1:
        req = requests.get('https://en.wikipedia.org/wiki/'+target)
        soup = BeautifulSoup(req.content,'html.parser')
        isSearch = soup.find('h1').getText()
        if req.status_code ==404:
            return None,None
        if isSearch is not None and isSearch.find("Bad title")!=-1:
            return None,None
    if 'refer to' in soup.find('p').getText() and soup.find('ul') is not None:
        return req.url, None
    words = soup.find('p').getText().split(' ')
    if len(words) > 30:
        words = words[0:30]
    summary =  " ".join(words)
    return req.url, summary
