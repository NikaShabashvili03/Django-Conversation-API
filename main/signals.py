from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Message, MessageImage

@receiver(post_save, sender=Message)
def message(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    if not created:
        if (
                not instance.isDeleted == None or 
                instance.seens.all() or 
                not instance.isEdited == None or
                instance.isReacted
            ):
            async_to_sync(channel_layer.group_send)(
                f"messages_{instance.conversation.id}", 
                {
                    "type": "update_message",
                    "id": instance.id,
                }
            )
        else:
            async_to_sync(channel_layer.group_send)(
                f"messages_{instance.conversation.id}", 
                {
                    "type": "send_message",
                    "id": instance.id,
                }
            )

        
