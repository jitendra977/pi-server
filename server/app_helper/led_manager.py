# led_manager.py
from gpiozero import LED as GPIOLED

# Global dictionary to store LED objects
led_instances = {}

def manage_led(led_pin, action_type):
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

def update_led_status(led_instance, led):
    led_instance.status = led.is_lit
    led_instance.save()