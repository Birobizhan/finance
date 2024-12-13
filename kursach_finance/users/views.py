from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView

from finance_site.models import Finance_site
from users.forms import LoginUserForm, RegisterUserForm, ProfileUserForm


# Create your views here.

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login')


class ProfileUser(LoginRequiredMixin, ListView,):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {"title": 'Профиль пользователя'}
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        # Получаем контекст из родительского метода
        context = super().get_context_data(**kwargs)
        # Добавляем request в контекст
        context['request'] = self.request
        context['expenses'] = Finance_site.objects.filter(operation_type=1, author__username=self.request.user.username).aggregate(Sum('amount'))
        context['income'] = Finance_site.objects.filter(operation_type=0, author__username=self.request.user.username).aggregate(Sum('amount'))
        return context

    def get_queryset(self):
        return Finance_site.objects.filter(author__username=self.request.user.username)

    def get_success_url(self):
        return reverse_lazy('users:profile', args=[self.request.user.pk])

    def get_object(self, queryset=None):
        return self.request.user


