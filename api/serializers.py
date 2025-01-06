from rest_framework import serializers
from .models import (
    User, Firmware, IoTDevice, GPIOPin, Button, LED, 
    SensorData, ActuatorCommand, DeviceLog, Notification
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'created_at']


class FirmwareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firmware
        fields = ['id', 'version', 'release_date', 'description']


class GPIOPinSerializer(serializers.ModelSerializer):
    device = serializers.StringRelatedField()  # Display the device name

    class Meta:
        model = GPIOPin
        fields = ['id', 'pin_number', 'device', 'is_led']


class ButtonSerializer(serializers.ModelSerializer):
    gpio_pin = GPIOPinSerializer()  # Nested GPIO pin details
    device = serializers.StringRelatedField()  # Display the device name

    class Meta:
        model = Button
        fields = ['id', 'gpio_pin', 'button_status', 'device']


class LEDSerializer(serializers.ModelSerializer):
    gpio_pin = GPIOPinSerializer()  # Nested GPIO pin details
    device = serializers.StringRelatedField()  # Display the device name

    class Meta:
        model = LED
        fields = ['id', 'gpio_pin', 'led_status', 'device']


class SensorDataSerializer(serializers.ModelSerializer):
    device = serializers.StringRelatedField()  # Display the device name

    class Meta:
        model = SensorData
        fields = ['id', 'device', 'timestamp', 'data']


class ActuatorCommandSerializer(serializers.ModelSerializer):
    device = serializers.StringRelatedField()  # Display the device name

    class Meta:
        model = ActuatorCommand
        fields = ['id', 'device', 'timestamp', 'command']


class DeviceLogSerializer(serializers.ModelSerializer):
    device = serializers.StringRelatedField()  # Display the device name

    class Meta:
        model = DeviceLog
        fields = ['id', 'device', 'timestamp', 'log_entry']


class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Display the username

    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'timestamp', 'read']


class IoTDeviceSerializer(serializers.ModelSerializer):
    device_owner = serializers.StringRelatedField()  # Display the username
    firmware = FirmwareSerializer()  # Nested firmware details
    gpio_pins = GPIOPinSerializer(many=True, read_only=True)  # Include related GPIO pins
    buttons = ButtonSerializer(many=True, read_only=True)  # Include related buttons
    leds = LEDSerializer(many=True, read_only=True)  # Include related LEDs

    class Meta:
        model = IoTDevice
        fields = [
            'id', 'device_name', 'device_type', 'device_status', 'device_location',
            'device_last_updated', 'device_owner', 'firmware', 'gpio_pins', 'buttons', 'leds'
        ]