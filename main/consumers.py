import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.shortcuts import get_object_or_404
class MessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversationId']
        self.group_name = f"messages_{self.conversation_id}"
        user = self.scope['user']

        conversation = await sync_to_async(self.get_conversation)()
        if user not in await sync_to_async(self.get_conversation_users)(conversation):
            await self.close(code=403)
            return
        
        
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_message(self, event):
        message = await sync_to_async(self.get_serialized_message)(event['id'])
        await self.send(text_data=json.dumps({
            "message": message,
            "action": "create"
        }))
    
    async def update_message(self, event):
        message = await sync_to_async(self.get_serialized_message)(event['id'])
        await self.send(text_data=json.dumps({
            "message": message,
            "action": "update"
        }))
    
    def get_serialized_message(self, id):
        from .models import Message
        from .serializers.message import MessageSerializer

        try:
            message_instance = Message.objects.get(id=id)
        except Message.DoesNotExist:
            return None
        
        message_data = MessageSerializer(message_instance).data
        return message_data

    def get_conversation(self):
        from .models.conversation import Conversation
        return get_object_or_404(Conversation, id=self.conversation_id)
    
    def get_conversation_users(self, conversation):
        return list(conversation.users.all())