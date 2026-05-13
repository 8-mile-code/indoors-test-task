from rest_framework import serializers

from .models import Cat


class CatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cat
        fields = (
            'id',
            'name',
            'age',
            'breed',
            'fluffiness',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'created_at',
            'updated_at',
        )
