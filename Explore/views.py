import json
import google.generativeai as genai
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token

# Use the same API key as Chat app for consistency
GEMINI_API_KEY = "AIzaSyDSbisde1SZQEinxeEdwkTbCM99IRDsoe8"

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    model = None

def explore_view(request):
    # Generate CSRF token
    get_token(request)
    return render(request, 'Explore.html')

@csrf_exempt
def generate_code(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            prompt = data.get('prompt')
            language = data.get('language')

            if not model:
                return JsonResponse({"error": "Gemini API not configured"}, status=500)

            if not prompt:
                return JsonResponse({"error": "No prompt provided"}, status=400)

            if language == 'fullpage':
                full_prompt = f"""
Generate a complete, well-structured HTML page with embedded CSS and JavaScript for the following requirement:
{prompt}

Provide the full HTML code including <html>, <head>, and <body> tags.
Ensure the CSS and JavaScript are included within the page.
Do not include explanations or markdown formatting.
"""
            else:
                full_prompt = f"""
Generate {language} code for the following requirement:
{prompt}

Provide only the code without any explanations or markdown formatting.
Ensure the code is well-commented and follows best practices.
"""

            response = model.generate_content(full_prompt)
            generated_code = response.text.strip()

            # Clean the response if it contains markdown code blocks
            if generated_code.startswith('```'):
                lines = generated_code.split('\n')
                if len(lines) > 2:
                    generated_code = '\n'.join(lines[1:-1])

            return JsonResponse({"code": generated_code})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def fix_code(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_code = data.get('code')

            if not model:
                return JsonResponse({"error": "Gemini API not configured"}, status=500)

            if not user_code:
                return JsonResponse({"error": "No code provided"}, status=400)

            fix_prompt = f"""
Analyze the following code for errors.
Provide the error details in text format under the heading "ERROR DETAILS:".
Then provide a fixed version of the code under the heading "FIXED CODE:".
If there are no errors, state "No errors found" under "ERROR DETAILS:" and return the code as is under "FIXED CODE:".
Do not include any other text or formatting.

Code:
{user_code}
"""

            response = model.generate_content(fix_prompt)
            response_text = response.text.strip()

            # Parse response by splitting on headings
            error_details = ""
            fixed_code = ""

            if "ERROR DETAILS:" in response_text and "FIXED CODE:" in response_text:
                parts = response_text.split("ERROR DETAILS:")
                if len(parts) > 1:
                    rest = parts[1]
                    error_part, _, fixed_part = rest.partition("FIXED CODE:")
                    error_details = error_part.strip()
                    fixed_code = fixed_part.strip()
            else:
                error_details = "Could not parse error details."
                fixed_code = response_text

            return JsonResponse({
                "error_details": error_details,
                "fixed_code": fixed_code
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)
