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
    path('login/', register_views.custom_login, name='login'),
    path('logout/', register_views.custom_logout, name='logout'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/update_profile/', register_views.update_profile, name='update_profile'),
    path('accounts/register/', register_views.register, name='register'),
    path('accounts/password_reset/', include('register.urls')),  # Include the register app's URLs for password reset
    path('profile', profile, name='profile'),
    path('update_profile/', register_views.update_profile, name='update_profile'),
    path('register/', register_views.register, name='register'),
]
