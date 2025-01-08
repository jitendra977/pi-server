from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
import logging

from server.app_helper.button_handler import ButtonHandler
from server.app_helper.led_manager import manage_led, update_led_status
from server.app_helper.sensor_handler import SensorReader
from .models import LED, SensorData, User
from .serializers import LEDSerializer, SensorDataSerializer, UserSerializer

# Set up logging
logging.basicConfig(level=logging.DEBUG)

class SensorDataViewSet(viewsets.ModelViewSet):
    queryset = SensorData.objects.all()
    serializer_class = SensorDataSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer

class LEDViewSet(viewsets.ModelViewSet):
    queryset = LED.objects.all().order_by('name')
    serializer_class = LEDSerializer

    @action(detail=True, methods=['post'])
    def turn_on(self, request, pk=None):
        led_instance = self.get_object()
        led, error = manage_led(led_instance.led_pin, 'on')
        if error:
            return Response({"error": error}, status=400)

        update_led_status(led_instance, led)
        return Response({"status": f"LED on GPIO pin {led_instance.led_pin} is now ON"})

    @action(detail=True, methods=['post'])
    def turn_off(self, request, pk=None):
        led_instance = self.get_object()
        led, error = manage_led(led_instance.led_pin, 'off')
        if error:
            return Response({"error": error}, status=400)

        update_led_status(led_instance, led)
        return Response({"status": f"LED on GPIO pin {led_instance.led_pin} is now OFF"})

    @action(detail=True, methods=['post'])
    def toggle(self, request, pk=None):
        led_instance = self.get_object()
        led, error = manage_led(led_instance.led_pin, 'toggle')
        if error:
            return Response({"error": error}, status=400)

        update_led_status(led_instance, led)
        status = "on" if led.is_lit else "off"
        return Response({"status": f"{led_instance.name} LED is now {status}"})

# Start the button handler
ButtonHandler().start()


# Start the sensor reader
def check_temperature_and_toggle_leds():
    temperateure_reader = SensorReader(sensor_type='temperature')
    latest_temperature_data = temperateure_reader.read_latest_sensor_data()
    if latest_temperature_data and latest_temperature_data.value > 25:
       try:
           led_instances = LED.objects.get(name = "KITCHEN")
           led,error = manage_led(led_instances.led_pin,"toggle")
           if not error:
               update_led_status(led_instances, led)
               logging.info(f"Toggled LED on GPIO pin {led_instances.led_pin} due to temperature alert.")
           else:
               logging.error(f"Error managing LED: {error}")
       except LED.DoesNotExist:
           logging.error("LED with name 'KITCHEN' does not exist.")
           return
       except Exception as e:
           logging.error(f"An error occurred while retrieving LEDs: {e}")
           return

# Schedule the temperature check and LED toggle
check_temperature_and_toggle_leds()