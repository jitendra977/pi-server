# filepath: /home/jitu/Project/Django/api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, IoTDeviceViewSet, SensorDataViewSet, ActuatorCommandViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'iotdevices', IoTDeviceViewSet)
router.register(r'sensordata', SensorDataViewSet)
router.register(r'actuatorcommands', ActuatorCommandViewSet)

urlpatterns = [
    path('', include(router.urls)),
]