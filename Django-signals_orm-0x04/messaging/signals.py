from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, MessageHistory
from notifications.models import Notification

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """Automatically create a notification when a new message is received."""
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(post_delete, sender=User)
def delete_related_user_data(sender, instance, **kwargs):
    """
    Signal to clean up user-related data when a user is deleted.
    Triggered automatically after a User instance is deleted.
    """
    # Delete all messages sent or received by the user
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete notifications related to the user
    Notification.objects.filter(user=instance).delete()

    # Delete message histories linked to the user’s messages
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()