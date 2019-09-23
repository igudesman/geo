from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from payments.models import Purchase, PurchaseItem
from rosreestr.models import SpatialDataItem
from django.contrib.auth.models import User
# from django.http import HttpResponse


def register(request):
	if request.user.is_authenticated:
		return redirect('profile')
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, 'Аккаунт для "{}" успешно создан!'.format(username))
			return redirect('/')
	else:
		form = UserRegisterForm()

	context = {'form': form}
	return render(request, 'users/register.html', context)


def get_user_purchase_history(user, max_items=1000):
    """
    Get the user's purchase history - all purchased items stored in the db for the given user.

    Parameters:
    user : User instance
        see users/models for reference
    max_items : int
        Maximum number of items to return; defaults to a large number (1000)

    Returns:
    list(PurchaseItem) - a flat list of all items purchased by the given user
    """
    purchases = Purchase.objects.filter(client_id=user.pk)
    purchases_sorted = sorted(purchases, key=lambda x: x.created_at, reverse=True)
    purchased_items = [PurchaseItem.objects.filter(purchase_id=purchase.pk) for purchase in purchases_sorted]
    return [item for sublist in purchased_items for item in sublist][:max_items]


@login_required
def profile(request):
    """"""
    user = User.objects.get(username=request.user.username)
    purchased_items = [{
        'name': SpatialDataItem.objects.get(pk=item.item_id.pk).name,
        'parcel_index': Purchase.objects.get(pk=item.purchase_id.pk).parcel_index,
        'purchased_at': Purchase.objects.get(pk=item.purchase_id.pk).created_at,
        'carrier': 'бумажный' if item.carrier == 'paper' else 'электронный',
        'status': 'Оформлен' if Purchase.objects.get(pk=item.purchase_id.pk).is_complete else 'Не оформлен'
        } for item in get_user_purchase_history(user)]

    context = {'purchased_items': purchased_items}
    return render(request, 'users/profile.html', context)
