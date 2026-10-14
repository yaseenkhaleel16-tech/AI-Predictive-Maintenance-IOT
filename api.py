from flask import Flask, request, jsonify
from src.predict import predict_risk

app = Flask(__name__)

@app.get("/")
def home():
    return jsonify({
        "project": "AI-Powered Predictive Maintenance for IoT Devices",
        "usage": "POST JSON to /predict with temperature, vibration, current",
        "example": {"temperature": 78, "vibration": 4.8, "current": 13.5}
    })

@app.post("/predict")
def predict():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "Send a JSON object in the request body."}), 400
    try:
        values = [float(payload[k]) for k in ("temperature", "vibration", "current")]
        if not all(map(lambda v: abs(v) < 1e6, values)):
            raise ValueError
        result = predict_risk(*values)
        return jsonify(result)
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Required numeric fields: temperature, vibration, current."}), 400
    except FileNotFoundError as exc:
        return jsonify({"error": str(exc)}), 503

if __name__ == "__main__":
    # Local development only; do not expose this debug server to the public internet.
    app.run(host="127.0.0.1", port=5000, debug=False)
