from django.urls import path, include
from rest_framework import routers
from .views import *

#api versioning
router = routers.DefaultRouter()
router.register(r'customUsers', CustomUserView, 'customUsers')

urlpatterns = [
    path('api/v1/', include(router.urls)),
]