from django.contrib import admin
from products.models import Categories, Products, Person, Currency, Warehouse

admin.site.register(Categories)
admin.site.register(Products)
admin.site.register(Person)
admin.site.register(Warehouse)
admin.site.register(Currency)
