# coding=utf-8
"""
date: 2021/8/10 17:43
author: lee sure
"""
from django.urls import path

from note import views

urlpatterns=[
    path('add', views.addnote_view),
    path('list', views.list_view),
    path('detail', views.notedetail_view),
    path('edit', views.noteedit_view),
    path('delete/<int:id>', views.notedelete_view),
]