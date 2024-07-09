from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'core/index.html')

# def contact(request):
#     return render(request, 'core/contact_page.html')


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
