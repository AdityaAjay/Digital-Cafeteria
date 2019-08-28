from standalone_py_code.orderPage import *
from tkinter import messagebox
from time import sleep

# import webbrowser


window = Tk()
window.geometry('1366x768')
window.title("Catering Care")
while True:
    lbl = Label(window, text="Welcome to Catering Care", font=("Ubuntu", 30))
    lbl.grid(column=10, row=0)

    lbl2 = Label(window, text="Tap your College ID", font=("Ubuntu", 20))
    lbl2.grid(column=10, row=13)

    lbl3 = Label(window, text="or Click here to pay via Paytm or Credit/Debit Card", font=("Ubuntu", 20))
    lbl3.grid(column=10, row=14)


    def clicked():
        if startOrder("Guest"):
            messagebox.showinfo("Order Complete", "Please collect your receipt\nThank You")
            window.mainloop()
        else:
            messagebox.showerror("Order failed", "Please try again")


    def card_tapped():
        # if code is read from rfid then true
        # messagebox.showinfo("Info","Please hold the card")
        return False


    def post_tap():
        # code to read data from ID

        # available in raspberry pi only

        enrolment = " "
        if startOrder(enrolment):
            messagebox.showinfo("Order Complete", "Please collect your receipt\nThank You")
            window.mainloop()
        else:
            messagebox.showerror("Order failed", "Please try again")


    # strURL = "http://www.csestack.org"
    # webbrowser.open(strURL, new=0)
    btn = Button(window, text="Click", command=clicked)
    btn.grid(column=10, row=15)
    window.update_idletasks()
    window.update()
    if card_tapped():
        post_tap()
    sleep(1)
# window.mainloop()
