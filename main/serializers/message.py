from rest_framework import serializers
from ..models import Message
from .user import ProfileSerializer

class MessageSerializer(serializers.ModelSerializer):
     sender = ProfileSerializer()
     seens = ProfileSerializer(many=True)
     
     class Meta:
        model = Message 
        fields = ['id', 'sender', 'body', 'seens', 'isDeleted', 'created_at', 'updated_at']