import os
import re

from dotenv import load_dotenv
from groq import Groq

load_dotenv(".env.local")

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def clean_ai_output(text):
    text = re.sub(
        r"<think>.*?</think>",
        "",
        text,
        flags=re.DOTALL
    )

    return text.strip()


def get_hint(challenge, test, got, code):

    prompt = f"""
You are a coding tutor. Reply back to the user.

IMPORTANT:
- Give only a short indirect hint.
- Do not provide the full solution.
- Try to give indirect hints
- Do not include reasoning tags.
- Be beginner friendly.

Problem:
{challenge['description']}

Student Code:
{code}

Failed Test:
Input: {test.get('input')}
Expected: {test.get('expected')}
Got: {got}
"""

    response = client.chat.completions.create(
        model="qwen/qwen3-32b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return clean_ai_output(
        response.choices[0].message.content
    )