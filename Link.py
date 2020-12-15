from bs4 import BeautifulSoup
import requests

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0'}
try:
    link = requests.get('https://www.kmart.com.au/sitemap-core.xml',headers=headers)
    link = BeautifulSoup(link.text,'html.parser')
    link = link.findAll('loc')
    for lnk in link:
        print(lnk.text)
except Exception as e:
    print(e)

