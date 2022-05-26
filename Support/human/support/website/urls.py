from django.urls import path, include
from . import views


urlpatterns = [
    path('customs', views.customs, name='customs'),
    path('categories', views.categories, name='categories'),
    path('', views.index, name='index'),
]