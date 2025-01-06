from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from gpiozero import LED as GPIOLED, Button as GPIOButton
from .models import LED, User
from .serializers import LEDSerializer, UserSerializer
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

    def _manage_led(self, led_pin, action_type):
        if led_pin == 0:
            return None, "Invalid GPIO pin"

        if led_pin not in led_instances:
            led_instances[led_pin] = GPIOLED(led_pin)

        led = led_instances[led_pin]

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
        led_pin = led_instance.led_pin
        led, error = self._manage_led(led_pin, 'on')
        if error:
            return Response({"error": error}, status=400)

        self._update_led_status(led_instance, led)
        return Response({"status": f"LED on GPIO pin {led_pin} is now ON"})

    @action(detail=True, methods=['post'])
    def turn_off(self, request, pk=None):
        led_instance = self.get_object()
        led_pin = led_instance.led_pin
        led, error = self._manage_led(led_pin, 'off')
        if error:
            return Response({"error": error}, status=400)

        self._update_led_status(led_instance, led)
        return Response({"status": f"LED on GPIO pin {led_pin} is now OFF"})

    @action(detail=True, methods=['post'])
    def toggle(self, request, pk=None):
        led_instance = self.get_object()
        led_pin = led_instance.led_pin
        led, error = self._manage_led(led_pin, 'toggle')
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
        self.led_viewset = LEDViewSet()
        self.button_handlers = []
        self.setup_buttons()

    def setup_buttons(self):
        # Fetch all LEDs and create a button handler for each LED's button pin
        leds = LED.objects.all()
        for led in leds:
            if led.button_pin != 0:  # Ensure there is a valid GPIO pin
                button = GPIOButton(led.button_pin, bounce_time=0.1)
                button.when_pressed = lambda led_instance=led: self.handle_button_press(led_instance)
                self.button_handlers.append(button)
                print(f"Button set up for LED {led.name} on GPIO pin {led.button_pin}")

    def handle_button_press(self, led_instance):
        try:
            print(f"Button pressed for LED: {led_instance.name}!")

            led_pin = led_instance.led_pin  # Get GPIO pin for the LED from the model
            led, error = self.led_viewset._manage_led(led_pin, 'toggle')

            if error:
                print(f"Error: {error}")
            else:
                # Update the LED instance status in the database
                self.led_viewset._update_led_status(led_instance, led)
                print(f"LED on GPIO pin {led_pin} toggled successfully. Current state: {'ON' if led.is_lit else 'OFF'}")
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
                button_handler.button_handlers[0].wait_for_press()  # Wait for the button press event
                sleep(0.1)
            except KeyboardInterrupt:
                break
    
    threading.Thread(target=button_thread, daemon=True).start()