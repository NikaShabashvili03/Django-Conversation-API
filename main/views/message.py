from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Conversation, Message, MessageImage, MessageReaction
from ..serializers.message import MessageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils.timezone import now
from datetime import timedelta

class MessageCreate(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, conversationId, *args, **kwargs):
        data = request.data
        user = request.user
        images = request.FILES.getlist("images")

        if (not data.get("body") and not images):
            return Response({"detail": "Message body or image is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        body = data.get("body")
        
        try:
            conversation = Conversation.objects.get(id=conversationId)
        except Conversation.DoesNotExist:
            return Response({"detail": "Conversation not found"}, status=404)

        if user not in conversation.users.all():
            return Response({"detail": "You do not have permission to view this conversation."}, status=status.HTTP_403_FORBIDDEN)

        message = Message.objects.create(sender=user, body=body or "", conversation=conversation)
        conversation.lastMessage = message
        conversation.save()
        for img in images:
            message_image = MessageImage(message=message, url=img)
            message_image.save()

        message.save()
        return Response(MessageSerializer(message).data)

class MessageSeen(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id, conversationId, *args, **kwargs):
        user = request.user

        try:
            conversation = Conversation.objects.get(id=conversationId)
        except Conversation.DoesNotExist:
            return Response({"detail": "Conversation not found"}, status=404)
        
        if user not in conversation.users.all():
            return Response({"detail": "You do not have permission to view this conversation."}, status=status.HTTP_403_FORBIDDEN)

        try:
            message = Message.objects.get(id=id)
        except Message.DoesNotExist:
            return Response({"detail": "Conversation not found"}, status=404)
        
        if message.sender == user:
            return Response({"detail": "You cant seen your message"}, status=status.HTTP_403_FORBIDDEN)
        
        if user in message.seens.all():
            return Response({"detail": "This message already seened"}, status=status.HTTP_403_FORBIDDEN)
        
        message.seens.add(user)
        message.save()

        conversation.lastMessage = message
        conversation.save()

        return Response(MessageSerializer(message).data)

class MessageReactionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id, conversationId, *args, **kwargs):
        user = request.user
        data = request.data

        if (not data.get("emoji")):
            return Response({"detail": "Message body or image is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        emoji = data.get("emoji")

        if len(emoji) > 1:
            return Response({"detail": "Please set emoji"}, status=404)
        try:
            conversation = Conversation.objects.get(id=conversationId)
        except Conversation.DoesNotExist:
            return Response({"detail": "Conversation not found"}, status=404)
        
        if user not in conversation.users.all():
            return Response({"detail": "You do not have permission to view this conversation."}, status=status.HTTP_403_FORBIDDEN)

        try:
            message = Message.objects.get(id=id)
        except Message.DoesNotExist:
            return Response({"detail": "Conversation not found"}, status=404)
    
        if message.sender == user:
            return Response({"detail": "You cant react your message"}, status=status.HTTP_403_FORBIDDEN)
        
        message.isReacted = True
        reaction = MessageReaction.objects.filter(message=message, user=user).first()

        if reaction:
            if reaction.emoji == emoji:
                reaction.delete()
                message.save()
                return Response(MessageSerializer(message).data)
            else:
                reaction.emoji = emoji
                reaction.save()
                message.save()
                return Response(MessageSerializer(message).data)
        
        create_reaction = MessageReaction.objects.create(message=message, user=user, emoji=emoji)
        create_reaction.save()
        message.save()


        conversation.lastMessage = message
        conversation.save()

        return Response(MessageSerializer(message).data)
    
class MessageEdit(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id, *args, **kwargs):
        user = request.user
        data = request.data

        if (not data.get("body")):
            return Response({"detail": "Message body is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        body = data.get("body")

        try:
            message = Message.objects.get(id=id, sender=user)
        except Message.DoesNotExist:
            return Response({"detail": "Message not found"}, status=404)

        if message.isDeleted:
            return Response({"detail": "You cannot edit deleted message"}, status=404)
        
        message.isEdited = now()
        message.body = body
        message.save()

        return Response(MessageSerializer(message).data)
    

class MessageDelete(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id, *args, **kwargs):
        user = request.user

        try:
            message = Message.objects.get(id=id, sender=user)
        except Message.DoesNotExist:
            return Response({"detail": "Message not found"}, status=404)

        if message.isDeleted:
            return Response({"details": "Message was deleted"}, status=404)
        
        message.isDeleted = now()
        message.save()

        return Response(MessageSerializer(message).data)

class MessageRecover(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id, *args, **kwargs):
        user = request.user

        try:
            message = Message.objects.get(id=id, sender=user)
        except Message.DoesNotExist:
            return Response({"detail": "Message not found"}, status=404)

        if not message.isDeleted:
            return Response({"details": "Message not deleted"}, status=404)
        
        time_difference = now() - message.isDeleted
        if time_difference > timedelta(minutes=5):
            return Response({"detail": "Message cannot be modified after 5 minutes."}, status=status.HTTP_400_BAD_REQUEST)
        
        message.isDeleted = None
        message.save()

        return Response(MessageSerializer(message).data)
    
class MessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, conversationId, *args, **kwargs):
        user = request.user
        limit = request.query_params.get('limit', 15)

        try:
            limit = int(limit)
        except ValueError:
            return Response({'error': 'Invalid limit parameter'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            conversation = Conversation.objects.get(id=conversationId)
        except Conversation.DoesNotExist:
            return Response({"detail": "Conversation not found"}, status=404)

        if user not in conversation.users.all():
            return Response({"detail": "You do not have permission to view this conversation."}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            messages = Message.objects.filter(conversation=conversation).distinct().order_by('-created_at')[:limit]
            messages = list(messages)[::-1]
        except Message.DoesNotExist:
            return Response({"detail": "Conversation not found"}, status=404)
        
        return Response(MessageSerializer(messages, many=True).data)
        