from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView

from .forms import CustomUserCreationForm, CreationGuideForm


class RegistrationView(CreateView):
    """Регистрация пользователя"""
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('guides:home_page')
    template_name = 'registration/registration.html'


class HomePageView(TemplateView):
    """Главная страница"""
    template_name = 'main.html'


class NewGuideView(CreateView):
    """Создание нового Руководства"""
    form_class = CreationGuideForm
    success_url = reverse_lazy('guides:detail')
    template_name = 'guide/new.html'

# def new_guide(request):
#     """заглушка"""
#     # todo: вместо этого метода сделать класс NewGuide(CreateView) по аналогии с RegistrationView(CreateView)
#     return render(request, 'guide/new.html')
