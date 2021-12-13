import requests
from bs4 import BeautifulSoup as bs

url = 'https://sci-hub.se/https://www.sciencedirect.com/science/article/pii/S2211285519301648'
print("Retrieving " + url)

html_text = requests.get(url).text
soup = bs(html_text, 'html.parser')
print(soup)
print('_'*10)
link = soup.findAll('button')[0]["onclick"]
link1 = link.split("'")
print(link1[1])
