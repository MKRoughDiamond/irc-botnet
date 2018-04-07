from bs4 import BeautifulSoup
import requests

def wiki_crawler(target):
    req = requests.get('https://en.wikipedia.org/w/index.php?search='+target)
    if req.status_code == 404:
        return None, None
    soup = BeautifulSoup(req.content,'html.parser')
    words = soup.find('p').getText().split(' ')
    if len(words) > 30:
        words = words[0:30]
    summary =  " ".join(words)
    if summary.find("may refer to:")!=-1:
        return req.url, None
    return req.url, summary
