from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from finance_site.models import Finance_site
from users.forms import LoginUserForm, RegisterUserForm


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


class ProfileUser(LoginRequiredMixin, ListView):
    model = get_user_model()
    template_name = 'users/icons.html'
    extra_context = {"title": 'Профиль'}
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expenses'] = Finance_site.objects.filter(operation_type=1, author__username=self.request.user.username).aggregate(Sum('amount'))
        context['income'] = Finance_site.objects.filter(operation_type=0, author__username=self.request.user.username).aggregate(Sum('amount'))
        return context

    def get_queryset(self):
        return Finance_site.objects.filter(author__username=self.request.user.username)


