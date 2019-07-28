from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, 'Account for "{}" successfully created!'.format(username))
			return redirect('/')
	else:
		form = UserRegisterForm()

	context = {
		'form': form
	}
	return render(request, 'users/register.html', context)
