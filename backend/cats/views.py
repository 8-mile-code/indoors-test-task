from rest_framework import viewsets

from .models import Cat
from .serializers import CatSerializer


class CatViewSet(viewsets.ModelViewSet):
    serializer_class = CatSerializer

    def get_queryset(self):
        return Cat.objects.filter(
            owner=self.request.user
            ).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
