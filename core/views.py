from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse
from .models import YogaClass
import datetime

# Create your views here.

def home(request):
    return render(request, 'core/index.html')

# def contact(request):
#     return render(request, 'core/contact_page.html')

# def timetable(request):
#     return render(request, "core/timetable.html")

def timetable(request):
    today = datetime.date.today()
    start_month = today.replace(day=1)
    end_month = (start_month + datetime.timedelta(days=32)).replace(day=1)
    
    online_classes = YogaClass.objects.filter(class_type='online', start_time__gte=start_month, start_time__lt=end_month)
    in_person_classes = YogaClass.objects.filter(class_type='in_person', start_time__gte=start_month, start_time__lt=end_month)

    context = {
        'online_classes': online_classes,
        'in_person_classes': in_person_classes,
        'today': today,
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
