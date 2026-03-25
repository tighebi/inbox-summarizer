import google.generativeai as genai

'''
Takes the email dictionary and the API key as arguments. 
The key comes in from main.py rather than being read from config here
keeps this file focused on one job and makes it easier to test in isolation.
'''
def summarize(email, api_key):
    # authenticates with gemini key and confirms model
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash-lite")

    prompt = f"""
    Summarize this email in 2 sentences.

    Subject: {email["subject"]}
    Body: {email["body"]}
    """

    # the API call 
    try:
        response = model.generate_content(prompt)
        return response.text
    # catches error
    except Exception as e:
        print(f"Gemini API error: {e}")
        return "Could not summarize this email."