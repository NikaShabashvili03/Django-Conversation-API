from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/<int:conversationId>/messages/', consumers.MessageConsumer.as_asgi()),
    path('ws/online/', consumers.OnlineConsumer.as_asgi()),
    path('ws/conversation/', consumers.ConversationConsumer.as_asgi())
]
