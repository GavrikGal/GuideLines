from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm


class RegistrationView(CreateView):
    """Регистрация пользователя"""
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('guides:home_page')
    template_name = 'registration/registration.html'

#
# def registration(request):
#     return render(request, 'registration/registration.html')


def home_page(request):
    return render(request, 'base.html')

