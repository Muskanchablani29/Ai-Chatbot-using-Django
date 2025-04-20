from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Conversation, Message
import json

@csrf_exempt
def get_chat_history(request):
    if request.method == 'GET':
        conversations = Conversation.objects.all().order_by('-id')
        data = []
        for conv in conversations:
            messages = Message.objects.filter(conversation=conv).order_by('timestamp')
            messages_data = [{'content': msg.content, 'sender': msg.sender, 'timestamp': msg.timestamp.isoformat()} for msg in messages]
            data.append({
                'conversation_id': str(conv.id),
                'title': conv.title,
                'messages': messages_data,
            })
        return JsonResponse({'status': 'success', 'conversations': data})
    else:
        return JsonResponse({'status': 'error', 'error': 'Invalid request method'}, status=405)

@csrf_exempt
def delete_conversation(request, conversation_id):
    if request.method == 'DELETE':
        try:
            conversation = Conversation.objects.get(id=conversation_id)
            conversation.delete()
            return JsonResponse({'status': 'success', 'message': 'Conversation deleted'})
        except Conversation.DoesNotExist:
            return JsonResponse({'status': 'error', 'error': 'Conversation not found'}, status=404)
    else:
        return JsonResponse({'status': 'error', 'error': 'Invalid request method'}, status=405)

@csrf_exempt
def delete_all_conversations(request):
    if request.method == 'DELETE':
        Conversation.objects.all().delete()
        return JsonResponse({'status': 'success', 'message': 'All conversations deleted'})
    else:
        return JsonResponse({'status': 'error', 'error': 'Invalid request method'}, status=405)
