from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('nofluff_data', views.NofluffView)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls'))
]
