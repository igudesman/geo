from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import Purchase, PurchaseItem
from rosreestr.models import SpatialDataItem
# from django.http import HttpResponse


@login_required
def checkout(request):
    """"""
    if request.method != 'POST':
        return redirect('/')
    # save the purchase to db
    user = User.objects.get(username=request.user.username)
    purchase = Purchase(client_id=user, parcel_index=request.POST['search'])
    purchase.save()
    # identify purchased items
    checkboxes = [key for key in request.POST.keys() if key.startswith('check_')]
    ordered_items = [item.split('_')[1:] for item in checkboxes]
    bill = {}
    for item in ordered_items:
        # save to db
        product, carrier = item
        purchaseItem = PurchaseItem(
            purchase_id=purchase,
            item_id=SpatialDataItem.objects.get(name=product),
            carrier=carrier
        )
        purchaseItem.save()
        # save to context
        price_attr = "price_{}".format(carrier)
        price = getattr(SpatialDataItem.objects.get(name=product), price_attr)
        carrier_translated = 'бумажный' if carrier == 'paper' else 'электронный'
        item_display = "{} ({} вид)".format(product, carrier_translated)
        bill[item_display] = price

    context = {
        'search': request.POST['search'],
        'bill': bill,
        'sum': sum(bill.values())
        }

    return render(request, 'payments/checkout.html', context)


@csrf_exempt
def alert(request):
    """"""
    if request.method != 'POST':
        return redirect('/')
    context = {'alert': 'Money!'}
    user = User.objects.get(email=request.POST['email'])
    purchase = Purchase.objects.get(client_id=user.pk, parcel_id=request.POST['label'])
    purchase.is_complete = True
    purchase.save()
    return render(request, 'payments/alert.html', context)