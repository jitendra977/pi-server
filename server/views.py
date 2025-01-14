import random
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
import logging
import schedule
import threading
import time
from datetime import datetime, timedelta

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

def generate_fake_sensor_data():
    """Generate and save fake sensor data every second."""
    fake_temperature = round(random.uniform(10, 30), 2)  # Generate a random temperature between 10 and 30
    sensor_data = SensorData(
        sensor_name="Fake Temperature",
        sensor_type="temperature",
        value=fake_temperature,
        unit="°C",
        user=None,  # Assuming no user is associated
        device=None  # Assuming no device is associated
    )
    sensor_data.save()
    print(f"Saved fake sensor data: {fake_temperature}°C")

def delete_old_sensor_data():
    """Delete sensor data older than a specific time frame."""
    cutoff_time = datetime.now() - timedelta(minutes=1)
    deleted_count, _ = SensorData.objects.filter(timestamp__lt=cutoff_time).delete()
    logging.info(f"Deleted {deleted_count} old sensor data entries.")

def check_temperature_and_toggle_leds():
    temperature_reader = SensorReader(sensor_type='temperature')
    latest_temperature_data = temperature_reader.read_latest_sensor_data()
    if latest_temperature_data:
        # Print the temperature value
        print(f"Current temperature: {latest_temperature_data.value}°C")
        
        if latest_temperature_data.value > 25:
            try:
                led_instance = LED.objects.get(name="KITCHEN")
                led, error = manage_led(led_instance.led_pin, "toggle")
                if not error:
                    update_led_status(led_instance, led)
                    logging.info(f"Toggled LED on GPIO pin {led_instance.led_pin} due to temperature alert.")
                else:
                    logging.error(f"Error managing LED: {error}")
            except LED.DoesNotExist:
                logging.error("LED with name 'KITCHEN' does not exist.")
            except Exception as e:
                logging.error(f"An error occurred while retrieving LEDs: {e}")

def start_scheduler():
    # Schedule tasks
    schedule.every(10).minutes.do(generate_fake_sensor_data)
    schedule.every(10).minutes.do(check_temperature_and_toggle_leds)
    schedule.every(60).minutes.do(delete_old_sensor_data)
    
    # Run the scheduler in a separate thread to avoid blocking
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start the scheduler in a new thread
scheduler_thread = threading.Thread(target=start_scheduler)
scheduler_thread.daemon = True
scheduler_thread.start()