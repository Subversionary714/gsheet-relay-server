from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# === CONFIGURATION ===
REAL_API_URL = "https://secure-gsheet-api.onrender.com/add_lender"
REAL_API_SECRET = "gsheets-admin-2024$secure!"  # your live API token

@app.route("/relay_add_lender", methods=["POST"])
def relay_add_lender():
    try:
        payload = request.get_json()

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {REAL_API_SECRET}"
        }

        response = requests.post(REAL_API_URL, headers=headers, json=payload)
        return jsonify({
            "status": "forwarded",
            "real_api_status": response.status_code,
            "real_api_response": response.json()
        }), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def health():
    return "✅ Relay server is up"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
