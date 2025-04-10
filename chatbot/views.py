import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from groqclass import GroqApiClass

# Dictionary to store GroqApiClass instances
groq_instances = {}

@csrf_exempt
@require_http_methods(["POST"])
def chat(request):
    try:
        data = json.loads(request.body)
        message = data.get('message', '')
        
        if not message:
            return JsonResponse({'error': 'Message is required'}, status=400)
        
        # Get or create user's GroqApiClass instance using session key
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
            
        if session_key not in groq_instances:
            groq_instances[session_key] = GroqApiClass(max_messages=4)
        
        groq_api = groq_instances[session_key]
        response = groq_api.get_completion(message)
        
        return JsonResponse({
            'message': response.choices[0].message.content
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Create your views here.
