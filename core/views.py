from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse
from .models import YogaClass
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.utils import timezone
import datetime

# Create your views here.

def home(request):
    return render(request, 'core/index.html')

# def timetable(request):
#     today = datetime.date.today()
#     start_month = today.replace(day=1)
#     end_month = (start_month + datetime.timedelta(days=32)).replace(day=1)
    
#     online_classes = YogaClass.objects.filter(class_type='online', start_time__gte=start_month, start_time__lt=end_month).order_by('start_time')
#     in_person_classes = YogaClass.objects.filter(class_type='in_person', start_time__gte=start_month, start_time__lt=end_month).order_by('start_time')
    
#         # Debugging lines
#     print("Online Classes:", online_classes)
#     print("In Person Classes:", in_person_classes)


#     context = {
#         'online_classes': online_classes,
#         'in_person_classes': in_person_classes,
#         'today': today,
#     }
#     return render(request, 'core/timetable.html', context)


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
        return render(request, 'core/booking_portal.html')
    else: 
        print('You must be logged in to access this page.')
        return render(request, 'core/index.html', {'error': 'You must be logged in to access this page.'})