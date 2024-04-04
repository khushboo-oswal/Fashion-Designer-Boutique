from django.contrib import admin
from StyleSculptapp.models import Product
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display=['name','detail','category','fabric','size','color','price','is_active']
    list_filter=['category','is_active']


admin.site.register(Product,ProductAdmin)