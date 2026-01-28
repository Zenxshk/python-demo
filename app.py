import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

PIXPOC_API_KEY = os.getenv("PIXPOC_API_KEY")

# -------------------------
# HEALTH CHECK
# -------------------------
@app.route("/", methods=["GET"])
def health():
    return jsonify({
        "status": "OK",
        "service": "pixpoc-flask-api"
    }), 200


# -------------------------
# CREATE AI AGENT
# POST /api/user/agents
# -------------------------
@app.route("/api/user/agents", methods=["POST"])
def create_agent():

    if not PIXPOC_API_KEY:
        return jsonify({
            "error": "PIXPOC_API_KEY not configured"
        }), 500

    payload = request.get_json(silent=True)

    if not payload:
        return jsonify({
            "error": "Invalid or empty JSON body"
        }), 400

    try:
        response = requests.post(
            "https://api.pixpoc.ai/api/user/agents",
            headers={
                "Authorization": f"Bearer {PIXPOC_API_KEY}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=15
        )

        return jsonify(response.json()), response.status_code

    except requests.exceptions.Timeout:
        return jsonify({
            "error": "Pixpoc API timeout"
        }), 504

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Pixpoc request failed",
            "details": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 4000))
    app.run(host="0.0.0.0", port=port)
