from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from .forms import RegisterForm

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
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.POST.get('next', '/')
            return HttpResponseRedirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, "register/registrations/login.html", {"form": form})

def custom_logout(request):
    next_url = request.GET.get('next', '/')
    if '/bookingportal/' in next_url:
        next_url = '/'
    logout(request)
    return HttpResponseRedirect(next_url)