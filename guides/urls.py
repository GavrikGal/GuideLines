from django.urls import path

from .views import RegistrationView, HomePageView, NewGuideView, DetailGuideView, UpdateGuideView, DeleteGuideView, \
    NewArticleView, DetailArticleView


app_name = 'guides'
urlpatterns = [
    path('registrations/registration/', RegistrationView.as_view(), name='registration'),
    path('guides/new/', NewGuideView.as_view(), name='new_guide'),
    path('guides/<int:guide_pk>/', DetailGuideView.as_view(), name='detail_guide'),
    path('guides/<int:guide_pk>/edit/', UpdateGuideView.as_view(), name='edit_guide'),
    path('guides/<int:guide_pk>/delete/', DeleteGuideView.as_view(), name='delete_guide'),
    path('guides/<int:guide_pk>/articles/new/', NewArticleView.as_view(), name='new_article'),
    path('guides/<int:guide_pk>/articles/<int:pk>/', DetailArticleView.as_view(), name='detail_article'),
    path('', HomePageView.as_view(), name='home_page'),
]
