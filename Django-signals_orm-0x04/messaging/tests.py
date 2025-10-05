from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification


class MessageSignalTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='alice', password='password123')
        self.receiver = User.objects.create_user(username='bob', password='password123')

    def test_notification_created_on_message(self):
        """Ensure that sending a message triggers a notification for the receiver."""
        Message.objects.create(sender=self.sender, receiver=self.receiver, content='Hello, Bob!')

        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.receiver)
        self.assertEqual(notification.message.content, 'Hello, Bob!')
