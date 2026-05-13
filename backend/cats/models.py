from django.contrib.auth.models import User
from django.db import models


class Cat(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cats',
        verbose_name='Владелец',
    )
    name = models.CharField(
        'Имя',
        max_length=100,
    )
    age = models.PositiveIntegerField(
        'Возраст',
    )
    breed = models.CharField(
        'Порода',
        max_length=100,
        blank=True,
    )
    fluffiness = models.PositiveIntegerField(
        'Пушистость',
        default=1,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = 'Кот'
        verbose_name_plural = 'Коты'

    def __str__(self):
        return f'{self.name} ({self.owner.username})'
