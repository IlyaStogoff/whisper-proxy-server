from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/transcribe", methods=["POST"])
def transcribe():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    try:
        resp = openai.Audio.transcriptions.create(
            model="whisper-1",
            file=file,
            language="ru",
            response_format="text"
        )
        return resp, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
