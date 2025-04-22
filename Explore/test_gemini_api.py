import google.generativeai as genai

def test_gemini_api():
    # Configure your API key here if not already configured globally
    genai.configure(api_key="AIzaSyBFuikHl1HHID9r2hzqCsr7yht1xa67J5I")
    model = genai.GenerativeModel("models/gemini-1.5-pro")

    prompt = "Write a Python function to add two numbers."

    try:
        response = model.generate_content(prompt)
        print("API call successful. Generated content:")
        print(response.text)
    except Exception as e:
        print("API call failed with error:")
        print(e)

if __name__ == "__main__":
    test_gemini_api()
