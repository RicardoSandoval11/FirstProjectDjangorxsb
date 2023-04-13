from django.contrib import admin

# models 
from .models import *

admin.site.register(Color)
admin.site.register(Materials)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(CarShop)
admin.site.register(WishList)
