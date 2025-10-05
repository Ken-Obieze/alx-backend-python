from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page
from messaging.models import Message

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Conversations
    """
    queryset = Conversation.objects.all().prefetch_related("participants", "messages")
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["participants__username"]
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with participants
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()
        return Response(
            ConversationSerializer(conversation).data,
            status=status.HTTP_201_CREATED
        )
    
    def get_queryset(self):
        # Only return conversations where the user is a participant
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Messages
    """
    queryset = Message.objects.all().select_related("conversation", "sender")
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["content", "sender__username"]
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = MessageFilter
    ordering_fields = ["sent_at"]
    search_fields = ["message_body"]

    def get_queryset(self):
        conversation_id = self.kwargs.get("conversation_id")
        conversation = get_object_or_404(Conversation, id=conversation_id)

        # Ensure user is a participant
        if self.request.user not in conversation.participants.all():
            return Message.objects.none()  # hide from non-participants

        return Message.objects.filter(conversation=conversation)

    def create(self, request, *args, **kwargs):
        conversation_id = self.kwargs.get("conversation_id")
        conversation = get_object_or_404(Conversation, id=conversation_id)

        # Explicit 403 if user not in conversation
        if request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant of this conversation."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=request.user, conversation=conversation)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

# ⏱️ Cache this view for 60 seconds
@cache_page(60)
def conversation_view(request, username):
    """
    Displays a conversation between the logged-in user and another user.
    Cached for 60 seconds to improve performance.
    """
    other_user = get_object_or_404(User, username=username)

    # Fetch messages for this conversation
    messages = (
        Message.objects.filter(
            (models.Q(sender=request.user, receiver=other_user) |
             models.Q(sender=other_user, receiver=request.user))
        )
        .select_related("sender", "receiver")
        .order_by("timestamp")
    )

    return render(request, "chats/conversation.html", {
        "other_user": other_user,
        "messages": messages,
    })