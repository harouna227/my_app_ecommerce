from django.shortcuts import render


def shop(request):
    context = {}
    return render(request, 'myshop/shop.html')


def cart(request):
    context = {}
    return render(request, 'myshop/cart.html')


def checkout(request):
    context = {}
    return render(request, 'myshop/checkout.html')
