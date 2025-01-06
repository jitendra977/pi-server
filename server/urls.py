from django.urls import include, path
from rest_framework import routers
from . import views 


routers = routers.DefaultRouter()

routers.register(r'users',views.UserViewSet)
routers.register(r'leds',views.LEDViewSet)


urlpatterns = [
      path('',include(routers.urls)),
          

]
