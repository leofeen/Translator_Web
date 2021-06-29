from django.urls import path

from . import views


app_name = "translator_web"
urlpatterns = [
    path('translate/', views.translate, name='translate'),
    path('specification/<str:language>/', views.specification, name='specification'),
    path('', views.index, name='index'),
]
