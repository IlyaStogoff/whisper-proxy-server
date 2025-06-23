from flask import Flask, request, jsonify
from flask_cors import CORS  # ← добавлено
import openai
import os

app = Flask(__name__)
CORS(app)  # ← разрешаем запросы с других доменов

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
        print("Ошибка при транскрипции:", e)
        return jsonify({"error": str(e)}), 500
