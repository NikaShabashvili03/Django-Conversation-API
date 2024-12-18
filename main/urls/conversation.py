# urls.py
from django.urls import path
from main.views.conversation import ConversationCreate, ConversationView, ConversationId

urlpatterns = [
    path('create/', ConversationCreate.as_view(), name='conversation-create'),
    path('list/', ConversationView.as_view(), name='conversation-list'),
    path('list/<int:id>/', ConversationId.as_view(), name='conversation-id')
]


