from django.urls import path, include
from .views import home, contact, timetable, booking_portal, profile, add_class_to_profile, remove_class_from_profile
from register import views as register_views

urlpatterns = [
    path('', home, name='home'),
    path('contact/', contact, name='contact'),
    path('timetable/', timetable, name='timetable'),
    path('bookingportal/', booking_portal, name='booking_portal'),
    path('add_class_to_profile/<int:class_id>/', add_class_to_profile, name='add_class_to_profile'),
    path('remove_class_from_profile/<int:class_id>/', remove_class_from_profile, name='remove_class_from_profile'),
    path('accounts/', include("django.contrib.auth.urls")),  # Ensure this path is correct
    path('profile', profile, name='profile'),
    path("update_profile/", register_views.update_profile, name="update_profile"), 
    path('login/', register_views.custom_login, name='login'),
    path('logout/', register_views.custom_logout, name='logout'),
]
