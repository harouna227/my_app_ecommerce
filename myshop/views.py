import json
import datetime

from django.shortcuts import render
from django.http import JsonResponse

from .models import Product, Order, Customer, OrderItem, ShippingAddress

def shop(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        # print(customer)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shopping': False}
        cartItems = order['get_cart_items']


    products = Product.objects.all()
    context = {
        'products': products, 
        'cartItems': cartItems,
        
        }
    return render(request, 'myshop/shop.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        # print(customer)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shopping': False}
        cartItems = order['get_cart_items']
        
    context = {
        'items': items, 
        'order': order,
        'cartItems':cartItems,
        }
    return render(request, 'myshop/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        #Create empty cart for now for non-logged in user
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    context = {
        'products':products, 
        'cartItems':cartItems,
        'order': order,
        'items': items
        }

    return render(request, 'myshop/checkout.html', context)

def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    # print('productid:', productId)
    # print('action:', action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
            
    return JsonResponse('Item was added', safe=False)

def process_order(request):
    transasction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transasction_id
        
        if total == float(order.get_cart_total):
            order.complete = True
        order.save()
        
        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
    else:
        print("l'utilisateur n'est connecté")
        
    return JsonResponse('Paiment est soumi...', safe=False)