from django.contrib import admin
from .models import SensorData, User, LED



admin.site.site_header = 'NISHANA SMART HOME PORTAL'
admin.site.site_title = 'Smart Home Admin Portal'
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


# Register the SensorData model
@admin.register(SensorData)  # Assuming SensorData is in the same app as LED and User models
class SensorDataAdmin(admin.ModelAdmin):
    list_display = ('sensor_name', 'sensor_type', 'value', 'unit', 'timestamp', 'user', 'device')
    search_fields = ('sensor_name', 'user__username')
    date_hierarchy = 'timestamp'
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)
    raw_id_fields = ('user', 'device')
    autocomplete_fields = ('user', 'device')
   
