from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    #path('devices', views.devices, name='devices'),
    #path('configure', views.configure, name='configure'),
    path('deploy', views.deploy, name='deploy'),
    #path('verify_config', views.verify_config, name='verify_config'),
    path('about', views.about, name='about'),
    path('verify_result', views.verify_result, name='verify_result'),
    path('log', views.log, name='log'),
]
