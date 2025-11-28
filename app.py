from flask import Flask, request, jsonify, send_from_directory
from parser import parse_quiz_page
from scraper import QuizScraper
from solver import solve_question
from downloader import download_files
import requests
import os
import time

SECRET = os.environ.get("QUIZ_SECRET", "123456789abcdefghi")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

@app.route("/quiz", methods=["POST"])
def quiz_endpoint():
    try:
        data = request.get_json(force=True)
    except:
        return jsonify({"error": "Invalid JSON"}), 400

    if not data or data.get("secret") != SECRET:
        return jsonify({"error": "Forbidden"}), 403

    quiz_url = data.get("url")
    if not quiz_url:
        return jsonify({"error": "Missing 'url' field"}), 400

    email = data.get("email")
    if not email:
        return jsonify({"error": "Missing 'email' field"}), 400

    start_time = time.time()

    try:
        scraper = QuizScraper()
        try:

            html = scraper.fetch_page_content(quiz_url)

            parsed = parse_quiz_page(html)

            downloaded_files = download_files(parsed.file_urls)

            answer = solve_question(parsed, downloaded_files)

            submission_payload = {
                "email": email,
                "secret": data["secret"],
                "url": quiz_url,
                "answer": answer
            }

            submit_response = requests.post(
                parsed.submit_url,
                json=submission_payload,
                timeout=20
            )
            submit_response.raise_for_status()
            result = submit_response.json()

        finally:
            scraper.close()

    except Exception as e:
        return jsonify({
            "error": "Quiz solving pipeline failed",
            "details": str(e),
            "url_attempted": quiz_url
        }), 500

    total_time = round(time.time() - start_time, 3)


    return jsonify({
        "status": "submitted",
        "answer": answer,
        "submit_result": result,
        "time_taken_seconds": total_time
    })

if __name__ == "__main__":
    app.run(debug=True)
