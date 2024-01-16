from django.contrib import admin

# Register your models here.
from .models import Category,Product,CartProduct,OrderProduct,Order,User

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(CartProduct)
admin.site.register(OrderProduct)
admin.site.register(Order)
