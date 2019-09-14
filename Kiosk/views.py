# The imports used in this module are mentioned below:
# [1] render is imported to render .html files from the templates folder and pass on some extra information like item list, etc.
# [2] decimal is being used to type cast the sum and upload to AWS
# [3] boto3 is the python3 package for AWS
# [4] Food and CurrentOrder are the database tables that are being used to maintain the order number and food items
# [5] sqlite3 is the python3 package for SQLite
# [6] fpdf is a python package to generate .pdf files
# [7] datetime is used to get the current date and time to print on the bill

from django.shortcuts import render
from decimal import Decimal
import boto3
from .models import Food, CurrentOrder
import sqlite3
from boto3.dynamodb.conditions import Key
from fpdf import FPDF
from datetime import datetime

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
    global item_counter
    db = sqlite3.connect('/home/aditya/PycharmProjects/DigitalCafeteria/db.sqlite3')
    cursor = db.cursor()
    cursor.execute('DELETE from Kiosk_currentorder')
    db.commit()
    db.close()
    item_counter.clear()


# -----------------
class PDF(FPDF):
    def header(self):
        # Logo
        self.image('/home/aditya/PycharmProjects/DigitalCafeteria/templates/Kiosk/logo.png', 10, 8, 33)
        self.ln(30)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


def get_time():
    hour = datetime.now().hour
    minute = datetime.now().minute
    second = datetime.now().second
    day = datetime.now().day
    month = datetime.now().month
    year = datetime.now().year
    return f"""{hour}:{minute}:{second}  {day}/{month}/{year}"""


def generator(items_local, price, quantity):
    pdf = PDF('P', 'mm', (76.2, 150))
    # modify according to page width. change size of logo image and reformat date time
    total = 0
    for individual_price in price:
        total += individual_price
    grand_total = f"Grand Total: Rs. {total}"
    # pdf = PDF()
    time = get_time()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Courier', 'BI', 12)
    pdf.cell(50, 8, time, 0, 1, 'C')
    pdf.set_font('Helvetica', 'I', 12)
    # init = 50
    pdf.ln(10)
    pdf.cell(65, 15, "Item          Quantity        Total", 1, 1, 'L')
    for i in range(len(items_local)):
        toWrite = f'''{items_local[i]} {quantity[i]} unit(s) Rs {price[i]}\n'''
        # pdf.write(init, toWrite)
        # init += 1
        pdf.cell(65, 15, toWrite, 1, 1, 'L')
    pdf.set_font('Courier', 'BU', 12)
    pdf.cell(65, 15, grand_total, 1, 1, 'L')
    #    pdf.write(init + 10, grand_total)
    pdf.output('bill.pdf', 'F')
    return True


# ----------------

def bill_generate():
    db = sqlite3.connect('/home/aditya/PycharmProjects/DigitalCafeteria/db.sqlite3')
    cursor = db.cursor()
    cursor.execute('''SELECT * from Kiosk_currentorder''')
    all_fetched_items = cursor.fetchall()
    # print(all_fetched_items)
    name_list = []
    price_list = []
    quantity_list = []
    for item in all_fetched_items:
        name_list.append(item[4])
        price_list.append(item[3])
        quantity_list.append(item[2])
    # print(name_list)
    # print(price_list)
    db.close()
    if generator(name_list, price_list, quantity_list):
        return True


def bill_print():
    # ---------------------
    #          add print functionality
    # ---------------------
    return True


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
    # to generate bill
    if bill_generate():
        clear_cart()
        # --------- Printer functionality ----------

        # -------------------------------------------
        if bill_print():
            return render(request, 'Kiosk/landing.html', {'msg': msg})


def check_rfid(request):
    clear_aws()
    clear_cart()
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


def logout(request):
    clear_cart()
    global balance_table
    clear_aws()
    global current_user
    global current_balance
    # to remove when RFID setup is complete
    current_user = '5871857'
    resp = balance_table.query(KeyConditionExpression=Key('ID').eq('5871857'))
    current_balance = (resp.get('Items'))[0].get('Balance')
    # to set to NULL after RFID setup is complete
    return render(request, 'Kiosk/landing.html')
