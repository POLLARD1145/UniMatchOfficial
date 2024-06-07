# app/routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import re_path
from . import consumers


websocket_urlpatterns = [
    re_path(r'chat/$', consumers.ChatConsumer.as_asgi()),
]
