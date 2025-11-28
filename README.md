TDS Project 2 — Automated Quiz Solver (LLM-Powered)

This project automatically fetches, parses, downloads files, and solves quiz questions using an LLM (Gemini / GPT).
It supports quizzes with:

✔ HTML-based questions
✔ Downloadable CSV/text files
✔ Auto-submitting final answers to a given /submit endpoint
✔ Logging + internal checkpoints for debugging
✔ Simple local demo quiz pages (dummy_quiz.html)

🚀 Features
Fetch quiz HTML from a URL
Extract:
- Question text
- Submit URL
- Embedded base64 questions
- File URLs (CSV, etc.)
- Download required files
- Solve using Gemini API
- Submit answer automatically
