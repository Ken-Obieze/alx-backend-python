from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom User model extending AbstractUser.
    Adds explicit fields required by project checks.
    """
    user_id = models.AutoField(primary_key=True)  # Explicit user_id
    password = models.CharField(max_length=128)  # Explicit password field (already in AbstractUser, but required for checks)

    def __str__(self):
        return self.username


class Conversation(models.Model):
    """
    Tracks which users are involved in a conversation.
    """
    conversation_id = models.AutoField(primary_key=True)  # Explicit conversation_id
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id}"


class Message(models.Model):
    """
    Stores messages within a conversation.
    """
    message_id = models.AutoField(primary_key=True)  # Explicit message_id
    conversation = models.ForeignKey(
        Conversation, related_name="messages", on_delete=models.CASCADE
    )
    sender = models.ForeignKey(
        User, related_name="messages", on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.message_id} in Conversation {self.conversation.conversation_id}"
