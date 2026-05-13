from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.permissions import IsOwner

from .models import Cat
from .serializers import CatSerializer


class CatViewSet(viewsets.ModelViewSet):
    serializer_class = CatSerializer
    permission_classes = (IsAuthenticated, IsOwner,)

    def get_queryset(self):
        return Cat.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
