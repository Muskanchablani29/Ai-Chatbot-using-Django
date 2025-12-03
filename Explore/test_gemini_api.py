import google.generativeai as genai

def test_gemini_api():
    # Configure your API key here if not already configured globally
    genai.configure(api_key="AIzaSyDSbisde1SZQEinxeEdwkTbCM99IRDsoe8")

    # List available models
    try:
        models = genai.list_models()
        print("Available models:")
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                print(f"- {model.name}")
    except Exception as e:
        print("Error listing models:")
        print(e)

    # Test with a known working model
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = "Write a Python function to add two numbers."
        response = model.generate_content(prompt)
        print("API call successful with gemini-2.0-flash. Generated content:")
        print(response.text)
    except Exception as e:
        print("API call failed with gemini-2.0-flash:")
        print(e)

if __name__ == "__main__":
    test_gemini_api()
