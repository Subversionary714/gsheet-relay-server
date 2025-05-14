from flask import Flask, request, jsonify
import requests
import sys
import json  # ✅ Required for json.dumps()

app = Flask(__name__)

REAL_API_URL = "https://secure-gsheet-api.onrender.com/add_lender"
REAL_API_SECRET = "gsheets-admin-2024$secure!"

@app.route("/relay_add_lender", methods=["POST"])
def relay_add_lender():
    try:
        payload = request.get_json()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {REAL_API_SECRET}"
        }

        # ✅ Force sending as raw JSON string to Flask
        response = requests.post(
            REAL_API_URL,
            data=json.dumps(payload),
            headers=headers
        )

        print("🔁 Forwarded to secure-gsheet-api")
        print("Response code:", response.status_code)
        print("Response body:", response.text)
        sys.stdout.flush()

        return jsonify({
            "status": "forwarded",
            "response_code": response.status_code,
            "response_body": response.text
        }), response.status_code

    except Exception as e:
        print("❌ Relay encountered an error:", str(e))
        sys.stdout.flush()
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def index():
    return "✅ Relay is up"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
