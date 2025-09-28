from rest_framework.permissions import BasePermission
from rest_framework.permissions import BasePermission, IsAuthenticated

class IsOwner(BasePermission):
    """
    Custom permission: Only allow users to access their own objects
    (e.g., conversations, messages).
    """

    def has_object_permission(self, request, view, obj):
        # For Message model
        if hasattr(obj, "sender"):
            return obj.sender == request.user

        # For Conversation model
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()

        return False

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to allow only participants of a conversation
    to view, send, update, or delete messages.
    """

    def has_object_permission(self, request, view, obj):
        # Ensure the user is authenticated first
        if not request.user or not request.user.is_authenticated:
            return False

        # For Conversation objects
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()

        # For Message objects (assumes Message has a conversation FK)
        if hasattr(obj, "conversation"):
            return request.user in obj.conversation.participants.all()

        return False