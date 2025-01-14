# button_handler.py
from gpiozero import Button as GPIOButton

from server.models import LED

from .led_manager import manage_led, update_led_status

class ButtonHandler:
    def __init__(self):
        self.button_handlers = []
        self.setup_buttons()

    def setup_buttons(self):
        leds = LED.objects.all()
        for led in leds:
            if led.button_pin != 0:
                button = GPIOButton(led.button_pin, bounce_time=0.1)
                button.when_pressed = lambda led_instance=led: self.handle_button_press(led_instance)
                self.button_handlers.append(button)
                print(f"Button set up for LED {led.name} on GPIO pin {led.button_pin}")

    def handle_button_press(self, led_instance):
        print(f"Button pressed for LED: {led_instance.name}!")
        led, error = manage_led(led_instance.led_pin, 'toggle')
        if error:
            print(f"Error: {error}")
        else:
            update_led_status(led_instance, led)
            print(f"LED on GPIO pin {led_instance.led_pin} toggled successfully. Current state: {'ON' if led.is_lit else 'OFF'}")

    def start(self):
        print("ButtonHandler started.")