from django.urls import path
from . import views


urlpatterns = [
    path('', views.Home.as_view(), name='home'),  # http://127.0.0.1:8000
    path('addpage/', views.AddPage.as_view(), name='add_page'),
    path('operations/', views.Operations.as_view(), name='operations'),
    path('about/', views.about.as_view(), name='about'),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard')
]
