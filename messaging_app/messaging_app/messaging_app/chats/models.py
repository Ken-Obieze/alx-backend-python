import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# --------------------------
# Custom User Model
# --------------------------
class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser
    Adds UUID as primary key and extra fields (phone_number, role).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, db_index=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    ROLE_CHOICES = [
        ("guest", "Guest"),
        ("host", "Host"),
        ("admin", "Admin"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="guest")

    created_at = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        db_table = "users"
        indexes = [
            models.Index(fields=["email"]),
        ]

    def __str__(self):
        return f"{self.email} ({self.role})"


# --------------------------
# Conversation Model
# --------------------------
class Conversation(models.Model):
    """
    Conversation between multiple users.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "conversations"

    def __str__(self):
        return f"Conversation {self.id}"


# --------------------------
# Message Model
# --------------------------
class Message(models.Model):
    """
    Message sent by a user in a conversation.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    message_body = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "messages"
        ordering = ["sent_at"]

    def __str__(self):
        return f"Message from {self.sender.email} at {self.sent_at}"
