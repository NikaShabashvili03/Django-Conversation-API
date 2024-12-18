from . import Conversation, User
from django.db import models
from ..utils import image_upload, validate_image


def upload_image(instance, filename):
    return image_upload(instance, filename, 'message/')

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    seens = models.ManyToManyField(User, related_name="seens")
    body = models.CharField(max_length=255, null=False, blank=False)

    isReacted = models.BooleanField(default=False)
    isDeleted = models.DateTimeField(auto_now=False, null=True, blank=True, default=None)
    isEdited = models.DateTimeField(auto_now=False, null=True, blank=True, default=None)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sender.firstname} | {self.body} / {self.created_at}"
    

class MessageReaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name='reactions', on_delete=models.CASCADE)
    emoji = models.CharField(max_length=1, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'message', 'emoji')

    def __str__(self):
        return f"{self.user.firstname} reacted to message {self.message.body} with {self.emoji}"

class MessageImage(models.Model):
    message = models.ForeignKey(Message, related_name='images', on_delete=models.CASCADE)
    url = models.ImageField(upload_to=upload_image, null=True, blank=True)

    def clean(self):
        if self.url:
            validate_image(self.url, 4000, 4000, 4000)