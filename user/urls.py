# coding=utf-8
"""
date: 2021/8/10 13:59
author: lee sure
"""
from django.urls import path

from user import views

urlpatterns = [
    path('reg',views.reg_view),
    path('login',views.login_view),
    path('logout',views.logout_view),
]