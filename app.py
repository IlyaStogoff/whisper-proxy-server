from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/transcribe", methods=["POST"])
def transcribe():
    uploaded_file = request.files.get("file")
    if not uploaded_file:
        return jsonify({"error": "No file uploaded"}), 400

    try:
        # Преобразуем FileStorage → (имя_файла, поток, mimetype)
        file_tuple = (uploaded_file.filename, uploaded_file.stream, uploaded_file.mimetype)

        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=file_tuple,
            language="ru",
            response_format="text"
        )
        return transcript.text, 200

    except Exception as e:
        print("Ошибка при транскрипции:", e)
        return jsonify({"error": str(e)}), 500
