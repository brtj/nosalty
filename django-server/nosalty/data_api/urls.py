from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('data_api', views.DataAggregatorView)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls'))
]
