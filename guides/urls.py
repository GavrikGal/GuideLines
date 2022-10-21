from django.urls import path

from .views import RegistrationView, HomePageView, new_guide


app_name = 'guides'
urlpatterns = [
    path('registration/registration/', RegistrationView.as_view(), name='registration'),
    path('guide/new/', new_guide, name='new_guide'),
    path('', HomePageView.as_view(), name='home_page'),
]
