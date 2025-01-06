from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from .models import LED, User
from .serializers import LEDSerializer, UserSerializer
from gpiozero import LED as GPIOLED, Button as GPIOButton
import threading
import os
import signal
import sys
from time import sleep

# Create a global dictionary to store LED objects for persistence across requests
led_instances = {}

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer

class LEDViewSet(viewsets.ModelViewSet):
    queryset = LED.objects.all().order_by('name')
    serializer_class = LEDSerializer

    def _manage_led(self, gpio_pin, action_type):
        if gpio_pin == 0:
            return None, "Invalid GPIO pin"

        if gpio_pin not in led_instances:
            led_instances[gpio_pin] = GPIOLED(gpio_pin)

        led = led_instances[gpio_pin]

        if action_type == 'on':
            led.on()
        elif action_type == 'off':
            led.off()
        elif action_type == 'toggle':
            led.toggle()
        else:
            return None, "Invalid action type"

        return led, None

    def _update_led_status(self, led_instance, led):
        led_instance.status = led.is_lit
        led_instance.save()

    @action(detail=True, methods=['post'])
    def turn_on(self, request, pk=None):
        led_instance = self.get_object()
        gpio_pin = led_instance.gpio
        led, error = self._manage_led(gpio_pin, 'on')
        if error:
            return Response({"error": error}, status=400)

        self._update_led_status(led_instance, led)
        return Response({"status": f"LED on GPIO pin {gpio_pin} is now ON"})

    @action(detail=True, methods=['post'])
    def turn_off(self, request, pk=None):
        led_instance = self.get_object()
        gpio_pin = led_instance.gpio
        led, error = self._manage_led(gpio_pin, 'off')
        if error:
            return Response({"error": error}, status=400)

        self._update_led_status(led_instance, led)
        return Response({"status": f"LED on GPIO pin {gpio_pin} is now OFF"})

    @action(detail=True, methods=['post'])
    def toggle(self, request, pk=None):
        led_instance = self.get_object()
        gpio_pin = led_instance.gpio
        led, error = self._manage_led(gpio_pin, 'toggle')
        if error:
            return Response({"error": error}, status=400)

        self._update_led_status(led_instance, led)
        status = "on" if led.is_lit else "off"
        return Response({"status": f"{led_instance.name} LED is now {status}"})
class LEDButtonViewSet(viewsets.ModelViewSet):
    queryset = LED.objects.all()
    serializer_class = LEDSerializer

class ButtonHandler:
    def __init__(self):
        self.button = GPIOButton(21, bounce_time=0.1)
        self.led_viewset = LEDViewSet()
        self.button.when_pressed = self.handle_button_press

    def handle_button_press(self):
        try:
            print("Hello, I'm pressed! How are you?")
            gpio_pin = 26
            led, error = self.led_viewset._manage_led(gpio_pin, 'toggle')
            if error:
                print(f"Error: {error}")
            else:
                led_instance = LED.objects.get(gpio = gpio_pin)
                self.led_viewset._update_led_status(led_instance, led)
                print(f"LED on GPIO pin {gpio_pin} toggled successfully. Current state: {'ON' if led.is_lit else 'OFF'}")
        except Exception as e:
            print(f"An unexpected error occurred in handle_button_press: {e}")

def signal_handler(sig, frame):
    print("Gracefully exiting...")
    sys.exit(0)

if os.environ.get('RUN_MAIN') == 'true':
    signal.signal(signal.SIGINT, signal_handler)
    
    # Start button handler in a separate thread
    def button_thread():
        button_handler = ButtonHandler()
        while True:
            try:
                button_handler.button.wait_for_press()
                sleep(0.1)
            except KeyboardInterrupt:
                break
    
    threading.Thread(target=button_thread, daemon=True).start()