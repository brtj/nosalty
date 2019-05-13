from django.urls import path, include
from django.conf.urls import url
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('category_report_choice', views.category_report_choice, name='category_report_choice'),
    path('city_report_choice', views.city_report_choice, name='city_report_choice'),
    path('contact', views.contact, name='contact'),
    path('change_log', views.change_log, name='change_log'),
    path('how_it_works', views.how_it_works, name='how_it_works'),
    url(r'category_report_current/(?P<city>\w+)/(?P<category>[\w|-]+)$', views.category_report, name='category_report'),
    url(r'city_report_current/(?P<city>\w+)$', views.city_report, name='city_report')
]