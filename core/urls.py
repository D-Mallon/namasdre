from django.urls import path, include
from .views import home, contact, timetable, booking_portal, profile
from register import views as register_views

urlpatterns = [
    path('', home, name='home'),
    path('contact/', contact, name='contact'),
    path('timetable/', timetable, name='timetable'),
    path('bookingportal/', booking_portal, name='booking_portal'),
    path('accounts/', include("django.contrib.auth.urls")),  # Ensure this path is correct
    path('profile', profile, name='profile'),
    path('login/', register_views.custom_login, name='login'),
    path('logout/', register_views.custom_logout, name='logout'),
]
