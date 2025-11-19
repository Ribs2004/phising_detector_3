# src/main.py
from flask import Flask, render_template, request, jsonify
from analyzer import analyze_url

import os

# Define caminhos para templates e static (estão em ../web)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "..", "web", "templates")
STATIC_DIR = os.path.join(BASE_DIR, "..", "web", "static")

app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)

@app.route("/", methods=["GET"])
def index():
    # Renderiza a página inicial com o form
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Recebe JSON: { "url": "https://..." }
    Retorna JSON com resultado da análise.
    """
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "Campo 'url' é obrigatório"}), 400

    url = data["url"]
    result = analyze_url(url)
    return jsonify(result)

if __name__ == "__main__":
    # Roda localmente
    app.run(debug=True)
