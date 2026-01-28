import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

PIXPOC_API_KEY = os.getenv("PIXPOC_API_KEY")
PIXPOC_BASE_URL = os.getenv("PIXPOC_BASE_URL")


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
        return jsonify({"error": "PIXPOC_API_KEY not configured"}), 500

    payload = request.json

    try:
        response = requests.post(
            f"{PIXPOC_BASE_URL}/api/user/agents",
            headers={
                "Authorization": f"Bearer {PIXPOC_API_KEY}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=15
        )

        if response.status_code not in [200, 201]:
            return jsonify({
                "error": "Pixpoc API Error",
                "details": response.json()
            }), response.status_code

        return jsonify(response.json()), 201

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Request failed",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 4000))
    app.run(host="0.0.0.0", port=port)
