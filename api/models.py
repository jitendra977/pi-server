from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, help_text="Enter the username")
    password = models.CharField(max_length=255, help_text="Enter the password")  # Increased max_length for better security
    email = models.EmailField(unique=True, max_length=100, help_text="Enter the email address")
    first_name = models.CharField(max_length=100, help_text="Enter the first name")
    last_name = models.CharField(max_length=100, help_text="Enter the last name")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['username']

class IoTDevice(models.Model):
    DEVICE_TYPES = [
        ('sensor', 'Sensor'),
        ('actuator', 'Actuator'),
    ]

    device_name = models.CharField(max_length=100, help_text="Enter the device name")
    device_type = models.CharField(max_length=8, choices=DEVICE_TYPES, help_text="Select the device type")  # Reduced max_length
    device_status = models.BooleanField(default=False, help_text="Indicate the device status")
    device_location = models.CharField(max_length=100, help_text="Enter the device location")
    device_last_updated = models.DateTimeField(auto_now=True)
    device_owner = models.ForeignKey(User, related_name='devices', on_delete=models.CASCADE, help_text="Select the device owner")

    def __str__(self):
        return self.device_name

    class Meta:
        verbose_name = "IoT Device"
        verbose_name_plural = "IoT Devices"
        ordering = ['device_name']

class GPIOPin(models.Model):
    pin_number = models.PositiveIntegerField(unique=True, help_text="Enter the GPIO pin number")  # Changed to PositiveIntegerField
    device = models.ForeignKey(IoTDevice, related_name='gpio_pins', on_delete=models.CASCADE, help_text="Select the associated device")

    def __str__(self):
        return f"GPIO {self.pin_number} for {self.device.device_name}"

    class Meta:
        verbose_name = "GPIO Pin"
        verbose_name_plural = "GPIO Pins"
        ordering = ['pin_number']

class SensorData(models.Model):
    device = models.ForeignKey(IoTDevice, related_name='sensor_data', on_delete=models.CASCADE, help_text="Select the associated device")
    timestamp = models.DateTimeField(auto_now_add=True)
    data = models.JSONField(help_text="Enter the sensor data in JSON format")

    def __str__(self):
        return f"Data from {self.device.device_name} at {self.timestamp}"

    class Meta:
        verbose_name = "Sensor Data"
        verbose_name_plural = "Sensor Data"
        ordering = ['-timestamp']

class ActuatorCommand(models.Model):
    device = models.ForeignKey(IoTDevice, related_name='actuator_commands', on_delete=models.CASCADE, help_text="Select the associated device")
    timestamp = models.DateTimeField(auto_now_add=True)
    command = models.CharField(max_length=100, help_text="Enter the actuator command")

    def __str__(self):
        return f"Command to {self.device.device_name} at {self.timestamp}"

    class Meta:
        verbose_name = "Actuator Command"
        verbose_name_plural = "Actuator Commands"
        ordering = ['-timestamp']