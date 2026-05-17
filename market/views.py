from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.


def home(request):
    return render(request, 'home.html')
def about(request):
    return render(request, 'about_us.html')
def contact(request):
    return render(request, 'contact_us.html')
