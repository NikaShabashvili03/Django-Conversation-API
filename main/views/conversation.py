from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Conversation, User, Message
from rest_framework import status
from ..serializers.conversation import ConversationSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Max, Prefetch
from django.shortcuts import get_object_or_404

class ConversationCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        creator = request.user

        user_ids = data.get("users")
    
        if not isinstance(user_ids, list):
            return Response({"detail": "Users must be a list."}, status=status.HTTP_400_BAD_REQUEST)

        user_ids.append(creator.id)
        unique_user_ids = list(set(user_ids))
        users = User.objects.filter(id__in=unique_user_ids)

        if not users.exists():
            return Response({"detail": "No valid users found."}, status=status.HTTP_400_BAD_REQUEST)

        if len(users) == 2:
            isGroup = False
            other_user = users.exclude(id=creator.id).first()
            
            existing_conversation = Conversation.objects.filter(
                isGroup=False
            ).filter(
                users=other_user
            ) | Conversation.objects.filter(
                isGroup=False
            ).filter(
                users=creator
            )

            if existing_conversation.exists():
                return Response(ConversationSerializer(existing_conversation.first()).data, status=status.HTTP_200_OK)
            conversation = Conversation.objects.create(isGroup=False)
            conversation.users.set(users)
            return Response(ConversationSerializer(conversation).data, status=status.HTTP_201_CREATED)

        elif len(user_ids) > 2:
            isGroup = True
            name = data.get("name", "Untitled Group")
            conversation = Conversation.objects.create(name=name, isGroup=isGroup)
            conversation.users.set(users)
            return Response(ConversationSerializer(conversation).data, status=status.HTTP_201_CREATED)
        

class ConversationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        isGroup = self.request.query_params.get('isGroup', 'false')

        if isGroup == 'true':
            isGroup = True
        elif isGroup == 'false':
            isGroup = False

        conversations = Conversation.objects.filter(
            Q(users=user) & Q(isGroup=isGroup)
        ).distinct()

        conversations = conversations.annotate(last_message_time=Max('messages__created_at'))

        conversations = conversations.prefetch_related(
            Prefetch('messages', queryset=Message.objects.filter(
                created_at__in=conversations.values('last_message_time')
            ))
        )

        serialized_conversations = ConversationSerializer(conversations, many=True)

        return Response(serialized_conversations.data, status=200)
    
class ConversationId(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id, *args, **kwargs):
        conversation = get_object_or_404(
            Conversation.objects.filter(users=request.user),
            id=id
        )
        
        return Response(ConversationSerializer(conversation).data)