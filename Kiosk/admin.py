from django.contrib import admin
from .models import Food, CurrentOrder
import sqlite3


class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'availability')


class CurrentOrderAdmin(admin.ModelAdmin):
    list_display = ('food_item_id', 'name', 'quantity', 'price')


admin.site.register(Food, FoodAdmin)
# Register your models here.
admin.site.register(CurrentOrder, CurrentOrderAdmin)
