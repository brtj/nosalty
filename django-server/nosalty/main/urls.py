from django.urls import path, include
from django.conf.urls import url
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('category_report', views.category_report, name='category_report'),
    path('contact', views.contact, name='contact'),
    path('change_log', views.change_log, name='change_log'),
    path('how_it_works', views.how_it_works, name='how_it_works'),
    url(r'report_current/(?P<city>\w+)/(?P<category>[\w|-]+)$', views.report, name='report')
]