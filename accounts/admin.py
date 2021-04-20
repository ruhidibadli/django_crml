from django.contrib import admin
from .models import *
# Register your models here.


# admin.site.register(Customer)
# admin.site.register(Product)
# admin.site.register(Order)


models=[
    Customer,
    Product,
    Order,
    Tag
]

admin.site.register(models)