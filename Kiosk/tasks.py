from __future__ import absolute_import, unicode_literals
from celery import Celery
from django.shortcuts import render
from time import sleep

app = Celery('tasks', broker='redis://localhost:7777')


@app.task
def rfid():
    sleep(5)
    return render('Kiosk/landing.html')
# def add(x, y):
#     return x + y


# @shared_task
# def mul(x, y):
#     return x * y
#
#
# @shared_task
# def xsum(numbers):
#     return sum(numbers)
