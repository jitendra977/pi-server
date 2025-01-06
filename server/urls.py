from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'leds', views.LEDViewSet)

urlpatterns = [
    path('', include(router.urls)),
]