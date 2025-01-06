from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from .models import User, LED
from .serializers import UserSerializer, LEDSerializer
from gpiozero import LED as GPIOLED

# Create a global dictionary to store LED objects for persistence across requests
led_instances = {}

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer

class LEDViewSet(viewsets.ModelViewSet):
    queryset = LED.objects.all().order_by('name')
    serializer_class = LEDSerializer

    @action(detail=True, methods=['post'])
    def turn_on(self, request, pk=None):
        """Turn on the LED for a specific LED instance using the gpio pin from the model."""
        # Retrieve the LED object based on the pk
        led_instance = self.get_object()
        
        # Get the GPIO pin stored in the LED model
        gpio_pin = led_instance.gpio
        user = led_instance.user
        print(f"User: {user}, GPIO Pin: {gpio_pin}")
        
        if gpio_pin == 0:
            return Response({"error": "Invalid GPIO pin"}, status=400)

        try:
            # Check if the LED instance already exists in the dictionary
            if gpio_pin not in led_instances:
                # Create the LED instance and store it in the dictionary
                led_instances[gpio_pin] = GPIOLED(gpio_pin)

            # Turn on the LED (ensure it stays on)
            led_instances[gpio_pin].on()
            # update the status of the LED instance in the database
            led_instance.status = True
            led_instance.save()

            return Response({"status": f"LED on GPIO pin {gpio_pin} is now ON"})
        
        except ValueError:
            return Response({"error": "Invalid GPIO pin number"}, status=400)
            

    @action(detail=True, methods=['post'])
    def turn_off(self, request, pk=None):
        """Turn off the LED for a specific LED instance using the gpio pin from the model."""
        # Retrieve the LED object based on the pk
        led_instance = self.get_object()
        
        # Get the GPIO pin stored in the LED model
        gpio_pin = led_instance.gpio
        user = led_instance.user
        print(f"User: {user}, GPIO Pin: {gpio_pin}")
        
        if gpio_pin == 0:
            return Response({"error": "Invalid GPIO pin"}, status=400)

        try:
            # Check if the LED instance already exists in the dictionary
            if gpio_pin not in led_instances:
                # Create the LED instance and store it in the dictionary
                led_instances[gpio_pin] = GPIOLED(gpio_pin)

            # Turn off the LED
            led_instances[gpio_pin].off()
            # update the status of the LED instance in the database
            led_instance.status = False
            led_instance.save()

            return Response({"status": f"LED on GPIO pin {gpio_pin} is now OFF"})
        
        except ValueError:
            return Response({"error": "Invalid GPIO pin number"}, status=400)
    
    @action(detail=True, methods=['post'])
    def toggle(self, request, pk=None):
        """Toggle the LED state (on/off) for a specific LED instance using the gpio pin."""
        try:
            # Retrieve the LED object based on the pk
            led_instance = self.get_object()
            gpio_pin = led_instance.gpio

            if gpio_pin == 0:
                return Response({"error": "Invalid GPIO pin"}, status=400)

            # Check if the LED instance already exists in the dictionary
            if gpio_pin not in led_instances:
                led_instances[gpio_pin] = GPIOLED(gpio_pin)

            # Toggle the LED state
            led = led_instances[gpio_pin]
            if led.is_lit:
                led.off()
                led_instance.status = False
                status = "off"
            else:
                led.on()
                led_instance.status = True
                status = "on"

            led_instance.save()

            return Response({"status": f"LED on GPIO pin {gpio_pin} is now {status}"})

        except Exception as e:
            return Response({"error": str(e)}, status=500)