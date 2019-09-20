from fpdf import FPDF
from datetime import datetime
import sqlite3

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


def generator(items, price, quantity):
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
    pdf.set_text_color(0, 0, 102)
    pdf.set_font('Courier', 'BI', 12)
    pdf.cell(50, 8, time, 0, 1, 'C')
    pdf.set_font('Helvetica', 'I', 12)
    init = 50
    pdf.ln(10)
    pdf.cell(65, 15, "Item          Quantity        Total", 1, 1, 'L')
    for i in range(len(items)):
        toWrite = f'''{items[i]} {quantity[i]} units Rs {price[i]}\n'''
        # pdf.write(init, toWrite)
        # init += 1
        pdf.cell(65, 15, toWrite, 1, 1, 'L')
    pdf.set_font('Courier', 'BU', 12)
    pdf.cell(65, 15, grand_total, 1, 1, 'L')
    #    pdf.write(init + 10, grand_total)
    pdf.output('bill.pdf', 'F')


items = ['Egg Fried Rice', 'Aaloo Parathe']
price = [92.0, 51.0]
quantity = [2, 1]
#
generator(items, price, quantity)
