import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from owlready2 import *

# --------------------------------------------------
# Flask Setup
# --------------------------------------------------
app = Flask(__name__)
CORS(app)

# --------------------------------------------------
# Load Ontology ONCE
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ONTO_PATH = os.path.join(BASE_DIR, "cyclone.rdf")

onto = get_ontology(ONTO_PATH).load()
print("Ontology loaded into Flask.")

# --------------------------------------------------
# Test Endpoint
# --------------------------------------------------
@app.route("/test", methods=["GET"])
def test():
    return jsonify({"status": "Flask API is working"})

# --------------------------------------------------
# Analyze Endpoint (ONTOLOGY-BASED)
# --------------------------------------------------
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()

    cyclone_name = data.get("cyclone_name")
    wind_speed = data.get("wind_speed")
    water_level = data.get("water_level")
    location_type = data.get("location_type")

    # ---------- Create individual ----------
    with onto:
        cyclone = onto.Cyclone(cyclone_name)
        cyclone.windSpeed = [wind_speed]
        cyclone.waterLevel = [water_level]

        # Initial numeric classification
        if wind_speed > 120 or water_level > 5:
            cyclone.is_a.append(onto.HighSeverityCyclone)
        elif wind_speed > 80 or water_level > 3:
            cyclone.is_a.append(onto.MediumSeverityCyclone)

        if location_type == "coastal":
            cyclone.is_a.append(onto.CoastalCyclone)

    # ---------- Run reasoner ----------
    with onto:
        sync_reasoner_pellet(
            infer_property_values=True,
            infer_data_property_values=True
        )

    # ---------- Extract inferred knowledge ----------
    class_names = [cls.name for cls in cyclone.is_a]

    if "HighSeverityCyclone" in class_names:
        severity = "High"
    elif "MediumSeverityCyclone" in class_names:
        severity = "Medium"
    else:
        severity = "Low"

    evacuation_required = False
    if hasattr(cyclone, "requiresEvacuation") and cyclone.requiresEvacuation:
        evacuation_required = True

    authorities = []
    if hasattr(cyclone, "handledBy") and cyclone.handledBy:
        authorities = [a.name for a in cyclone.handledBy]

    # ---------- Final inferred response ----------
    response = {
        "cyclone_name": cyclone.name,
        "severity": severity,
        "evacuation_required": evacuation_required,
        "authority": authorities
    }

    return jsonify(response)

# --------------------------------------------------
# Run Server
# --------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
