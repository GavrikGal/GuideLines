from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Guide


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'avatar')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'avatar')


class CreationGuideForm(ModelForm):

    # def save(self):
    #     """добавить автора при сохранении"""
    #

    class Meta:
        model = Guide
        fields = ['name', 'description', 'cover']
