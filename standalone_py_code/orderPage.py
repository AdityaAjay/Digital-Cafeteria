import boto3
from tkinter import *
import csv


def startOrder(enrolment):
    order_count = 0
    total = 0
    with open('count.csv', newline='') as File:
        reader = csv.reader(File)
        for row in reader:
            order_count = int(row[0])
    order_window = Tk()
    order_window.geometry('1366x768')
    order_window.title("Select the items you'd like to order")
    item_list = Listbox(order_window, font=("Ubuntu", 40))
    item_list.insert(1, "Aaluu")
    item_list.pack()
    order_window.mainloop()   # fix here
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('Order')
    # resp = table.get_item(Key={"ID": 1})
    # print(resp['Item'])
    with open('current order.csv', 'w') as File:
        writer = csv.writer(File)

    # when order complete
    table.put_item(Item={"ID": order_count + 1, "Enrolment": enrolment, "Total": total})
    with open('count.csv', 'w') as File:
        l = [str(order_count + 1)]
        writer = csv.writer(File)
        writer.writerows(l)
    order_window.destroy()
    return True
