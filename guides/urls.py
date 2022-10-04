from django.urls import path

from .views import home_page, registration


app_name = 'guides'
urlpatterns = [
    path('registration/', registration, name='registration'),
    path('', home_page, name='home_page'),
]
