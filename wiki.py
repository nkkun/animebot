from urllib.request import Request, urlopen
import requests
from bs4 import BeautifulSoup as soup
import re
url = 'https://www.chegg.com/homework-help/questions-and-answers/7-following-system-prepare-busdata-linedata-solver-provided-textbook-value-marked-per-unit-q26961941'
req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
page_soup = soup(webpage, "html.parser")
title = page_soup.find("img")
print(title)
imag=title.attrs['src']
print(imag)
r = requests.get(imag)
with open("que.png",'wb') as f:
    f.write(r.content)
