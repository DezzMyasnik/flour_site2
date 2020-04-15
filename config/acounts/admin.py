from django.contrib import admin

from .models import Accounts, Gender

admin.site.site_header = "StudioMyka.ru администраитивный сайт"
admin.site.site_title = "Администрирование StudioMyka"
admin.site.register(Gender)
admin.site.register(Accounts)