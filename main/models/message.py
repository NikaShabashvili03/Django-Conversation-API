from . import Conversation, User
from django.db import models

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    seens = models.ManyToManyField(User, related_name="seens")
    body = models.CharField(max_length=255, null=False, blank=False)
    isDeleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sender.firstname} | {self.body} / {self.created_at}"