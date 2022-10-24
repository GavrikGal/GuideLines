from django.urls import path

from .views import RegistrationView, HomePageView, NewGuideView, DetailGuideView


app_name = 'guides'
urlpatterns = [
    path('registration/registration/', RegistrationView.as_view(), name='registration'),
    path('guide/new/', NewGuideView.as_view(), name='new_guide'),
    path('guide/<int:pk>', DetailGuideView.as_view(), name='detail_guide'),
    path('', HomePageView.as_view(), name='home_page'),
]
