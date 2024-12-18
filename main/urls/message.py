# urls.py
from django.urls import path
from main.views.message import MessageCreate, MessagesView, MessageDelete, MessageSeen

urlpatterns = [
    path('<int:conversationId>/create/', MessageCreate.as_view(), name='message-create'),
    path('delete/<int:id>', MessageDelete.as_view(), name='message-delete'),
    path('<int:conversationId>/all/', MessagesView.as_view(), name='message-list'),
    path('<int:conversationId>/seen/<int:id>', MessageSeen.as_view(), name='message-seen')
]


