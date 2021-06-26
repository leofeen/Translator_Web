from django.urls import path

from . import views


app_name = "translator_web"
urlpatterns = [
    path('', views.index, name='index'),
    path('translate/', views.translate, name='translate'),
]
