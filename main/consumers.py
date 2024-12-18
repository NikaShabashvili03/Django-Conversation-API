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
        sender_data = await sync_to_async(self.get_serialized_sender)(event['sender'])
        seens_data = await sync_to_async(self.get_serialized_seens)(event['seens'])
        await self.send(text_data=json.dumps({
            "message": {
                'id': event['id'],
                'created_at': event['created_at'],
                'updated_at': event['updated_at'],
                'body': event['body'],
                'isDeleted': event['isDeleted'],
                'sender': sender_data,
                'seens': seens_data
            },
            "action": "create"
        }))
    
    async def delete_message(self, event):
        sender_data = await sync_to_async(self.get_serialized_sender)(event['sender'])
        seens_data = await sync_to_async(self.get_serialized_seens)(event['seens'])
        await self.send(text_data=json.dumps({
            "message": {
                'id': event['id'],
                'created_at': event['created_at'],
                'updated_at': event['updated_at'],
                'body': event['body'],
                'isDeleted': event['isDeleted'],
                'sender': sender_data,
                'seens': seens_data
            },
            "action": "update"
        }))

    def get_serialized_seens(self, seens):
        from .serializers.user import ProfileSerializer
        return ProfileSerializer(seens, many=True).data
    
    def get_serialized_sender(self, sender):
        from .serializers.user import ProfileSerializer
        return ProfileSerializer(sender).data
    
    def get_conversation(self):
        from .models.conversation import Conversation
        return get_object_or_404(Conversation, id=self.conversation_id)
    
    def get_conversation_users(self, conversation):
        return list(conversation.users.all())