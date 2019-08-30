import sqlite3

db = sqlite3.connect('/home/aditya/PycharmProjects/DigitalCafeteria/db.sqlite3')
cursor = db.cursor()
cursor.execute('''SELECT sum(price) FROM Kiosk_currentorder''')
total = cursor.fetchone()
print(total[0])
