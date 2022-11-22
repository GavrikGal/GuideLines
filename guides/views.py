from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView


from .forms import CustomUserCreationForm, CreationGuideForm, UpdateGuideForm, CreationArticleForm
from .models import Guide, Article


class DetailArticleView(DetailView):
    """Детальный просмотр Статьи"""
    model = Article
    context_object_name = 'article'
    template_name = 'article/detail.html'


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
        return reverse_lazy('guides:detail_guide', kwargs={'guide_pk': self.kwargs.get('guide_pk')})


class DeleteGuideView(DeleteView):
    """Удаление Руководства"""
    model = Guide
    success_url = reverse_lazy('guides:home_page')
    slug_field = 'pk'
    slug_url_kwarg = 'guide_pk'


class UpdateGuideView(UpdateView):
    """Обновление (редактирование) Руководства"""
    model = Guide
    form_class = UpdateGuideForm
    template_name = 'guide/edit.html'
    slug_field = 'pk'
    slug_url_kwarg = 'guide_pk'

    def get_success_url(self):
        return reverse_lazy('guides:detail_guide', kwargs={'guide_pk': self.object.pk})


class RegistrationView(CreateView):
    """Регистрация пользователя"""
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('guides:home_page')
    template_name = 'registration/registration.html'


class HomePageView(TemplateView):
    """Главная страница"""
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        """Добавляет Руководства в контекст страницы"""
        context = super().get_context_data(**kwargs)
        context['guides'] = Guide.objects.all()
        return context


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
        return reverse_lazy('guides:detail_guide', kwargs={'guide_pk': self.object.pk})


class DetailGuideView(DetailView):
    """Детальный просмотр поста"""
    model = Guide
    context_object_name = 'guide'
    template_name = 'guide/detail.html'
    slug_field = 'pk'
    slug_url_kwarg = 'guide_pk'


def detail_article_view(request):
    """Заглушка"""
    pass

