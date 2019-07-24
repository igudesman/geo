import requests
from bs4 import BeautifulSoup

url = 'https://rosreestr.net/50:16:0103007:1279'
page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')

print(soup.find_all('div', class_='order3')[0].find_all('h2')[0].get_text())
# for line in soup.find_all('div', class_='test__data')[0].find_all('div'):
# 	print(line.get_text())