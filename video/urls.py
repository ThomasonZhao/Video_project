"""
@author: Thomason
@contact: ThomasonZhao810@gmail.com 
@create: 2020/5/2 8:26 AM 
"""
from django.urls import path
from . import views

app_name = 'video'
urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index'),
    path('search/', views.SearchListView.as_view(), name='search'),
]
