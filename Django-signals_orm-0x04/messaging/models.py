from django.db import models
from django.contrib.auth.models import User


# -------------------------
# 🧠 Custom Manager
# -------------------------
class UnreadMessagesManager(models.Manager):
    """
    Custom manager to filter unread messages for a specific user.
    Optimized to retrieve only necessary fields.
    """
    def for_user(self, user):
        return (
            self.filter(receiver=user, read=False)
            .only("id", "sender", "content", "timestamp")
            .select_related("sender")  # optimization: fetch sender in one query
        )


# -------------------------
# 📬 Message Model
# -------------------------
class Message(models.Model):
    """
    Represents a message sent between users.
    Supports threaded replies and unread message tracking.
    """
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    read = models.BooleanField(default=False)  # ✅ New field for unread tracking

    # Self-referential field for threaded replies
    parent_message = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )

    # Attach custom manager
    objects = models.Manager()  # Default manager
    unread = UnreadMessagesManager()  # Custom manager

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}: {self.content[:30]}"

    def get_thread(self):
        """
        Recursively fetch all replies to this message.
        Uses ORM optimizations to reduce queries.
        """
        thread = []
        replies = self.replies.all().select_related("sender", "receiver").prefetch_related("replies")
        for reply in replies:
            thread.append(reply)
            thread.extend(reply.get_thread())
        return thread


# -------------------------
# 🕓 Message History
# -------------------------
class MessageHistory(models.Model):
    """
    Stores message edit history.
    Triggered by signals before a message update.
    """
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="history")
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History of Message ID {self.message.id} at {self.edited_at}"


# -------------------------
# 🔔 Notification Model
# -------------------------
class Notification(models.Model):
    """
    Notification model for user alerts.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.text[:30]}"
