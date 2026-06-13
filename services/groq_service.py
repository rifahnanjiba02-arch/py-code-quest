import re
from config import get_api_key
from groq import Groq

def get_client():
    return Groq(api_key=get_api_key())


def clean_ai_output(text):
    text = re.sub(
    r"<tool_call>.*?</tool_call>",
    "",
    text,
    flags=re.DOTALL
)
    return text.strip()


def get_hint(challenge, test, got, code):
    client= get_client()

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