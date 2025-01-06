from rest_framework import viewsets
from .models import User, IoTDevice, GPIOPin, Button, LED, SensorData, ActuatorCommand
from .serializers import (
    UserSerializer, IoTDeviceSerializer, GPIOPinSerializer, ButtonSerializer,
    LEDSerializer, SensorDataSerializer, ActuatorCommandSerializer
)


class GPIOPinViewSet(viewsets.ModelViewSet):
    queryset = GPIOPin.objects.all()
    serializer_class = GPIOPinSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class IoTDeviceViewSet(viewsets.ModelViewSet):
    queryset = IoTDevice.objects.all()
    serializer_class = IoTDeviceSerializer


class GPIOPinViewSet(viewsets.ModelViewSet):
    queryset = GPIOPin.objects.all()
    serializer_class = GPIOPinSerializer


class ButtonViewSet(viewsets.ModelViewSet):
    queryset = Button.objects.all()
    serializer_class = ButtonSerializer


class LEDViewSet(viewsets.ModelViewSet):
    queryset = LED.objects.all()
    serializer_class = LEDSerializer


class SensorDataViewSet(viewsets.ModelViewSet):
    queryset = SensorData.objects.all()
    serializer_class = SensorDataSerializer


class ActuatorCommandViewSet(viewsets.ModelViewSet):
    queryset = ActuatorCommand.objects.all()
    serializer_class = ActuatorCommandSerializer