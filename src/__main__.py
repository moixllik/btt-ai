from flask import Flask, send_from_directory, request, send_file
import tempfile
from gtts import gTTS
import os
import dotenv
import requests
import json

dotenv.load_dotenv()

app = Flask(__name__, static_folder="../docs")


@app.route("/")
def home():
    return "API"


def with_tts(filepath, text, lang):
    tts = gTTS(text=text, lang=lang)
    tts.save(filepath)
    return True


def with_api(filepath, text, height, width):
    url = ""
    api_key = os.getenv("OPENAI")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {}
    response = requests.post(url, headers=headers, json=data)
    print(response, headers, data, response.json())
    if response.status_code == 200:
        print("ok")
    return False


@app.route("/", methods=["POST"])
def receive_data():
    data = request.get_json()
    with tempfile.NamedTemporaryFile() as temp_file:
        mimetype = ""
        if data["type"] == "speech":
            mimetype = "audio/mpeg"
            lang = request.args.get("lang", default="en")
            if not with_tts(temp_file.name, data["text"], lang):
                return "", 500

        elif data["type"] == "image":
            mimetype = "image/png"
            if not with_api(
                temp_file.name, data["text"], data["height"], data["width"]
            ):
                return "", 500

        try:
            return send_file(temp_file.name, mimetype=mimetype, as_attachment=True)
        except Exception as e:
            print(f"\nError:\n\t{e}")
            return "", 500

    return "", 404


@app.route("/docs/<path:filename>")
def serve_docs(filename):
    return send_from_directory("../docs", filename)


@app.route("/docs/")
def serve_docs_index():
    return send_from_directory("../docs", "index.html")


if __name__ == "__main__":
    app.run(debug=True, port=8080)
