"""
@author: Thomason
@contact: ThomasonZhao810@gmail.com 
@create: 2020/4/29 6:05 PM 
"""

from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
]
