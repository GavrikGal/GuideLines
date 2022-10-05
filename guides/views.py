from django.shortcuts import render


def home_page(request):
    return render(request, 'base.html')


def registration(request):
    return render(request, 'registration/registration.html')
