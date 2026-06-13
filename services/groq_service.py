import re
from config import get_api_key
from groq import Groq


def get_client():
    return Groq(api_key=get_api_key())


def clean_ai_output(text: str) -> str:
    # Remove any hidden reasoning blocks if they appear
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL | re.IGNORECASE)

    # Also remove standalone leftover tags just in case
    text = re.sub(r"</?think>", "", text, flags=re.IGNORECASE)

    return text.strip()


def get_hint(challenge, test, got, code):
    client = get_client()

    prompt = f"""
You are a coding tutor.

RULES:
- Give ONLY a very short indirect hint.
- Do NOT provide full solution.
- Do NOT show reasoning or steps.
- Do NOT use tags like <think> or any hidden blocks.
- Output must be plain text only.

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
                "role": "system",
                "content": "You are a helpful assistant. Output only final text. Never include <think> or reasoning tags."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return clean_ai_output(
        response.choices[0].message.content
    )