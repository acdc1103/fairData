import os
from openai import OpenAI

api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=api_key)

def interact_with_gpt(messages, max_tokens=500):  
    try:
        response = client.chat.completions.create(model="gpt-4o",messages=messages,max_tokens=max_tokens)
        return response.choices[0].message.content
    except Exception as e:
        return str(e)