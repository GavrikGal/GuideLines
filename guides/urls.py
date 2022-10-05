from django.urls import path

from .views import home_page, RegistrationView


app_name = 'guides'
urlpatterns = [
    path('registration/registration/', RegistrationView.as_view(), name='registration'),
    path('', home_page, name='home_page'),
]
