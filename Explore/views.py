from django.shortcuts import render

import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os

# Create your views here.

def Explore(request):
    return render(request, 'Explore.html')


# Replace with your actual Gemini API key
GEMINI_API_KEY = "AIzaSyBFuikHl1HHID9r2hzqCsr7yht1xa67J5I"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")

import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def fix_code(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            code = data.get("code", "")
            logger.info(f"Received code to fix: {code[:100]}")  # Log first 100 chars
            prompt = f"Please fix the following code and explain the error:\n\n{code}"
            response = model.generate_content(prompt)
            logger.info("Generated response from model")
            return JsonResponse({"result": response.text})
        except Exception as e:
            logger.error(f"Error in fix_code: {str(e)}")
            return JsonResponse({"error": "Failed to generate fixed code", "details": str(e)}, status=500)

@csrf_exempt
def generate_code(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            lang = data.get("lang", "python")
            prompt = data.get("prompt", "")
            logger.info(f"Received generate code request: lang={lang}, prompt={prompt[:100]}")
            final_prompt = f"Write a {lang} code for: {prompt}"
            response = model.generate_content(final_prompt)
            logger.info("Generated response from model for generate_code")
            return JsonResponse({"result": response.text})
        except Exception as e:
            logger.error(f"Error in generate_code: {str(e)}")
            return JsonResponse({"error": "Failed to generate code", "details": str(e)}, status=500)
