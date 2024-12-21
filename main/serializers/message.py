from rest_framework import serializers
from ..models import Message, MessageImage, MessageReaction
from .user import ProfileSerializer

class MessageImageSerializer(serializers.ModelSerializer):
     url = serializers.ImageField(required=False)
     class Meta:
          model = MessageImage
          fields = ['url']

     def to_representation(self, instance):
         representation = super().to_representation(instance)
         if instance.url:
               representation['url'] = instance.url.url
         return representation
     
class MessageReactionSerializer(serializers.ModelSerializer):
     user = ProfileSerializer()
     class Meta:
          model = MessageReaction
          fields = ['emoji', 'user', 'created_at']
     
class MessageSerializer(serializers.ModelSerializer):
     sender = ProfileSerializer()
     seens = ProfileSerializer(many=True)
     images = MessageImageSerializer(many=True, read_only=True)
     reactions = MessageReactionSerializer(many=True, read_only=True)
     class Meta:
        model = Message 
        fields = ['id', 'sender', 'body', 'images', 'reactions', 'seens', 'isDeleted', 'isEdited', 'isReacted', 'created_at', 'updated_at']
     
     def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['isDeleted']:
            representation['body'] = None
        return representation
