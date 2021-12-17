from django.urls import path
from . import views

urlpatterns = [
    path('' , views.login),
    path('charts.html' , views.apiTest),
    path('login.html' , views.login),
    path('trade.html' , views.trade),
    path('accounts.html' , views.accounts),
    path('testRegistration.html',views.contact),
    path('history.html' ,views.history),
    path('ledger.html', views.ledger)


]