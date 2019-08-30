# import sqlite3
#
# #
# # received_id = 1
# db = sqlite3.connect('/home/aditya/PycharmProjects/DigitalCafeteria/db.sqlite3')
# cursor = db.cursor()
# # cursor.execute('''SELECT price from Kiosk_food WHERE id=?''', (received_id,))
# # price = cursor.fetchone()
# # cursor.execute('''INSERT INTO Kiosk_currentorder(food_item_id, quantity, price) VALUES (?,?,?)''',
# #                (received_id, 2, price[0]))
# # db.commit()
# # print(type(price))
# cursor.execute('DELETE from Kiosk_currentorder')
# db.commit()

i={2:4}
if 1 in i:
    print("hello")