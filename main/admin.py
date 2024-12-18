from django.contrib import admin
from .models import User, Session, Conversation, Message


admin.site.register(User)
admin.site.register(Session)
admin.site.register(Conversation)
admin.site.register(Message)

