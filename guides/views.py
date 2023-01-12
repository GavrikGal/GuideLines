from abc import ABC
from django.db.models import QuerySet
from django.http import HttpResponse, HttpRequest
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from django.urls import reverse_lazy


from .forms import CustomUserCreationForm, CreationGuideForm, UpdateGuideForm, CreationArticleForm, UpdateArticleForm
from .models import Guide, Article


def do_not_publish_article(request: HttpRequest, guide_pk: int, pk: int) -> HttpResponse:
    """Снимает Статью с публикации"""
    article = Article.objects.get(pk=pk)
    article.draft = True
    article.save()
    return redirect('guides:detail_guide', guide_pk=guide_pk)


def publish_article(request: HttpRequest, guide_pk: int, pk: int) -> HttpResponse:
    """Публикует Статью"""
    article = Article.objects.get(pk=pk)
    article.draft = False
    article.save()
    return redirect('guides:detail_guide', guide_pk=guide_pk)


class DeleteArticleView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление Руководства"""
    model = Article
    login_url = reverse_lazy('login')

    def get_success_url(self):
        return reverse_lazy('guides:detail_guide', kwargs={'guide_pk': self.object.guide.pk})

    def test_func(self):
        return self.get_object().author == self.request.user


class UpdateArticleView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Обновление (редактирование) Статьи"""
    model = Article
    form_class = UpdateArticleForm
    template_name = 'article/edit.html'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        return Article.objects.select_related('guide', 'author').filter(pk=self.kwargs.get('pk'))

    def get_success_url(self):
        return reverse_lazy('guides:detail_article', kwargs={'guide_pk': self.object.guide.pk,
                                                             'pk': self.object.pk})

    def test_func(self):
        return self.get_object().author == self.request.user


class DetailArticleView(UserPassesTestMixin, DetailView):
    """Детальный просмотр Статьи"""
    model = Article
    context_object_name = 'article'
    template_name = 'article/detail.html'

    def get_queryset(self):
        return Article.objects.select_related('guide', 'author').filter(pk=self.kwargs.get('pk'))

    def test_func(self):
        article: Article = self.get_object()
        if article.draft:
            if not self.request.user.is_authenticated:
                return False
            if self.request.user == article.author:
                return True
            return False
        else:
            return True


class NewArticleView(LoginRequiredMixin, CreateView):
    """Создание новой Статьи"""
    form_class = CreationArticleForm
    template_name = 'article/new.html'
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        """добавить автора и Руководство перед сохранением, если форма валидна"""
        form.instance.author = self.request.user
        form.instance.guide = Guide.objects.get(pk=self.kwargs.get('guide_pk'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('guides:detail_guide', kwargs={'guide_pk': self.kwargs.get('guide_pk')})


class DeleteGuideView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление Руководства"""
    model = Guide
    success_url = reverse_lazy('guides:home_page')
    login_url = reverse_lazy('login')
    slug_field = 'pk'
    slug_url_kwarg = 'guide_pk'

    def test_func(self):
        return self.get_object().author == self.request.user


class UpdateGuideView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Обновление (редактирование) Руководства"""

    model = Guide
    form_class = UpdateGuideForm
    template_name = 'guide/edit.html'
    login_url = reverse_lazy('login')
    slug_field = 'pk'
    slug_url_kwarg = 'guide_pk'

    def get_queryset(self):
        return Guide.objects.select_related('author').filter(pk=self.kwargs.get('guide_pk'))

    def get_success_url(self):
        return reverse_lazy('guides:detail_guide', kwargs={'guide_pk': self.object.pk})

    def test_func(self):
        return self.get_object().author == self.request.user


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
        # context['guides'] = Guide.objects.all()
        context['guides'] = Guide.objects.select_related('author').all()
        return context


class NewGuideView(LoginRequiredMixin, CreateView):
    """Создание нового Руководства"""
    login_url = reverse_lazy('login')
    form_class = CreationGuideForm
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            q = Q(draft=False)
        else:
            q = Q(draft=False) | Q(author=self.request.user)
        # articles = self.object.article_set.filter(q)
        articles = self.object.article_set.select_related('guide', 'author').filter(q)
        # articles = Article.objects.select_related('guide', 'author').filter(Q(guide=self.object) & q)
        context['articles'] = articles
        return context


def delete_article_view(request):
    """Заглушка"""
    pass

