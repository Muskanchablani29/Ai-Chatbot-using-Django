import json
import google.generativeai as genai
import logging
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token

# Set up logging
logger = logging.getLogger(__name__)

# Integrate Gemini API Key here (ensure this key is valid)
GEMINI_API_KEY = "AIzaSyBFHwApnat5UYU_B2FUu5zV29AuIYfDIVw"

if not GEMINI_API_KEY:
    logger.error("Gemini API key is not set. Please set the API key.")
else:
    genai.configure(api_key=GEMINI_API_KEY)

# Initialize the model
model = genai.GenerativeModel("models/gemini-1.5-pro")

def explore_view(request):
    # Generate CSRF token
    get_token(request)
    return render(request, 'Explore.html')

@csrf_exempt
def generate_code(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            logger.info(f"Received generate_code request data: {data}")
            prompt = data.get('prompt')
            language = data.get('language')

            if not GEMINI_API_KEY:
                error_msg = "Gemini API key is not configured."
                logger.error(error_msg)
                return JsonResponse({"error": error_msg}, status=500)

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

            logger.debug(f"Sending prompt to Gemini API: {full_prompt}")

            response = model.generate_content(full_prompt)
            logger.info(f"Gemini API response received")

            generated_code = response.text.strip()

            # Clean the response if it contains markdown code blocks
            if generated_code.startswith('```'):
                lines = generated_code.split('\n')
                if len(lines) > 2:
                    generated_code = '\n'.join(lines[1:-1])

            return JsonResponse({
                "code": generated_code
            })

        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            logger.error(f"Error generating code from Gemini API: {e}\n{tb}", exc_info=True)
            return JsonResponse({
                "error": f"{str(e)}\n{tb}"
            }, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def fix_code(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_code = data.get('code')

            if not GEMINI_API_KEY:
                error_msg = "Gemini API key is not configured."
                logger.error(error_msg)
                return JsonResponse({"error": error_msg}, status=500)

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

            logger.debug(f"Sending fix prompt to Gemini API: {fix_prompt}")

            response = model.generate_content(fix_prompt)
            logger.info(f"Gemini API response received for fix_code")

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
                # fallback: assign whole response to fixed_code and empty error_details
                error_details = "Could not parse error details."
                fixed_code = response_text

            return JsonResponse({
                "error_details": error_details,
                "fixed_code": fixed_code
            })

        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            logger.error(f"Error fixing code from Gemini API: {e}\n{tb}", exc_info=True)
            return JsonResponse({
                "error": f"{str(e)}\n{tb}"
            }, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)
