from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/<int:conversationId>/messages/', consumers.MessageConsumer.as_asgi()),
]
