from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from .models import LED,  User
from .serializers import  LEDSerializer, UserSerializer
from gpiozero import LED as GPIOLED , Button as GPIOButton
from signal import pause
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
        """
        A helper method to handle LED actions (on/off/toggle).
        :param gpio_pin: The GPIO pin of the LED.
        :param action_type: The action ('on', 'off', 'toggle') to perform on the LED.
        :return: A tuple of the status and the updated LED instance.
        """
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

        return led, None  # Return the LED instance and no error

    def _update_led_status(self, led_instance, led):
        """
        Update the LED instance status in the database.
        :param led_instance: The LED instance from the database.
        :param led: The GPIOLED instance to check the status of.
        """
        led_instance.status = led.is_lit
        led_instance.save()

    @action(detail=True, methods=['post'])
    def turn_on(self, request, pk=None):
        """Turn on the LED for a specific LED instance using the gpio pin."""
        led_instance = self.get_object()
        gpio_pin = led_instance.gpio

        led, error = self._manage_led(gpio_pin, 'on')
        if error:
            return Response({"error": error}, status=400)

        self._update_led_status(led_instance, led)
        return Response({"status": f"LED on GPIO pin {gpio_pin} is now ON"})

    @action(detail=True, methods=['post'])
    def turn_off(self, request, pk=None):
        """Turn off the LED for a specific LED instance using the gpio pin."""
        led_instance = self.get_object()
        gpio_pin = led_instance.gpio

        led, error = self._manage_led(gpio_pin, 'off')
        if error:
            return Response({"error": error}, status=400)

        self._update_led_status(led_instance, led)
        return Response({"status": f"LED on GPIO pin {gpio_pin} is now OFF"})

    @action(detail=True, methods=['post'])
    def toggle(self, request, pk=None):
        """Toggle the LED state (on/off) for a specific LED instance using the gpio pin."""
        led_instance = self.get_object()
        gpio_pin = led_instance.gpio

        led, error = self._manage_led(gpio_pin, 'toggle')
        if error:
            return Response({"error": error}, status=400)

        self._update_led_status(led_instance, led)
        status = "on" if led.is_lit else "off"
        return Response({"status": f"{led_instance.name} LED is now {status}"})

class ButtonViewSet:
    def __init__(self):
        # Initialize the button on GPIO pin 21
        self.button = GPIOButton(21, bounce_time=0.1)  # Use debouncing
        self.led_viewset = LEDViewSet()  # Create an instance of LEDViewSet
        self.button.when_pressed = self.say_hello

    def say_hello(self):
        try:
            print("Hello, I'm pressed! How are you?")
            gpio_pin = 26
            led, error = self.led_viewset._manage_led(gpio_pin, 'toggle')
            if error:
                print(f"Error: {error}")
            else:
                print(f"LED on GPIO pin {gpio_pin} toggled successfully. Current state: {'ON' if led.is_lit else 'OFF'}")
        except Exception as e:
            print(f"An unexpected error occurred in say_hello: {e}")

# Instantiate the ButtonViewSet to start listening for button presses
button_view_set = ButtonViewSet()

# Manually poll the button state in a loop for improved responsiveness
while True:
    button_view_set.button.wait_for_press()  # Wait for button press
    sleep(0.1)  # Sleep for a short period to reduce CPU load