from django.conf import settings
from django.db import models
from django.utils import timezone
import sqlite3

db = sqlite3.connect('db.sqlite3')


class Food(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    image_url = models.CharField(max_length=2083, default='#')
    availability = models.BooleanField(default=True)


class CurrentOrder(models.Model):
    food_item_id = models.IntegerField(default=0)
    name = models.CharField(max_length=100, default="test")
    quantity = models.IntegerField(default=1)
    price = models.FloatField(default=0)


class OrderNumber(models.Model):
    order_id = models.IntegerField(default=1)
