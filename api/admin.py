# filepath: /home/jitu/Project/Django/api/admin.py
from django.contrib import admin
from .models import User, IoTDevice, GPIOPin, SensorData, ActuatorCommand

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in User._meta.fields]

@admin.register(IoTDevice)
class IoTDeviceAdmin(admin.ModelAdmin):
    list_display = [field.name for field in IoTDevice._meta.fields]

@admin.register(GPIOPin)
class GPIOPinAdmin(admin.ModelAdmin):
    list_display = [field.name for field in GPIOPin._meta.fields]

@admin.register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SensorData._meta.fields]

@admin.register(ActuatorCommand)
class ActuatorCommandAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ActuatorCommand._meta.fields]