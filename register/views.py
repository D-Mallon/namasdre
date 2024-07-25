from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from core.models import YogaClassBooking
from .forms import ProfileUpdateForm, RegisterForm

# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "register/register.html", {"form": form})

def custom_login(request):
    next_url = request.GET.get('next', '/')
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponseRedirect(request.POST.get('next', '/'))
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form, "next": next_url})

def custom_logout(request):
    logout(request)
    return redirect("home")

# def custom_logout(request):
#     next_url = request.GET.get('next', '/')
#     if '/bookingportal/' in next_url:
#         next_url = '/'
#     logout(request)
#     return HttpResponseRedirect(next_url)

@login_required  
def profile(request):
    booked_classes = YogaClassBooking.objects.filter(user=request.user).order_by('yoga_class__start_time')
    return render(request, 'core/profile.html', {'booked_classes': booked_classes})

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important, to update the session with the new password
            return redirect('core/profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'register/update_profile.html', {'form': form})
