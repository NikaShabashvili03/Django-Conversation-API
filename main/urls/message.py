# urls.py
from django.urls import path
from main.views.message import MessageCreate, MessagesView, MessageDelete, MessageEdit, MessageSeen, MessageRecover, MessageReactionView

urlpatterns = [
    path('<int:conversationId>/create/', MessageCreate.as_view(), name='message-create'),
    path('delete/<int:id>', MessageDelete.as_view(), name='message-delete'),
    path('edit/<int:id>', MessageEdit.as_view(), name='message-edit'),
    path('<int:conversationId>/reaction/<int:id>', MessageReactionView.as_view(), name='message-create-reaction'),
    path('recover/<int:id>', MessageRecover.as_view(), name='message-recover'),
    path('<int:conversationId>/all/', MessagesView.as_view(), name='message-list'),
    path('<int:conversationId>/seen/<int:id>', MessageSeen.as_view(), name='message-seen')
]


