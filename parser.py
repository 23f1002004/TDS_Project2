import re
import base64
from collections import namedtuple

ParsedQuiz = namedtuple("ParsedQuiz", ["question_text", "submit_url", "file_urls"])

def parse_quiz_page(html):

    match = re.search(r'atob\((?:`|"|\')(.+?)(?:`|"|\')\)', html, re.S)
    if not match:
        raise Exception("Base64 data not found")

    b64_str = match.group(1)
    decoded = base64.b64decode(b64_str).decode("utf-8")

    question_text = re.split(r'<pre>', decoded)[0].strip()
    if not question_text:
        question_text = decoded.strip()

    file_urls = re.findall(
        r'https?://[^\s"\']+\.(?:csv|pdf|json|txt|xlsx)',
        decoded,
        re.I
    )

    submit = re.search(
        r'https?://[^\s"\']*(submit)[^\s"\']*',
        decoded,
        re.I
    )
    if not submit:
        raise Exception("Submit URL missing")

    return ParsedQuiz(
        question_text=question_text,
        submit_url=submit.group(0),
        file_urls=file_urls
    )
