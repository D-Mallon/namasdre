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
from django.conf import settings
from .forms import ContactForm
from django.core.mail import send_mail

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
        form = ContactForm(request.POST)
        if form.is_valid():
            # Cleaned data from the form
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Construct the email subject and message
            subject = f"Contact Form Submission from {name}"
            message_body = f"Message from {name} ({email}):\n\n{message}"

            try:
                # Send the email using Django's send_mail function
                send_mail(
                    subject,
                    message_body,
                    settings.DEFAULT_FROM_EMAIL,  # From email
                    ['namasdreinfo@gmail.com'],    # To email
                    fail_silently=False,
                )
                # Redirect to the same page with a success message
                return redirect('contact')
            except Exception as e:
                # Handle errors and possibly display an error message
                print(f"An error occurred while sending the email: {e}")
                # Optionally, set an error message in the form
                form.add_error(None, 'An error occurred while sending the email. Please try again.')

    else:
        form = ContactForm()

    # Render the contact page with the form
    return render(request, 'core/contact_page.html', {'form': form})

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

@login_required
def remove_class_from_profile(request, class_id):
    if request.method == "POST":
        try:
            booking = get_object_or_404(YogaClassBooking, id=class_id, user=request.user)
            booking.delete()
            return JsonResponse({"success": True, "message": "Booking cancelled successfully."})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    return JsonResponse({"success": False, "message": "Invalid request method."})





@login_required  
def profile(request):
    booked_classes = YogaClassBooking.objects.filter(user=request.user).order_by('yoga_class__start_time')
    return render(request, 'core/profile.html', {'booked_classes': booked_classes})

