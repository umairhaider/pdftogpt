import logging
import openai
import os

# Configure OpenAI API credentials
def set_openai_key():
    openai.api_key = os.getenv("OPENAI_API_KEY")

# If the API key is not set, raise an exception
if openai.api_key is None:
    raise Exception("Please set your OPENAI_API_KEY as an environment variable.")

def generate_chatgpt_response(prompt, max_tokens=100):
    set_openai_key()
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=0.7
        )
        generated_text = response.choices[0].text.strip()
        return generated_text
    except Exception as e:
        logging.error(f"Error occurred while generating chatGPT response: {str(e)}")
        raise  Exception("Unexpected error")

def clean_text(text):
    text = text.replace('\n', ' ')
    text = text.replace('\r', '') 
    text = text.replace('\t', ' ') 
    return text