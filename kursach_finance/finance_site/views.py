from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView
import plotly.graph_objects as go
from django.shortcuts import render
from finance_site.models import Finance_site, Category
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


class graphics(LoginRequiredMixin, ListView):
    """Страница на которой будут графики и диаграммы"""
    template_name = 'finance/graphics.html'


class AddPage(LoginRequiredMixin, CreateView): # Класс с формой для добавления операции
    model = Category
    form_class = AddOperationForm
    template_name = 'finance/addpage.html'
    success_url = reverse_lazy('operations')
    extra_context = {'title': "Добавление операции"}

    def form_valid(self, form):
        w = form.save(commit=False)
        print(self.request.POST)
        if self.request.POST['cat1']:
            w.cat = Category.objects.get(pk=self.request.POST['cat1'])
        else:
            w.cat = Category.objects.get(pk=self.request.POST['cat2'])
        w.author = self.request.user
        return super().form_valid(form)



def create_chart(random_x):
    amount = [x[1] for x in random_x]
    cat = [x[0] for x in random_x]
    operation_name = [x[2] for x in random_x]
    print(operation_name)
    fig = go.Figure(data=go.Pie(labels=cat, values=amount, textinfo='label+percent', hovertext=operation_name,
                              hoverinfo='label+value+text'))

    # Сохранение графика в HTML
    graph_html = fig.to_html(full_html=False)

    return graph_html


class Dashboard(ListView):
    model = Finance_site
    template_name = 'finance/dashboard.html'
    context_object_name = 'graphics'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        random_x = list(
            Finance_site.objects.filter(operation_type=1, author__username=self.request.user.username).values_list('cat__name', 'amount', 'operation_name'))
        chart1 = create_chart(random_x)
        random_x = list(
            Finance_site.objects.filter(operation_type=0, author__username=self.request.user.username).values_list(
                'cat__name', 'amount', 'operation_name'))
        chart2 = create_chart(random_x)
        context['chart1'] = chart1
        context['chart2'] = chart2
        return context


def page_not_found(request, exception): # Обработчик ошибки 404
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")

