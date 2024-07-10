# The admin.py file in a Django application is used to configure how your models are displayed and managed in the Django admin interface. In the context of your YogaClass model, the admin.py file allows you to customize the admin interface for easier management of your yoga class data.

from django.contrib import admin
from .models import YogaClass

@admin.register(YogaClass)
class YogaClassAdmin(admin.ModelAdmin):
    list_display = ('title', 'class_type', 'start_time', 'end_time', 'location')
    list_filter = ('class_type',)
    search_fields = ('title', 'location')
