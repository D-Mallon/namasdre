from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from .models import YogaClass, YogaClassBooking
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.utils import timezone
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, 'core/index.html')

def timetable(request):
    now = timezone.now()
    # Get classes for today
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    # use below if trying to bookend filter with start and end of current day. Preference is to show all future classes though.
    # today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)

    online_classes = YogaClass.objects.filter(
        class_type='online',
        start_time__gte=today_start
    ).order_by('start_time')

    in_person_classes = YogaClass.objects.filter(
        class_type='in_person',
        start_time__gte=today_start
    ).order_by('start_time')

    # Debugging lines to print the context
    print("Current Time:", now)
    for cls in online_classes:
        print(f"Online Class: {cls.title}, Start Time: {cls.start_time}, End Time: {cls.end_time}")
    for cls in in_person_classes:
        print(f"In Person Class: {cls.title}, Start Time: {cls.start_time}, End Time: {cls.end_time}")

    context = {
        'online_classes': online_classes,
        'in_person_classes': in_person_classes,
        'now': now,
    }
    return render(request, 'core/timetable.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        
        # Send email
        send_mail(
            f"Contact Form Submission from {name}",
            message,
            email,
            ['info@namasdre.com'],
            fail_silently=False,
        )
        
        return HttpResponse('Thank you for your message.')

    return render(request, 'core/contact_page.html')


@login_required
def booking_portal(request):
    if request.user.is_authenticated:
        now = timezone.now()
        # Removing prior classes from the booking portal so that only future classes are shown
        # today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        # use below if trying to bookend filter with start and end of current day. Preference is to show all future classes though.
        # today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)

        online_classes = YogaClass.objects.filter(
            class_type='online',
            start_time__gte=now
        ).order_by('start_time')

        in_person_classes = YogaClass.objects.filter(
            class_type='in_person',
            start_time__gte=now
        ).order_by('start_time')

        context = {
            'online_classes': online_classes,
            'in_person_classes': in_person_classes,
            'now': now,
        }
        return render(request, 'core/booking_portal.html', context)
        # return render(request, 'core/booking_portal.html')
    else: 
        print('You must be logged in to access this page.')
        return render(request, 'core/index.html', {'error': 'You must be logged in to access this page.'})

@login_required
def add_class_to_profile(request, class_id):
    yoga_class = get_object_or_404(YogaClass, id=class_id)
    if YogaClassBooking.objects.filter(user=request.user, yoga_class=yoga_class).exists():
        return JsonResponse({'message': 'You have already booked this class.'})
    YogaClassBooking.objects.create(user=request.user, yoga_class=yoga_class)
    return JsonResponse({'message': 'Class added to your profile!'})


# @login_required
# def add_class_to_profile(request, class_id):
#     yoga_class = get_object_or_404(YogaClass, id=class_id)
#     if YogaClassBooking.objects.filter(user=request.user, yoga_class=yoga_class).exists():
#         alert = 'You have already booked this class.'
#         return redirect('profile')
#     YogaClassBooking.objects.create(user=request.user, yoga_class=yoga_class)
#     return redirect('profile')

def isClassBooked(user, yoga_class):
    return YogaClassBooking.objects.filter(user=user, yoga_class=yoga_class).exists()

@login_required  
def profile(request):
    booked_classes = YogaClassBooking.objects.filter(user=request.user).order_by('yoga_class__start_time')
    return render(request, 'core/profile.html', {'booked_classes': booked_classes})

