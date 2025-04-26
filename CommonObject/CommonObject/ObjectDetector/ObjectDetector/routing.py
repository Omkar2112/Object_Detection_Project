from django.urls import path
from . import consumers
websockt_urls = [
    path("ws/detect/",consumers.SendDetectionConsumer.as_asgi())
]