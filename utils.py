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
    

def calculate_summary_grade(results):
    
    grades = {'A': 5, 'B': 4, 'C': 3, 'D': 2, 'E': 1, 'F': 0}
    total = 0
    count = 0

    for result in results.values():
        grade = result.get('grade')
        if grade:
            total += grades[grade]
            count += 1

    if count > 0:
        average = total / count
    else:
        average = 0

    if average >= 4.5:
        return 'A'
    elif average >= 3.5:
        return 'B'
    elif average >= 2.5:
        return 'C'
    elif average >= 1.5:
        return 'D'
    elif average >= 0.5:
        return 'E'
    else:
        return 'F'