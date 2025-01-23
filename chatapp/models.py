from django.db import models
from django.contrib.auth.models import User


class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Unique room name or identifier
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    sender_ip = models.GenericIPAddressField(null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender} in {self.room}: {self.content[:20]}'
