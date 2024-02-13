from django.shortcuts import render

from .models import Product

def shop(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'myshop/shop.html', context)


def cart(request):
    context = {}
    return render(request, 'myshop/cart.html')


def checkout(request):
    context = {}
    return render(request, 'myshop/checkout.html')
