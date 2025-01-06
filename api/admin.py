from django.contrib import admin
from .models import (
    User,
    Firmware,
    IoTDevice,
    GPIOPin,
    Button,
    LED,
    SensorData,
    ActuatorCommand,
    DeviceLog,
    Notification,
)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name')

@admin.register(Firmware)
class FirmwareAdmin(admin.ModelAdmin):
    list_display = ('version', 'release_date', 'description')
    search_fields = ('version',)
    list_filter = ('release_date',)

@admin.register(IoTDevice)
class IoTDeviceAdmin(admin.ModelAdmin):
    list_display = ('device_name', 'device_type', 'device_status', 'device_location', 'device_last_updated', 'device_owner', 'firmware')
    list_filter = ('device_type', 'device_status', 'firmware')
    search_fields = ('device_name', 'device_owner__username')

@admin.register(GPIOPin)
class GPIOPinAdmin(admin.ModelAdmin):
    list_display = ('pin_number', 'device', 'is_led')
    search_fields = ('pin_number', 'device__device_name')

@admin.register(Button)
class ButtonAdmin(admin.ModelAdmin):
    list_display = ('gpio_pin', 'button_status', 'device')
    search_fields = ('gpio_pin__pin_number', 'device__device_name')

@admin.register(LED)
class LEDAdmin(admin.ModelAdmin):
    list_display = ('gpio_pin', 'led_status', 'device')
    search_fields = ('gpio_pin__pin_number', 'device__device_name')

@admin.register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    list_display = ('device', 'timestamp', 'data')
    search_fields = ('device__device_name',)
    list_filter = ('timestamp',)

@admin.register(ActuatorCommand)
class ActuatorCommandAdmin(admin.ModelAdmin):
    list_display = ('device', 'command', 'timestamp')
    search_fields = ('device__device_name', 'command')
    list_filter = ('timestamp',)

@admin.register(DeviceLog)
class DeviceLogAdmin(admin.ModelAdmin):
    list_display = ('device', 'timestamp', 'log_entry')
    search_fields = ('device__device_name', 'log_entry')
    list_filter = ('timestamp',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'timestamp', 'read')
    search_fields = ('user__username', 'message')
    list_filter = ('read', 'timestamp')