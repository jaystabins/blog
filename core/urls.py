from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/dashboard/', admin.site.urls),
    path('', include('blog.urls')),
    path('accounts/', include("accounts.urls")),
]
