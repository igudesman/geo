from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def checkout(request):
	return redirect('https://money.yandex.ru/to/410014034160798/99')