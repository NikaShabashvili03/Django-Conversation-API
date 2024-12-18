from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Message

@receiver(post_save, sender=Message)
def message(sender, instance, created, **kwargs):
    event_type = 'created' if created else 'updated'
    channel_layer = get_channel_layer()

    if event_type == 'created':
        async_to_sync(channel_layer.group_send)(
            f"messages_{instance.conversation.id}", 
                {
                    "type": "send_message",
                    "id": instance.id,
                    "created_at": instance.created_at.isoformat(),
                    "updated_at": instance.updated_at.isoformat(),
                    "body": instance.body,
                    "isDeleted": instance.isDeleted,
                    "seens": instance.seens,
                    "sender": instance.sender
                }
            )

    if event_type == 'updated':
        async_to_sync(channel_layer.group_send)(
            f"messages_{instance.conversation.id}", 
            {
                "type": "delete_message",
                "id": instance.id,
                "created_at": instance.created_at.isoformat(),
                "updated_at": instance.updated_at.isoformat(),
                "body": instance.body,
                "isDeleted": instance.isDeleted,
                "seens": instance.seens,
                "sender": instance.sender
            }
        )
