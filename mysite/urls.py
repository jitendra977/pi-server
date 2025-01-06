# myproject/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('server.urls')),
    # path('api/', include('api.urls')),  # Include the API URLs here
]