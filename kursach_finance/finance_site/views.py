from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView, UpdateView, DeleteView
import plotly.graph_objects as go
from finance_site.models import Finance_site, Category
from finance_site.forms import AddOperationForm
from django.http import HttpResponseForbidden


# Create your views here.
class Home(TemplateView):
    template_name = 'finance/index.html'


class AddPage(LoginRequiredMixin, CreateView):
    model = Finance_site
    form_class = AddOperationForm
    template_name = 'finance/addpage.html'
    success_url = reverse_lazy('users:profile')
    extra_context = {'title': "Добавление операции"}

    def form_valid(self, form):
        w = form.save(commit=False)
        if self.request.POST['cat1']:
            w.cat = Category.objects.get(pk=self.request.POST['cat1'])
        else:
            w.cat = Category.objects.get(pk=self.request.POST['cat2'])
        w.author = self.request.user
        return super().form_valid(form)


class DeletePage(LoginRequiredMixin, DeleteView):
    model = Finance_site
    success_url = reverse_lazy('users:profile')
    template_name = 'finance/finance_site_confirm_delete.html'
    context_object_name = 'post'
    extra_context = {'title': 'Удаление операции'}

    def form_valid(self, form):
        return super(DeletePage, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        return HttpResponseForbidden("У вас нет прав для удаления этого объекта.")


class UpdatePage(LoginRequiredMixin, UpdateView):
    model = Finance_site
    form_class = AddOperationForm

    template_name = 'finance/addpage.html'
    success_url = reverse_lazy('users:profile')
    extra_context = {'title': "Изменение операции"}

    def form_valid(self, form):
        w = form.save(commit=False)
        print(self.request.POST)
        if self.request.POST['cat1']:
            w.cat = Category.objects.get(pk=self.request.POST['cat1'])
        else:
            w.cat = Category.objects.get(pk=self.request.POST['cat2'])
        w.author = self.request.user
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        return HttpResponseForbidden("У вас нет прав для изменения этого объекта.")

def create_chart(random_x):
    amount = [x[1] for x in random_x]
    cat = [x[0] for x in random_x]
    fig = go.Figure(data=go.Pie(labels=cat, values=amount, textinfo='label+percent',
                              hoverinfo='label+value+text'))

    fig.update_layout(
        width=500,
        height=500,
    )
    graph_html = fig.to_html(full_html=False)

    return graph_html


class Dashboard(LoginRequiredMixin, ListView):
    model = Finance_site
    template_name = 'finance/icons1.html'
    context_object_name = 'graphics'
    extra_context = {'title': 'Статистика'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        random_x = list(
            Finance_site.objects.filter(operation_type=1, author__username=self.request.user.username).values_list('cat__name', 'amount'))
        chart1 = create_chart(random_x)
        random_x = list(
            Finance_site.objects.filter(operation_type=0, author__username=self.request.user.username).values_list(
                'cat__name', 'amount'))
        chart2 = create_chart(random_x)
        context['chart1'] = chart1
        context['chart2'] = chart2

        category_sums = Finance_site.objects.filter(author__username=self.request.user.username).values('cat__name', 'cat__type').annotate(total_price=Sum('amount'))
        category = []
        for cat in category_sums:
            category.append([cat['cat__name'], cat['total_price'], cat['cat__type']])
        dia_income = [x[:2] for x in category if x[2] == False]
        dia_expenses = [x[:2] for x in category if x[2] == True]
        context['dia_income'] = dia_income
        context['dia_expenses'] = dia_expenses
        return context


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1><a href='/'>На главную</a>")
