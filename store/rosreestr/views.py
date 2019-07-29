from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup
from django.contrib import messages

def object_info(request):
	context = {}
	if request.method == "POST":
		info = []
		data = []
		search = request.POST.get('search')
		search = search.replace(':', '-')
		if (search != '') and ('-' in search):

			data = parse(search)

		if data == []:
			messages.error(request, 'Kadastral number "{}" not found'.format(request.POST.get('search')))
			return redirect('/')

		for element in data:
			if ('Ранее учтенные' in element)  or ('устаревшей' in element) or ('Учтенные' in element):
				print(element)
				continue
			info.append(element)

		context = {
			'info': info
		}
	if context == {}:
		return redirect('search')

	return render(request, 'rosreestr/object_info.html', context)


def search(request):
	context = {}

	return render(request, 'rosreestr/search.html', context)

def not_found(request):
	context = {}

	return render(request, 'rosreestr/not_found.html', context)

def parse(cadastral_number):
	data = []
	url = 'https://rosreestr.net/kadastr/' + str(cadastral_number)
	page = requests.get(url)

	soup = BeautifulSoup(page.text, 'html.parser')

	try:
		if 'Страница не найдена' in soup.find_all('div', class_='order3')[0].find_all('h2')[0].get_text():
			print('error')
			return data
	except Exception:
		pass

	for line in soup.find_all('div', class_='test__data')[0].find_all('div'):
		data.append(line.get_text())

	return data
