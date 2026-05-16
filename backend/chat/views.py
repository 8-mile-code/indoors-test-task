from django.db.models import Q
from rest_framework import viewsets

from .models import Message
from .serializers import MessageSerializer


class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(
            Q(sender=self.request.user) | Q(receiver=self.request.user)
        ).select_related(
            'sender',
            'receiver',
        )
