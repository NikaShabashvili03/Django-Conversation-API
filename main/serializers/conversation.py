from rest_framework import serializers
from ..models import Conversation
from .user import ProfileSerializer
from .message import MessageSerializer

class ConversationSerializer(serializers.ModelSerializer):
    users = ProfileSerializer(many=True)
    lastMessage = MessageSerializer()

    class Meta:
        model = Conversation 
        fields = ['id', 'name', 'isGroup', 'users', 'created_at', 'lastMessage', 'updated_at']