import os
import time
import requests

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-2.5-flash-preview-09-2025"
MAX_RETRIES = 4

def call_gemini(prompt):

    if not GEMINI_API_KEY:
        raise Exception("GEMINI_API_KEY not set")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"

    headers = {"Content-Type": "application/json"}
    body = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    for i in range(MAX_RETRIES):
        try:
            r = requests.post(url, headers=headers, json=body, timeout=25)
            r.raise_for_status()
            data = r.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]

        except:
            if i == MAX_RETRIES - 1:
                raise
            time.sleep(2 ** i)

def solve_question(parsed_quiz, downloaded_files):
    prompt = (
        "You are a precise data analysis engine. "
        "Use the provided files EXACTLY as they appear. "
        "Do NOT guess. If any file is provided, read it carefully.\n\n"
    )

    prompt += f"QUESTION:\n{parsed_quiz.question_text}\n\n"

    if downloaded_files:
        prompt += "FILES:\n"
        for name, (ctype, content) in downloaded_files.items():
            prompt += f"FILE: {name} (type={ctype})\n"
            prompt += f"<file>\n{content}\n</file>\n\n"

    prompt += (
        "Return ONLY the correct final answer. "
        "If numeric, output only the number. No explanation. No extra text."
    )

    answer = call_gemini(prompt)

    return answer.strip()
