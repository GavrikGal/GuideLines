from django.urls import path

from .views import RegistrationView, HomePageView, NewGuideView, DetailGuideView, UpdateGuideView


app_name = 'guides'
urlpatterns = [
    path('registration/registration/', RegistrationView.as_view(), name='registration'),
    path('guide/new/', NewGuideView.as_view(), name='new_guide'),
    path('guide/<int:pk>', DetailGuideView.as_view(), name='detail_guide'),
    path('guide/edit/<int:pk>', UpdateGuideView.as_view(), name='edit_guide'),
    path('', HomePageView.as_view(), name='home_page'),
]
