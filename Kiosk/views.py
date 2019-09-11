from django.shortcuts import render
from django.http import HttpResponse
import boto3
from .models import Food, CurrentOrder
import sqlite3

items = Food.objects.all()
item_counter = {}


def clear_cart():
    db = sqlite3.connect('/home/aditya/PycharmProjects/DigitalCafeteria/db.sqlite3')
    cursor = db.cursor()
    cursor.execute('DELETE from Kiosk_currentorder')
    db.commit()
    db.close()
    item_counter.clear()


def dynamoOrder(request):
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('Order')
    table.put_item(Item={"Enrolment": 12, "Total": 100})


def send_paytm(request):
    # return HttpResponse("""<script>alert("Sent to Paytm")</script>""")
    pass


def landing_page(request):
    clear_cart()
    return render(request, 'Kiosk/landing.html')


def select_items(request):
    clear_cart()
    return render(request, 'Kiosk/order_page.html', {'items': items})


def item_added(request):
    db = sqlite3.connect('/home/aditya/PycharmProjects/DigitalCafeteria/db.sqlite3')
    cursor = db.cursor()
    received_id = request.POST.get('id')
    received_id = int(received_id)
    received_item = Food.objects.get(id=received_id)
    if received_id in item_counter:
        cursor.execute('''DELETE from Kiosk_currentorder WHERE food_item_id=?''', (received_id,))
        db.commit()
        item_counter.update({received_id: item_counter.get(received_id) + 1})
    else:
        item_counter.update({received_id: 1})
    count = item_counter.get(received_id)
    cursor.execute('''SELECT price from Kiosk_food WHERE id=?''', (received_id,))
    price = cursor.fetchone()
    cursor.execute('''SELECT name from Kiosk_food WHERE id=?''', (received_id,))
    received_name = cursor.fetchone()
    cursor.execute('''INSERT INTO Kiosk_currentorder(food_item_id, name, quantity, price) VALUES (?,?,?,?)''',
                   (received_id, received_name[0], count, price[0] * count))
    db.commit()
    db.close()
    return render(request, 'Kiosk/order_page.html', {'items': items, 'received_item': received_item})


def go_to_cart(request):
    cart_items = CurrentOrder.objects.all()
    db = sqlite3.connect('/home/aditya/PycharmProjects/DigitalCafeteria/db.sqlite3')
    cursor = db.cursor()
    cursor.execute('''SELECT sum(price) FROM Kiosk_currentorder''')
    total = cursor.fetchone()
    total = total[0]
    db.close()
    return render(request, 'Kiosk/cart.html', {'cart_items': cart_items, 'total': total})


def add_to_aws(request):
    total = request.POST.get('total')
    db = sqlite3.connect('/home/aditya/PycharmProjects/DigitalCafeteria/db.sqlite3')
    cursor = db.cursor()
    cursor.execute('''SELECT order_id from Kiosk_ordernumber where id=?''', (1,))
    current_order = cursor.fetchone()
    current_order = current_order[0]
    current_order += 1
    cursor.execute('''UPDATE Kiosk_ordernumber SET order_id=? WHERE id=?''', (current_order, 1))
    db.commit()
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('Order')
    table.put_item(Item={"ID": current_order, "Enrolment": "Guest", "Total": total})

    # return (added to aws successfully)
