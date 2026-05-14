from django.contrib import admin

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'sender',
        'receiver',
        'text',
        'created_at',
    )
    list_filter = (
        'created_at',
    )
    search_fields = (
        'sender__username',
        'receiver__username',
        'text',
    )
