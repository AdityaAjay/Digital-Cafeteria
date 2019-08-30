from django.shortcuts import render
from django.http import HttpResponse
import boto3
from .models import Food, CurrentOrder
import sqlite3

items = Food.objects.all()
item_counter = {}


def dynamoOrder(request):
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('Order')


def send_paytm(request):
    pass


def landing_page(request):
    return render(request, 'Kiosk/landing.html')


def select_items(request):
    return render(request, 'Kiosk/order_page.html', {'items': items})


def item_added(request):
    db = sqlite3.connect('/home/aditya/PycharmProjects/DigitalCafeteria/db.sqlite3')
    cursor = db.cursor()
    received_id = request.POST.get('id')
    received_id = int(received_id)
    received_item = Food.objects.get(id=received_id)
    if received_id in item_counter:
        cursor.execute('''DELETE from Kiosk_currentorder WHERE food_item_id=?''',(received_id,))
        db.commit()
        item_counter.update({received_id: item_counter.get(received_id) + 1})
    else:
        item_counter.update({received_id: 1})
    count = item_counter.get(received_id)
    cursor.execute('''SELECT price from Kiosk_food WHERE id=?''', (received_id,))
    price = cursor.fetchone()
    cursor.execute('''INSERT INTO Kiosk_currentorder(food_item_id, quantity, price) VALUES (?,?,?)''',
                   (received_id, count, price[0]*count))
    db.commit()
    return render(request, 'Kiosk/order_page.html', {'items': items, 'received_item': received_item})


def clear_cart():
    db = sqlite3.connect('/home/aditya/PycharmProjects/DigitalCafeteria/db.sqlite3')
    cursor = db.cursor()
    cursor.execute('DELETE from Kiosk_currentorder')
    db.commit()
    item_counter.clear()
