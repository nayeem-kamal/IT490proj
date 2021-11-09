from django.urls import path
from . import views

urlpatterns = [
    path('apiTest' , views.apiTest)
]