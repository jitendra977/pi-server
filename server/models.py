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