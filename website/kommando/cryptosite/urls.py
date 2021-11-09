from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('', include('kommando.urls')),
    path('admin/' , admin.site.urls)
]