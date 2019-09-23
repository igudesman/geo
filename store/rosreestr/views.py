import requests
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.utils import timezone
from .models import SpatialDataItem


def parse(cadastral_number, request):
	url = 'https://rosreestr.net/kadastr/' + cadastral_number.replace(':', '-')
	res = requests.get(url)
	if res.status_code == 404:
	    return None

	soup = BeautifulSoup(res.text, 'html.parser')
	fields = soup.select_one('.test__data')('div')
	data = {}
	keywords = ('Адрес полный', 'Адрес по документам', 'Площадь')
	for field in fields:
	    text = field.get_text()
	    split = text.split(':', 1)
	    if split[0] == 'Адрес полный':
	        data['address_full'] = split[1]
	    elif split[0] == 'Адрес по документам':
	        data['address_doc'] = split[1]
	    elif split[0] == 'Площадь':
	        data['area'] = split[1].split('м')[0]
	    if len(data) == len(keywords):
	        break

	return data


@login_required
def object_info(request):
    if request.method != 'POST':
        return redirect('/')

    search = request.POST.get('search')
	# отсеить номера которые заведомо не могут быть действительными
    if ':' not in search:
	    messages.error(request, 'Неверный формат кадастрового номера! Пожалуйста, проверьте написание.')
	    return redirect('/')

    info = parse(search, request)
    if not info:
	    messages.error(request, 'Введенный кадастровый номер не существует! Пожалуйста, проверьте написание.')
	    return redirect('/')

    items = SpatialDataItem.objects.all()
    price_list = [{
	    'name': item.name,
	    'price_paper': item.price_paper,
	    'price_digital': item.price_digital
	    } for item in items]

    context = {
		'info': info,
		'search': search,
		'price_list': price_list
	}

    return render(request, 'rosreestr/object_info.html', context)


# def gallery(request):
#     """Showcase available products."""
#     context = {'spatial_data_items': list('abc')}
#     return render(request, 'rosreestr/gallery.html', context)

def search(request):
	context = {}
	return render(request, 'rosreestr/search.html', context)

def not_found(request):
	context = {}
	return render(request, 'rosreestr/not_found.html', context)


class SpatialDataItemListView(ListView):
    """"""
    model = SpatialDataItem
    template_name = 'rosreestr/gallery.html'
    # paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

