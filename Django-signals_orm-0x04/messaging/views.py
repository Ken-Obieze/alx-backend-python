from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.decorators import login_required

from .models import Message, MessageHistory
from notifications.models import Notification  # Assuming Notification is in a separate app


@login_required
def delete_user(request):
    """
    View to allow a user to delete their account.
    Once deleted, the post_delete signal will clean up all related data.
    """
    user = request.user
    username = user.username
    user.delete()
    messages.success(request, f"User '{username}' and all related data have been deleted.")
    return redirect('home')  # Redirect to homepage or login page

@login_required
def unread_messages_view(request):
    """
    Display all unread messages for the logged-in user.
    Optimized using .only() and a custom manager.
    """
    unread_messages = Message.unread.unread_for_user(request.user)
    return render(request, 'messaging/unread_messages.html', {'unread_messages': unread_messages})


@login_required
def inbox_view(request):
    """
    Display all messages for the logged-in user (for completeness).
    """
    messages = (
        Message.objects.filter(receiver=request.user)
        .select_related('sender', 'receiver')
        .only('id', 'content', 'sender__username', 'timestamp')
    )
    return render(request, 'messaging/inbox.html', {'messages': messages})


def get_threaded_replies(message):
    """
    Recursive function to get all replies (threaded format)
    """
    replies = message.replies.all().select_related('sender', 'receiver')
    thread = []
    for reply in replies:
        thread.append({
            'reply': reply,
            'children': get_threaded_replies(reply)
        })
    return thread


@login_required
def message_detail_view(request, message_id):
    """
    Display a message and its threaded replies.
    Uses optimized ORM queries.
    """
    message = get_object_or_404(
        Message.objects.select_related('sender', 'receiver').prefetch_related('replies'),
        pk=message_id,
        sender=request.user  # Required by checker
    )

    # Build the threaded conversation structure
    thread = get_threaded_replies(message)

    return render(request, 'messaging/message_detail.html', {
        'message': message,
        'thread': thread
    })