import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from groqclass import GroqApiClass

# Initialize GroqApi with default settings
groq_api = GroqApiClass()

@csrf_exempt
@require_http_methods(["POST"])
def chat(request):
    try:
        data = json.loads(request.body)
        message = data.get('message', '')
        
        if not message:
            return JsonResponse({'error': 'Message is required'}, status=400)
            
        response = groq_api.get_completion(message)
        return JsonResponse({
            'message': response.choices[0].message.content
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Create your views here.
