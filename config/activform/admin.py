from django.contrib import admin

# Register your models here.
from .models import ActivForm, PetitionForm

class ActiveFormAdmin(admin.ModelAdmin):
    #fields = ['id', 'email', 'phone_number1', 'first_name']
    list_display = ['id', 'email', 'phone_number1', 'first_name', 'last_name', 'product_id', 'created', 'checked']
    list_display_links = ['id']
    list_filter = ['created', 'checked']
    list_per_page = 15
    date_hierarchy = 'created'
    ordering = ['checked', 'created']
    class Meta:
        model = ActivForm


admin.site.register(ActivForm, ActiveFormAdmin)

class PetitionFormAdmin(admin.ModelAdmin):
    #fields = ['id', 'email', 'phone_number1', 'first_name']
    list_display = ['id', 'email', 'phone_number1', 'first_name', 'last_name', 'petition',  'created', 'checked']
    list_display_links = ['id']
    list_filter = ['created', 'checked']
    list_per_page = 10
    date_hierarchy = 'created'
    ordering = ['checked', 'created']
    class Meta:
        model = PetitionForm

admin.site.register(PetitionForm, PetitionFormAdmin)