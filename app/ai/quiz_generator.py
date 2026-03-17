import json
import re
from groq import Groq
from app.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


def extract_json(text):
    """
    Extract JSON object from LLM response safely
    """

    # remove markdown blocks
    text = text.replace("```json", "").replace("```", "")

    # find JSON content
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        return match.group(0)

    raise ValueError("No JSON found in AI response")


def generate_quiz(topic, difficulty, num_questions):

    prompt = f"""
Generate {num_questions} multiple choice questions about {topic}.
Difficulty level: {difficulty}

Return ONLY JSON in this format:

{{
 "questions":[
   {{
     "question":"text",
     "options":["A","B","C","D"],
     "answer":"correct option",
     "explanation":"short explanation"
   }}
 ]
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.choices[0].message.content

    json_text = extract_json(content)

    quiz = json.loads(json_text)

    return quiz