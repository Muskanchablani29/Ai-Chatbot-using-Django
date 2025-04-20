from django.contrib import admin
from .models import ChatSession, ChatMessage

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'created_at', 'last_activity', 'user')
    search_fields = ('session_id', 'user__username')
    list_filter = ('created_at', 'last_activity')

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('session', 'content_preview', 'response_preview', 'created_at', 'is_error')
    list_filter = ('created_at', 'is_error', 'session')
    search_fields = ('content', 'response')

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    
    def response_preview(self, obj):
        return obj.response[:50] + '...' if len(obj.response) > 50 else obj.response

    content_preview.short_description = 'Content'
    response_preview.short_description = 'Response'
