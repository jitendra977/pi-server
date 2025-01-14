from django.db import models

class User(models.Model):
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)  # Consider using Django's User model for secure password handling
    email = models.EmailField(max_length=200, unique=True)
    phone = models.PositiveIntegerField(default=0)
    started = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class LED(models.Model):
    name = models.CharField(max_length=200, unique=True)
    led_pin = models.PositiveIntegerField(default=0)  # GPIO pin for controlling the LED
    status = models.BooleanField(default=False)  # LED status (on/off)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    button_pin = models.PositiveIntegerField(default=0)  # GPIO pin for the button

    def __str__(self):
        return self.name

class SensorData(models.Model):
    SENSOR_TYPES = [
        ('temperature', 'Temperature'),
        ('humidity', 'Humidity'),
        ('motion', 'Motion'),
        ('light', 'Light'),
        # Add more sensor types as needed
    ]
    
    sensor_name = models.CharField(max_length=200)
    sensor_type = models.CharField(max_length=50, choices=SENSOR_TYPES)
    value = models.FloatField()
    unit = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    device = models.ForeignKey(LED, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.sensor_name} - {self.value} {self.unit} ({self.sensor_type}) at {self.timestamp}"