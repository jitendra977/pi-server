
from rest_framework import serializers
from .models import SensorData, User, LED

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class LEDSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LED
        fields = '__all__'

class SensorDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SensorData
        fields = '__all__'

        