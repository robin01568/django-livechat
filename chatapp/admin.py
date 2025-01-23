from django.contrib import admin
from .models import ChatRoom, Message

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('room', 'sender', 'content', 'timestamp')
    list_filter = ('room', 'timestamp')
    search_fields = ('content', 'sender__username')
