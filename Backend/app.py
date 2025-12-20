from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/test", methods=["GET"])
def test():
    return jsonify({"status": "Flask API is working"})

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()

    cyclone_name = data.get("cyclone_name")
    wind_speed = data.get("wind_speed")
    water_level = data.get("water_level")
    location_type = data.get("location_type")

    response = {
        "cyclone_name": cyclone_name,
        "severity": "Medium",
        "evacuation_required": True,
        "authority": ["StateAuthority"]
    }

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
