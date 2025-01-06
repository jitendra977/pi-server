from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, IoTDeviceViewSet, GPIOPinViewSet, ButtonViewSet,
    LEDViewSet, SensorDataViewSet, ActuatorCommandViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'iot-devices', IoTDeviceViewSet)
router.register(r'gpio-pins', GPIOPinViewSet)
router.register(r'buttons', ButtonViewSet)
router.register(r'leds', LEDViewSet)
router.register(r'sensor-data', SensorDataViewSet)
router.register(r'actuator-commands', ActuatorCommandViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]