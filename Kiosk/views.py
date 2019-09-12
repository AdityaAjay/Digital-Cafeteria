from django.shortcuts import render
from decimal import Decimal
import boto3
from .models import Food, CurrentOrder
import sqlite3
from boto3.dynamodb.conditions import Key

items = Food.objects.all()
item_counter = {}
current_user = '5871857'
dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
balance_table = dynamodb.Table('Balance')
table = dynamodb.Table('Order')
resp = balance_table.query(KeyConditionExpression=Key('ID').eq('5871857'))
current_balance = (resp.get('Items'))[0].get('Balance')


def clear_aws():
    global current_balance
    global current_user
    current_user = ''
    current_balance = 0


def clear_cart():
    db = sqlite3.connect('/home/aditya/PycharmProjects/DigitalCafeteria/db.sqlite3')
    cursor = db.cursor()
    cursor.execute('DELETE from Kiosk_currentorder')
    db.commit()
    db.close()
    item_counter.clear()
    current_user_id = ''


def dynamo():
    pass


def send_paytm(request):
    # return HttpResponse("""<script>alert("Sent to Paytm")</script>""")
    pass


def landing_page(request):
    clear_cart()
    clear_aws()
    return render(request, 'Kiosk/landing.html')


def select_items(request):
    clear_cart()
    return render(request, 'Kiosk/order_page.html', {'items': items})


def item_added(request):
    global current_balance
    global current_user
    global dynamodb
    global table
    global balance_table
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
    # dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    # table = dynamodb.Table('Balance')
    # resp = table.query(KeyConditionExpression=Key('ID').eq('5871857'))
    # current_balance = (resp.get('Items'))[0].get('Balance')
    return render(request, 'Kiosk/order_page.html',
                  {'items': items, 'received_item': received_item, 'balance': current_balance})


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
    global current_balance
    global current_user
    global dynamodb
    global table
    global balance_table
    # total = request.POST.get('total')
    db = sqlite3.connect('/home/aditya/PycharmProjects/DigitalCafeteria/db.sqlite3')
    cursor = db.cursor()
    cursor.execute('''SELECT sum(price) FROM Kiosk_currentorder''')
    total = cursor.fetchone()
    total = total[0]
    cursor.execute('''SELECT order_id from Kiosk_ordernumber where id=?''', (1,))
    current_order = cursor.fetchone()
    current_order = current_order[0]
    current_order += 1
    cursor.execute('''UPDATE Kiosk_ordernumber SET order_id=? WHERE id=?''', (current_order, 1))
    db.commit()
    # dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    # table = dynamodb.Table('Order')
    total = Decimal(total)
    table.put_item(Item={"ID": current_order, "Enrolment": current_user, "Total": total})

    # # current_user = 5871857
    # balance_table = dynamodb.Table('Balance')
    # resp = balance_table.query(KeyConditionExpression=Key('ID').eq(current_user))
    # current_balance = (resp.get('Items'))[0].get('Balance')
    current_balance = str(current_balance)
    # return (added to aws success
    # fully)
    total = str(total)
    total = int(total)
    current_balance = int(current_balance)
    current_balance -= total
    balance_table.put_item(Item={"ID": '5871857', 'Balance': str(current_balance)})
    msg = "Order placed successfully"
    return render(request, 'Kiosk/landing.html', {'msg': msg})


def check_rfid(request):
    clear_aws()
    global current_balance
    global current_user
    global dynamodb
    global table
    global balance_table
    flag = False
    # dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    # table = dynamodb.Table('Balance')
    # ---------------------ADD RFID functionality here-----------------------
    current_user = '5871857'
    # -----------------------------------------------------------------------
    resp = balance_table.query(KeyConditionExpression=Key('ID').eq('5871857'))
    current_balance = (resp.get('Items'))[0].get('Balance')
    flag = True
    if flag:
        return render(request, 'Kiosk/order_page.html', {'items': items, 'balance': current_balance})
