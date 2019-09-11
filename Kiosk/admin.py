from django.contrib import admin
from .models import Food, CurrentOrder, OrderNumber
import sqlite3


class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'availability')


class CurrentOrderAdmin(admin.ModelAdmin):
    list_display = ('food_item_id', 'name', 'quantity', 'price')


class OrderNumberAdmin(admin.ModelAdmin):
    list_display = ('id','order_id')


admin.site.register(Food, FoodAdmin)
admin.site.register(OrderNumber, OrderNumberAdmin)
admin.site.register(CurrentOrder, CurrentOrderAdmin)
