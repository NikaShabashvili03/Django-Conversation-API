from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Conversation, Message
from ..serializers.message import MessageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

class MessageCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, conversationId, *args, **kwargs):
        data = request.data
        user = request.user
        
        body = data.get("body")

        if not body:
            return Response({"detail": "Message body is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            conversation = Conversation.objects.get(id=conversationId)
        except Conversation.DoesNotExist:
            return Response({"detail": "Conversation not found"}, status=404)

        if user not in conversation.users.all():
            return Response({"detail": "You do not have permission to view this conversation."}, status=status.HTTP_403_FORBIDDEN)


        message = Message.objects.create(sender=user, body=body, conversation=conversation)
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
        
        message.isDeleted = True
        message.save()

        return Response(MessageSerializer(message).data)
    
class MessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, conversationId, *args, **kwargs):
        user = request.user
        limit = request.query_params.get('limit', 10)

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
        except Message.DoesNotExist:
            return Response({"detail": "Conversation not found"}, status=404)
        
        return Response(MessageSerializer(messages, many=True).data)
        