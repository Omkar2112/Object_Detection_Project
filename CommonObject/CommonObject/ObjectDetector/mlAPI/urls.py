from django.urls import path
from .views import Detect,show_logs,upload_picture

app_name = 'detect'

urlpatterns = [

    path('',Detect,name='detect'),
    path('logs/',show_logs, name='show_logs'),
    path('capture/',upload_picture,name='upload_picture'),


]