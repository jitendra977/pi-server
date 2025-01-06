from django.contrib import admin
from .models import User, LED

# Register the User model
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'started')
    search_fields = ('username', 'email')
    list_filter = ('started',)

# Register the LED model
@admin.register(LED)
class LEDAdmin(admin.ModelAdmin):
    list_display = ('name', 'led_pin', 'status', 'button_pin', 'user')
    search_fields = ('name', 'user__username')
    list_filter = ('status', 'user')