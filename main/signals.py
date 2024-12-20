from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Message, Conversation


@receiver(post_save, sender=Conversation)
def conversation(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    user_ids = instance.users.values_list('id', flat=True)
    if created:
        for user_id in user_ids: 
            async_to_sync(channel_layer.group_send)(
                f"conversations_{user_id}",
                {
                    "type": "create_conversation",
                    "id": instance.id,
                }
            )
    else:
        for user_id in user_ids: 
            async_to_sync(channel_layer.group_send)(
                f"conversations_{user_id}",
                {
                    "type": "update_conversation",
                    "id": instance.id,
                }
            )

@receiver(post_save, sender=Message)
def message(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    print(instance.seens.all())
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

        
