import sqlite3
#
# db = sqlite3.connect('/home/aditya/PycharmProjects/DigitalCafeteria/db.sqlite3')
# cursor = db.cursor()
# cursor.execute('''SELECT sum(price) FROM Kiosk_currentorder''')
# total = cursor.fetchone()
# print(total[0])
import boto3

db = sqlite3.connect('/home/aditya/PycharmProjects/DigitalCafeteria/db.sqlite3')
cursor = db.cursor()
cursor.execute('''SELECT order_id from Kiosk_ordernumber where id=?''', (1,))
current_order = cursor.fetchone()
current_order = current_order[0]
print(current_order)
# cursor.execute('''DELETE from Kiosk_ordernumber WHERE id=?''', (1,))
# db.commit()
current_order += 1
# cursor.execute('''INSERT into Kiosk_ordernumber (id,order_id) VALUES (?,?)''', (1, current_order))
cursor.execute('''UPDATE Kiosk_ordernumber SET order_id=? WHERE id=?''', (current_order, 1))
db.commit()
dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table = dynamodb.Table('Order')
table.put_item(Item={"ID": current_order, "Total": 100})

# table.put_item(Item={"ID": current_order, "Enrolment": "Guest", "Total": 100})
