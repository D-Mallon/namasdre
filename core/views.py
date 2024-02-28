from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'core/index.html')

def contact(request):
    return render(request, 'core/contact_page.html')