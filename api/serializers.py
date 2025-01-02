# filepath: /home/jitu/Project/Django/api/serializers.py
from rest_framework import serializers
from .models import User, IoTDevice, SensorData, ActuatorCommand


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class IoTDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = IoTDevice
        fields = '__all__'

class SensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorData
        fields = '__all__'

class ActuatorCommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActuatorCommand
        fields = '__all__'