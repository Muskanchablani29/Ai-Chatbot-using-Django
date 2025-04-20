from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from .models import ChatSession, ChatMessage
import json
import google.generativeai as genai

# ✅ Configure Gemini API Key
genai.configure(api_key="AIzaSyBFuikHl1HHID9r2hzqCsr7yht1xa67J5I")  

# Initialize the model
model = genai.GenerativeModel("models/gemini-1.5-pro")

def get_or_create_session(request):
    if not request.session.session_key:
        request.session.create()
    
    session_id = request.session.session_key
    chat_session, created = ChatSession.objects.get_or_create(
        session_id=session_id,
        defaults={'user': request.user if request.user.is_authenticated else None}
    )
    return chat_session

def Chat(request):
    return render(request, 'ChatPage.html')

@csrf_exempt
def gemini_chat_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            prompt = data.get("message", "")
            if not prompt:
                return JsonResponse({"response": "Error: No message provided"}, status=400)
            
            chat_session = get_or_create_session(request)
            
            response = model.generate_content(prompt)
            response_text = response.text
            
            ChatMessage.objects.create(
                session=chat_session,
                content=prompt,
                response=response_text,
                is_error=False
            )
            
            return JsonResponse({
                "response": response_text,
                "timestamp": response.timestamp if hasattr(response, "timestamp") else None
            })
        except Exception as e:
            print(f"Error: {e}")
            
            try:
                chat_session = get_or_create_session(request)
                ChatMessage.objects.create(
                    session=chat_session,
                    content=prompt if 'prompt' in locals() else "",
                    response=f"Error: {str(e)}",
                    is_error=True
                )
            except Exception as db_error:
                print(f"Database Error: {db_error}")
                
            return JsonResponse({"response": f"Error: {str(e)}"}, status=500)
    return JsonResponse({"response": "Invalid request method"}, status=405)

@csrf_exempt
def list_models(request):
    try:
        models = genai.list_models()
        model_list = [
            {
                "name": model.name,
                "methods": model.supported_generation_methods
            }
            for model in models
        ]
        return JsonResponse({"models": model_list})
    except Exception as e:
        return JsonResponse({"error": f"Error: {str(e)}"})

@csrf_exempt
def chat_history(request):
    try:
        chat_session = get_or_create_session(request)
        messages = ChatMessage.objects.filter(session=chat_session)
        
        history = [{
            'content': msg.content,
            'response': msg.response,
            'created_at': msg.created_at.isoformat(),
            'is_error': msg.is_error
        } for msg in messages]
        
        return JsonResponse({'history': history})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def clear_history(request):
    try:
        chat_session = get_or_create_session(request)
        ChatMessage.objects.filter(session=chat_session).delete()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
