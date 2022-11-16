from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView


from .forms import CustomUserCreationForm, CreationGuideForm, UpdateGuideForm, CreationArticleForm
from .models import Guide


class NewArticleView(CreateView):
    """Создание новой Статьи"""
    form_class = CreationArticleForm
    template_name = 'article/new.html'

    def form_valid(self, form):
        """добавить автора и Руководство перед сохранением, если форма валидна"""
        form.instance.author = self.request.user
        form.instance.guide = Guide.objects.get(pk=self.kwargs.get('guide_pk'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('guides:detail_guide', kwargs={'pk': self.kwargs.get('guide_pk')})


class DeleteGuideView(DeleteView):
    """Удаление Руководства"""
    model = Guide
    success_url = reverse_lazy('guides:home_page')


class UpdateGuideView(UpdateView):
    """Обновление (редактирование) Руководства"""
    model = Guide
    form_class = UpdateGuideForm
    template_name = 'guide/edit.html'

    def get_success_url(self):
        return reverse_lazy('guides:detail_guide', kwargs={'pk': self.object.pk})


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
    # success_url = reverse_lazy('guides:detail_guide', kwargs={'pk': self.pk})
    template_name = 'guide/new.html'

    def form_valid(self, form):
        """добавить автора перед сохранение, если форма валидна"""
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('guides:detail_guide', kwargs={'pk': self.object.pk})


class DetailGuideView(DetailView):
    """Детальный просмотр поста"""
    model = Guide
    context_object_name = 'guide'
    template_name = 'guide/detail.html'


def new_article_view(request):
    """Заглушка"""
    pass

