from django.shortcuts import redirect
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
