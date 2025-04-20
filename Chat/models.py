from django.db import models
from django.conf import settings  # Import settings instead of User model

class ChatSession(models.Model):
    session_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Use AUTH_USER_MODEL instead of User
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-last_activity']

    def __str__(self):
        return f"Chat Session {self.session_id}"

class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_error = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.created_at}: {self.content[:50]}"
