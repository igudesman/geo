import requests
from bs4 import BeautifulSoup

url = 'https://rosreestr.net/kadastr/40-28-010805-8'
page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')
for line in soup.find_all('div', class_='test__data')[0].find_all('div'):
	print(line.get_text())