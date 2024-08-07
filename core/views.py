from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.utils import timezone
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import YogaClass, YogaClassBooking
from .forms import YogaClassForm, ContactForm
from django.core.mail import send_mail

def home(request):
    can_manage_classes = request.user.has_perm('core.manage_classes')
    return render(request, 'core/index.html', {
        'can_manage_classes': can_manage_classes
    })

def timetable(request):
    can_manage_classes = request.user.has_perm('core.manage_classes')
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

    online_classes = YogaClass.objects.filter(
        class_type='online',
        start_time__gte=today_start
    ).order_by('start_time')

    in_person_classes = YogaClass.objects.filter(
        class_type='in_person',
        start_time__gte=today_start
    ).order_by('start_time')

    context = {
        'online_classes': online_classes,
        'in_person_classes': in_person_classes,
        'now': now,
        'can_manage_classes': can_manage_classes
    }
    return render(request, 'core/timetable.html', context)

def contact(request):
    can_manage_classes = request.user.has_perm('core.manage_classes')
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            subject = f"Contact Form Submission from {name}"
            message_body = f"Message from {name} ({email}):\n\n{message}"

            try:
                send_mail(
                    subject,
                    message_body,
                    settings.DEFAULT_FROM_EMAIL,
                    ['namasdreinfo@gmail.com'],
                    fail_silently=False,
                )
                # Set the success message
                messages.success(request, "Contact form submitted successfully. Thanks for your message.")
                return redirect('contact')  # Use redirect instead of render
            except Exception as e:
                print(f"An error occurred while sending the email: {e}")
                form.add_error(None, 'An error occurred while sending the email. Please try again.')
    else:
        form = ContactForm()

    return render(request, 'core/contact_page.html', {'form': form, 'can_manage_classes': can_manage_classes})

@login_required
def booking_portal(request):
    can_manage_classes = request.user.has_perm('core.manage_classes')
    if request.user.is_authenticated:
        now = timezone.now()

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
            'can_manage_classes': can_manage_classes
        }
        return render(request, 'core/booking_portal.html', context)
    else: 
        return render(request, 'core/index.html', {'error': 'You must be logged in to access this page.', 'can_manage_classes': can_manage_classes})

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
    can_manage_classes = request.user.has_perm('core.manage_classes')
    now = timezone.now()
    booked_classes = YogaClassBooking.objects.filter(user=request.user).order_by('yoga_class__start_time')

    # Separate upcoming and past classes
    upcoming_classes = booked_classes.filter(yoga_class__start_time__gte=now)
    past_classes = booked_classes.filter(yoga_class__start_time__lt=now)

    context = {
        'upcoming_classes': upcoming_classes,
        'past_classes': past_classes,
        'can_manage_classes': can_manage_classes
    }
    
    return render(request, 'core/profile.html', context)

@login_required
def manage_classes(request):
    # Check if the user has the 'manage_classes' permission
    if not request.user.has_perm('core.manage_classes'):
        raise PermissionDenied("You do not have permission to manage classes.")

    if request.method == 'POST':
        form = YogaClassForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Class has been added successfully!')
            return redirect('manage_classes')  # Redirect to the same page
        else:
            messages.error(request, 'There was an error adding the class. Please check the form.')
    else:
        form = YogaClassForm()

    now = timezone.now()

    # Separate upcoming and past classes
    upcoming_classes = YogaClass.objects.filter(start_time__gte=now).order_by('-start_time')
    past_classes = YogaClass.objects.filter(start_time__lt=now).order_by('-start_time')

    # Pass classes to the template
    context = {
        'form': form,
        'upcoming_classes': upcoming_classes,
        'past_classes': past_classes,
        'can_manage_classes': True,
    }
    return render(request, 'core/manage_classes.html', context)

@login_required
def edit_class(request, class_id):
    yoga_class = get_object_or_404(YogaClass, id=class_id)
    if request.method == 'POST':
        form = YogaClassForm(request.POST, instance=yoga_class)
        if form.is_valid():
            form.save()
            messages.success(request, 'Class updated successfully!')
            return redirect('manage_classes')
    else:
        form = YogaClassForm(instance=yoga_class)
    return render(request, 'core/edit_class.html', {'form': form, 'yoga_class': yoga_class})

@login_required
def delete_class(request, class_id):
    yoga_class = get_object_or_404(YogaClass, id=class_id)
    if request.method == 'POST':
        yoga_class.delete()
        messages.success(request, 'Class deleted successfully!')
        return redirect('manage_classes')
    return render(request, 'core/delete_class.html', {'yoga_class': yoga_class})

def permission_denied(request, exception):
    return render(request, 'core/permission_denied.html', status=403)
