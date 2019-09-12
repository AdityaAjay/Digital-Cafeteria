import sqlite3

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
print(name_list)
print(price_list)
print(quantity_list)
db.close()
