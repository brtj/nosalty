from django.urls import path, include
from django.conf.urls import url
from . import views

app_name = 'changelog'

urlpatterns = [
    path('change_log', views.change_log, name='change_log')
    ]