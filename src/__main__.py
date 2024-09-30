from flask import Flask, send_from_directory, request, send_file
import tempfile
from gtts import gTTS
import torch
from diffusers import AutoPipelineForText2Image

app = Flask(__name__, static_folder="../docs")


@app.route("/")
def home():
    return "API"


def with_tts(filepath, text, lang):
    print(f"\n\t{lang} | {filepath} |\n")
    tts = gTTS(text=text, lang=lang)
    if tts:
        tts.save(filepath)
        return True
    return False


def with_torch(filepath, text, height, width):
    model_id = "kandinsky-community/kandinsky-2-1"
    pipe = AutoPipelineForText2Image.from_pretrained(model_id, dtype=torch.float16)
    height = int(int(height) / 4)
    width = int(int(width) / 4)
    print(f"\n\t{height}x{width} | {filepath} |\n")
    output = pipe(
        prompt=text,
        negative_prompt="low quality, bad quality",
        prior_guidance_scale=1.0,
        height=height,
        width=width,
    )
    if len(output.images) == 1:
        image = output.images[0]
        image.save(filepath)
        return True
    return False


@app.route("/", methods=["POST"])
def receive_data():
    data = request.get_json()
    with tempfile.NamedTemporaryFile() as temp_file:
        mimetype = ""
        filepath = temp_file.name
        if data["type"] == "speech":
            mimetype = "audio/mpeg"
            filepath += ".mp3"
            lang = request.args.get("lang", default="en")
            if not with_tts(filepath, data["text"], lang):
                return "", 500

        elif data["type"] == "image":
            mimetype = "image/png"
            filepath += ".png"
            if not with_torch(filepath, data["text"], data["height"], data["width"]):
                return "", 500

        try:
            return send_file(filepath, mimetype=mimetype, as_attachment=True)
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
