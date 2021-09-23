from django.contrib import admin
from . models import Category, Product,ProfileDetail, ShopCart, PaidOrder
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','title','img')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','category','name','price','min_quantity','max_quantity','img','description','available','featured','new_arrival')


class ProfileDetailAdmin(admin.ModelAdmin):
    list_display = ('id','first_name','last_name','phone','image','address','city','state')


class ShopCartAdmin(admin.ModelAdmin):
    list_display = ('id','user','product','quantity','cart_code','paid_order')


class PaidOrderAdmin(admin.ModelAdmin):
    list_display = ('id','total_paid','user','transac_code','created','cart_code','paid_order','first_name','last_name','phone','address','city','state')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProfileDetail, ProfileDetailAdmin)
admin.site.register(ShopCart, ShopCartAdmin)
admin.site.register(PaidOrder, PaidOrderAdmin)
