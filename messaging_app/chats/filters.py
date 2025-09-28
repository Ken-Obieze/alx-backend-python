import django_filters
from .models import Message


class MessageFilter(django_filters.FilterSet):
    sent_before = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr="lte")
    sent_after = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr="gte")

    class Meta:
        model = Message
        fields = ["sender", "conversation", "sent_before", "sent_after"]