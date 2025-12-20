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
print("Ontology loaded successfully.")

# --------------------------------------------------
# Test Endpoint
# --------------------------------------------------
@app.route("/test", methods=["GET"])
def test():
    return jsonify({"status": "Flask API is working"})

# --------------------------------------------------
# Analyze Endpoint (ONTOLOGY-DRIVEN)
# --------------------------------------------------
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()

    cyclone_name = data.get("cyclone_name")
    wind_speed = data.get("wind_speed")
    water_level = data.get("water_level")
    location_type = data.get("location_type")

    # Remove existing cyclone with same name (if any)
    if cyclone_name in onto.individuals():
        destroy_entity(onto[cyclone_name])


    # ---------- Create Cyclone Individual ----------
    with onto:
        cyclone = onto.Cyclone(cyclone_name)
        cyclone.windSpeed = [wind_speed]
        cyclone.waterLevel = [water_level]

        # Numeric severity pre-classification
        if wind_speed > 120 or water_level > 5:
            cyclone.is_a.append(onto.HighSeverityCyclone)
        elif wind_speed > 80 or water_level > 3:
            cyclone.is_a.append(onto.MediumSeverityCyclone)

        # Location classification
        if location_type.lower() == "coastal":
            cyclone.is_a.append(onto.CoastalCyclone)

    # ---------- Run OWL Reasoner ----------
    with onto:
        sync_reasoner_pellet(
            infer_property_values=True,
            infer_data_property_values=True
        )

    # ---------- Extract Inferred Classes ----------
    class_names = [cls.name for cls in cyclone.is_a]

    if "HighSeverityCyclone" in class_names:
        severity = "High"
    elif "MediumSeverityCyclone" in class_names:
        severity = "Medium"
    else:
        severity = "Low"

    # ---------- Extract Evacuation (OBJECT PROPERTY) ----------
    evacuation_required = False
    if hasattr(cyclone, "evacuationRequired") and cyclone.evacuationRequired:
        evacuation_required = cyclone.evacuationRequired[0]



    # ---------- Extract Authority (OBJECT PROPERTY) ----------
    authorities = []

    
    if hasattr(cyclone, "handledBy") and cyclone.handledBy:
        authorities = [a.name for a in cyclone.handledBy]


    # ---------- Final Response ----------
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
