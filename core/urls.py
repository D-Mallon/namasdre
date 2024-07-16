from django.urls import path, include
from .views import home, contact
from core import views

urlpatterns = [
    path('', home, name='home'),
    path('contact/', contact, name='contact'),  # This should serve your contact page
    path('timetable/', views.timetable, name='timetable'),
    path('', include("django.contrib.auth.urls"))
]