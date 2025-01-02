from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from gpiozero import LED
from .models import User, IoTDevice, SensorData, ActuatorCommand, GPIOPin
from .serializers import UserSerializer, IoTDeviceSerializer, SensorDataSerializer, ActuatorCommandSerializer
import logging

logger = logging.getLogger(__name__)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class IoTDeviceViewSet(viewsets.ModelViewSet):
    queryset = IoTDevice.objects.all()
    serializer_class = IoTDeviceSerializer
    leds = {}  # Dictionary to store LED objects

    @action(detail=True, methods=['post'])
    def turn_on(self, request, pk=None):
        logger.debug(f"Attempting to turn on device with ID: {pk}")
        try:
            device = self.get_object()
            gpio_pin = GPIOPin.objects.get(device=device)  # Get the associated GPIO pin
            if pk not in self.leds:
                self.leds[pk] = LED(gpio_pin.pin_number)  # Use the pin number from GPIOPin
            self.leds[pk].on()
            device.device_status = True  # Update the device status
            device.save()
            return Response({'status': 'Device turned on'}, status=status.HTTP_200_OK)
        except IoTDevice.DoesNotExist:
            logger.error(f"No IoTDevice matches the given query with ID: {pk}")
            return Response({'detail': 'No IoTDevice matches the given query.'}, status=status.HTTP_404_NOT_FOUND)
        except GPIOPin.DoesNotExist:
            logger.error(f"No GPIOPin associated with IoTDevice ID: {pk}")
            return Response({'detail': 'No GPIOPin associated with this IoTDevice.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def toggle(self, request, pk=None):
        logger.debug(f"Attempting to toggle device with ID: {pk}")
        try:
            device = self.get_object()
            gpio_pin = GPIOPin.objects.get(device=device)  # Get the associated GPIO pin
            if pk not in self.leds:
                self.leds[pk] = LED(gpio_pin.pin_number)  # Use the pin number from GPIOPin

            if device.device_status:
                self.leds[pk].off()
                device.device_status = False
                status_message = 'Device turned off'
            else:
                self.leds[pk].on()
                device.device_status = True
                status_message = 'Device turned on'

            device.save()
            return Response({'status': status_message}, status=status.HTTP_200_OK)
        except IoTDevice.DoesNotExist:
            logger.error(f"No IoTDevice matches the given query with ID: {pk}")
            return Response({'detail': 'No IoTDevice matches the given query.'}, status=status.HTTP_404_NOT_FOUND)
        except GPIOPin.DoesNotExist:
            logger.error(f"No GPIOPin associated with IoTDevice ID: {pk}")
            return Response({'detail': 'No GPIOPin associated with this IoTDevice.'}, status=status.HTTP_404_NOT_FOUND)

class SensorDataViewSet(viewsets.ModelViewSet):
    queryset = SensorData.objects.all()
    serializer_class = SensorDataSerializer

class ActuatorCommandViewSet(viewsets.ModelViewSet):
    queryset = ActuatorCommand.objects.all()
    serializer_class = ActuatorCommandSerializer