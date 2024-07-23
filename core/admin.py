# The admin.py file in a Django application is used to configure how your models are displayed and managed in the Django admin interface. In the context of your YogaClass model, the admin.py file allows you to customize the admin interface for easier management of your yoga class data.

from django.contrib import admin
from django import forms
from django.utils import timezone
from .models import YogaClass
from django.contrib.admin.widgets import AdminSplitDateTime

class YogaClassForm(forms.ModelForm):
    class Meta:
        model = YogaClass
        fields = '__all__'
        widgets = {
            'start_time': AdminSplitDateTime(),
            'end_time': AdminSplitDateTime(),
        }

    def clean_start_time(self):
        start_time = self.cleaned_data['start_time']
        if not timezone.is_aware(start_time):
            start_time = timezone.make_aware(start_time)
        return start_time

    def clean_end_time(self):
        end_time = self.cleaned_data['end_time']
        if not timezone.is_aware(end_time):
            end_time = timezone.make_aware(end_time)
        return end_time

# this is what's going to be shown on the admin page
@admin.register(YogaClass)
class YogaClassAdmin(admin.ModelAdmin):
    form = YogaClassForm
    list_display = ('id', 'title', 'class_type', 'start_time', 'end_time', 'location')
    list_filter = ('class_type','class_type')
    search_fields = ('title', 'location')

