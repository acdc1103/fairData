import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

def interact_with_gpt(messages, max_tokens=500):  
    try:
        response = client.chat.completions.create(model="gpt-4o",messages=messages,max_tokens=max_tokens)
        return response.choices[0].message.content
    except Exception as e:
        return str(e)
    

def calculate_summary_grade(results):
    
    grades = {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1, "F": 0}
    total = 0
    count = 0

    for result in results.values():
        grade = result.get("grade")
        if grade:
            total += grades.get(grade,0)
            count += 1

    if count > 0:
        average = total / count
    else:
        average = 0
    average = round(average, 2)
    if average >= 4.5:
        return {"text":"A", "number": average}
    elif average >= 4:
        return {"text":"B", "number": average}
    elif average >= 3.5:
        return {"text":"C", "number": average}
    elif average >= 3:
        return {"text":"D", "number": average}
    elif average >= 2.5:
        return {"text":"E", "number": average}
    else:
        return {"text":"F", "number": average}
    
def standards_gpt_workflow(messages):
    #Interacting with GPT-4o to get the response
    result = interact_with_gpt(messages=messages)
    
    #Cleaning the response
    result = result\
            .replace("OUTPUT","")\
            .replace("PREFIX","")\
            .replace("*","")
    
    #Extracting the adherence and grade from the response
    adherence = result.split("ADHERENCE:")[1].split("GRADE:")[0].strip()
    grade = result.split("GRADE:")[1].strip()
    grade = grade[0] #Sometimes the grade is followed by a comma, so we only take the first character

    if grade == "n":
        grade = "not applicable"
    
    return {"grade": grade, "adherence": adherence}

#Metric Grading System including grade, upper bound and lower bound
GRADING_SYSTEM = [
    ("A", 0.9, 1.0),
    ("B", 0.8, 0.89),
    ("C", 0.7, 0.79),
    ("D", 0.6, 0.69),
    ("E", 0.5, 0.59),
    ("F", 0.0, 0.49),
]


def determine_grade(score):
    """Determines the grade based on the score.

    Args:
        score (int): Numeric score of the metric.

    Returns:
        str: Grade of the metric.
    """
    
    # Iterating through the grading system to determine the grade based on the numeric score
    for grade, lower_bound, upper_bound in GRADING_SYSTEM:

        if lower_bound <= score <= upper_bound:

            return grade
        
    return "Invalid score"