import time
from google import genai

'''
Takes the email dictionary and the API key as arguments. 
The key comes in from main.py rather than being read from config here
keeps this file focused on one job and makes it easier to test in isolation.
'''
def summarize(email, api_key, max_retries=3):
    # authenticates with gemini key
    client = genai.Client(api_key=api_key)

    prompt = f"""
    Summarize this email in 2 sentences.

    Subject: {email["subject"]}
    Body: {email["body"]}
    """

    for attempt in range(max_retries):
        # the API call 
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=prompt
            )
            return response.text
            
        # catches error
        except Exception as e:
            error_msg = str(e)
            
            # If hit a rate limit, pause and loop again
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                wait_time = 30  # Wait the 36s Google asks for
                print(f"Rate limit hit! Waiting {wait_time}s before retrying (Attempt {attempt + 1}/{max_retries})...")
                time.sleep(wait_time)
                
            # If it's a different error (like bad API key or no internet), fail immediately
            else:
                print(f"Gemini API error: {e}")
                return "Could not summarize this email."
                
    # If the loop finishes all retries and still hasn't returned a summary
    print("Failed to summarize after maximum retries.")
    return "Could not summarize this email due to high API traffic."