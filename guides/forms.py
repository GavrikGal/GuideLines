from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Guide, Article


class UpdateArticleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update(rows='4')

    class Meta:
        model = Article
        fields = ['name', 'text']


class CreationArticleForm(ModelForm):

    class Meta:
        model = Article
        fields = ['name', 'text']


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'avatar')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'avatar')


class CreationGuideForm(ModelForm):

    class Meta:
        model = Guide
        fields = ['name', 'description', 'cover']


class UpdateGuideForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update(rows='4')

    class Meta:
        model = Guide
        fields = ['name', 'description', 'cover']