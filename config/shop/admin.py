from django.contrib import admin
from .models import *
from orders.models import Checkout
# Register your models here.
from django.contrib.admin.views.main import ChangeList
from django import forms

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    #raw_id_fields = ('dishes',)
admin.site.register(Category, CategoryAdmin)


class KitchenInline(admin.TabularInline):
    fk_name = 'kitchen'
    model = KitchenGallary


#@admin.register(Kitchen)
class KitchenAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'description', ]
    prepopulated_fields = {'slug': ('name',)}
    #raw_id_fields = ('dishes',)
    inlines = [KitchenInline, ]
admin.site.register(Kitchen, KitchenAdmin)


class DishesInline(admin.TabularInline):
    fk_name = 'dish'
    model = DishesGallary


#@admin.register(Dishes)
class DishesAdmin(admin.ModelAdmin):
    list_display = ['name','id', 'slug', 'description',]  #'kitchen'
    #exclude = ['kitchen']
    prepopulated_fields = {'slug': ('name',)}
    #raw_id_fields = ('dishes',)
    inlines = [DishesInline, ]
    search_fields = ('name',)

admin.site.register(Dishes, DishesAdmin)

class DishForamtAdmin(admin.ModelAdmin):
    fields = ['pos', 'dish']
    #list_display = ['pos', 'dish']

admin.site.register(DishFormat, DishForamtAdmin)

class OrederInlines(admin.StackedInline):
    model = Checkout
    fk_name = 'product_id'
    fields = ('user', 'product_id',
        ('first_name', 'last_name','phone_number1', 'email',),
       'quantity',
        )
    extra =  0




class ProductAdmin(admin.ModelAdmin):
    fields = ['name', 'category', 'kitchen', 'dishes',
              'slug', 'description','dateofevent','duration',
              'quantity', 'stock','price','image',  'available', ]
    list_display = ('name', 'category', 'dateofevent', 'duration',
                    'quantity', 'stock', 'price',
                    'available',)
    # filter_vertical  = ('dishes',) 'get_dishes','slug', 'description', 'image', 'created', 'updated', 'kitchen',

    list_filter = ['available',
                   'dateofevent', ]  #'created', 'updated'
    list_editable = ['price', 'dateofevent', 'quantity', 'stock',  'available']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [OrederInlines,]
    #get_dishes.ordering = 'first_dishes__id'
    #raw_id_fields = ('category', 'kitchen', 'dishes',)
    #raw_id_fields = ('dishes',)



    def get_dishes(self, obj):
        return '\n'.join([p.dish.name for p in obj.dishes.all()])


    @property
    def first_dishes(self):
        self.dishes.all().first()

admin.site.register(Product, ProductAdmin)