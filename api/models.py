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

class Firmware(models.Model):
    version = models.CharField(max_length=50, unique=True, help_text="Enter the firmware version")
    release_date = models.DateField(help_text="Enter the release date of the firmware")
    description = models.TextField(help_text="Enter the description of the firmware")

    def __str__(self):
        return self.version

    class Meta:
        verbose_name = "Firmware"
        verbose_name_plural = "Firmwares"
        ordering = ['-release_date']

class IoTDevice(models.Model):
    DEVICE_TYPES = [
        ('sensor', 'Sensor'),
        ('actuator', 'Actuator'),
    ]

    device_name = models.CharField(max_length=100, help_text="Enter the device name")
    device_type = models.CharField(max_length=8, choices=DEVICE_TYPES, help_text="Select the device type")
    device_status = models.BooleanField(default=False, help_text="Indicate the device status")
    device_location = models.CharField(max_length=100, help_text="Enter the device location")
    device_last_updated = models.DateTimeField(auto_now=True)
    device_owner = models.ForeignKey(User, related_name='devices', on_delete=models.CASCADE, help_text="Select the device owner")
    firmware = models.ForeignKey(Firmware, related_name='devices', on_delete=models.SET_NULL, null=True, help_text="Select the firmware version")

    def __str__(self):
        return self.device_name

    class Meta:
        verbose_name = "IoT Device"
        verbose_name_plural = "IoT Devices"
        ordering = ['device_name']

class GPIOPin(models.Model):
    pin_number = models.PositiveIntegerField(unique=True, help_text="Enter the GPIO pin number")
    device = models.ForeignKey(IoTDevice, related_name='gpio_pins', on_delete=models.CASCADE, help_text="Select the associated device")
    is_led = models.BooleanField(default=False, help_text="Indicates if the pin is connected to an LED")

    def __str__(self):
        return f"GPIO {self.pin_number} for {self.device.device_name}"

    class Meta:
        verbose_name = "GPIO Pin"
        verbose_name_plural = "GPIO Pins"
        ordering = ['pin_number']

class Button(models.Model):
    gpio_pin = models.OneToOneField(GPIOPin, related_name='button', on_delete=models.CASCADE, help_text="Select the GPIO pin for this button")
    button_status = models.BooleanField(default=False, help_text="The current state of the button (pressed or not)")
    device = models.ForeignKey(IoTDevice, related_name='buttons', on_delete=models.CASCADE, help_text="Select the associated IoT device")

    def __str__(self):
        return f"Button for {self.device.device_name}"

    class Meta:
        verbose_name = "Button"
        verbose_name_plural = "Buttons"

class LED(models.Model):
    gpio_pin = models.OneToOneField(GPIOPin, related_name='led', on_delete=models.CASCADE, help_text="Select the GPIO pin for this LED")
    led_status = models.BooleanField(default=False, help_text="The current state of the LED (on or off)")
    device = models.ForeignKey(IoTDevice, related_name='leds', on_delete=models.CASCADE, help_text="Select the associated IoT device")

    def __str__(self):
        return f"LED for {self.device.device_name}"

    class Meta:
        verbose_name = "LED"
        verbose_name_plural = "LEDs"

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

class DeviceLog(models.Model):
    device = models.ForeignKey(IoTDevice, related_name='logs', on_delete=models.CASCADE, help_text="Select the associated device")
    timestamp = models.DateTimeField(auto_now_add=True)
    log_entry = models.TextField(help_text="Enter the log entry")

    def __str__(self):
        return f"Log for {self.device.device_name} at {self.timestamp}"

    class Meta:
        verbose_name = "Device Log"
        verbose_name_plural = "Device Logs"
        ordering = ['-timestamp']

class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE, help_text="Select the user to notify")
    message = models.TextField(help_text="Enter the notification message")
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False, help_text="Indicate if the notification has been read")

    def __str__(self):
        return f"Notification for {self.user.username} at {self.timestamp}"

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-timestamp']