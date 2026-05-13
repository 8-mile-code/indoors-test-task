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

    def validate_fluffiness(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError(
                'Fluffiness must be between 1 and 10.'
            )
        return value