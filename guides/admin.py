from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .forms import CreationGuideForm, CreationArticleForm
from .models import CustomUser, Guide, Article


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'first_name', 'last_name', 'avatar']


class GuideAdmin(admin.ModelAdmin):
    add_form = CreationGuideForm
    model = Guide
    list_display = ['name', 'description', 'cover', 'author']


class ArticleAdmin(admin.ModelAdmin):
    add_form = CreationArticleForm
    model = Article
    list_display = ['name', 'text', 'guide', 'author', 'draft']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Guide, GuideAdmin)
admin.site.register(Article, ArticleAdmin)
