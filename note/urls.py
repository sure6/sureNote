# coding=utf-8
"""
date: 2021/8/10 17:43
author: lee sure
"""
from django.urls import path

from note import views

urlpatterns=[
    path('add', views.add_note),
]