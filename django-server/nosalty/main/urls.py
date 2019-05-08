from django.urls import path, include
from django.conf.urls import url
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    url(r'report_current/(?P<city>\w+)/(?P<category>[\w|-]+)$', views.report, name='report')
]