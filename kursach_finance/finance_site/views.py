from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, CreateView, TemplateView

from finance_site.models import Finance_site
from finance_site.forms import AddOperationForm


# Create your views here.


class Home(TemplateView):
    """Класс-представление который просто грузит странчику добро пожаловать и ссылкой на регистрацию"""
    template_name = 'finance/index.html'


class about(TemplateView): # Класс который грузит страничку На которой в дальнейшем будет Faq и о нас
    template_name = 'finance/about.html'


class Operations(LoginRequiredMixin, ListView): # Класс который показывает все операции пользователя
    template_name = 'finance/operations.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Finance_site.objects.filter(author__username=self.request.user.username)


class graphics(LoginRequiredMixin, ListView):
    """Страница на которой будут графики и диаграммы"""
    template_name = 'finance/graphics.html'


class AddPage(LoginRequiredMixin, CreateView): # Класс с формой для добавления операции
    form_class = AddOperationForm
    template_name = 'finance/addpage.html'
    success_url = reverse_lazy('home')
    extra_context = {'title': "Добавление операции"}

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


def page_not_found(request, exception): # Обработчик ошибки 404
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")