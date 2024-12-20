from . import User
from django.db import models

class Conversation(models.Model):
    users = models.ManyToManyField(User, related_name="conversations")

    name = models.CharField(max_length=255, null=True, blank=True)

    lastMessage = models.ForeignKey(
        'main.Message',
        on_delete=models.SET_NULL,
        related_name="conversation_lastmessage",
        null=True,
        blank=True
    )
    
    isGroup = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Conversation {self.id} {self.name or self.users.first()}"