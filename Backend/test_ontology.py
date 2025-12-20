import os
from owlready2 import *

# --------------------------------------------------
# STEP 1: Load Ontology (Safe Path Handling)
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ONTO_PATH = os.path.join(BASE_DIR, "cyclone.rdf")

onto = get_ontology(ONTO_PATH).load()
print("Ontology loaded successfully!")



# --------------------------------------------------
# STEP 3: Create Cyclone Individual
# --------------------------------------------------
with onto:
    cyclone = onto.Cyclone("Cyclone_Test_003")

    # Assign data properties (must match ontology names)
    cyclone.windSpeed = [120]
    cyclone.waterLevel = [4]

print("\nCyclone individual created:")
print("Name:", cyclone.name)
print("Wind Speed:", cyclone.windSpeed[0])
print("Water Level:", cyclone.waterLevel[0])

# --------------------------------------------------
# STEP 4: Python-based Severity Classification
# (Using EXISTING ontology classes)
# --------------------------------------------------
wind = cyclone.windSpeed[0]
water = cyclone.waterLevel[0]

with onto:
    if wind > 120 or water > 5:
        cyclone.is_a.append(onto["HighSeverityCyclone"])
        severity = "High"

    elif wind > 80 or water > 3:
        cyclone.is_a.append(onto["MediumSeverityCyclone"])
        severity = "Medium"

    else:
        severity = "Low"

print("\nSeverity classification complete:")
print("Severity:", severity)
print("Cyclone belongs to classes:")
for cls in cyclone.is_a:
    print(" -", cls.name)

# --------------------------------------------------
# STEP 5: (Optional) Assign CoastalCyclone
# --------------------------------------------------
# This is just a simulation for now
location_type = "coastal"  # later comes from frontend

with onto:
    if location_type == "coastal":
        cyclone.is_a.append(onto["CoastalCyclone"])
        print("\nLocation-based classification applied:")
        print(" - CoastalCyclone")

print("\nFinal class membership:")
for cls in cyclone.is_a:
    print(" -", cls.name)


# --------------------------------------------------
# STEP 5: Run OWL Reasoner (AXIOM-BASED INFERENCE)
# --------------------------------------------------

from owlready2 import *

print("\nRunning ontology reasoner (Pellet)...")

with onto:
    sync_reasoner_pellet(
        infer_property_values=True,
        infer_data_property_values=True
    )

print("Reasoning completed successfully.")


# --------------------------------------------------
# STEP 6: Convert inferred ontology data to JSON
# --------------------------------------------------

print("\nConverting inferred knowledge to JSON...")

# ---------- Extract class membership ----------
class_names = [cls.name for cls in cyclone.is_a]

# ---------- Determine severity ----------
if "HighSeverityCyclone" in class_names:
    severity_value = "High"
elif "MediumSeverityCyclone" in class_names:
    severity_value = "Medium"
else:
    severity_value = "Low"

# ---------- Evacuation inference ----------
evacuation_required = False
evacuation_plans = []

if hasattr(cyclone, "requiresEvacuation") and cyclone.requiresEvacuation:
    evacuation_required = True
    evacuation_plans = [plan.name for plan in cyclone.requiresEvacuation]

# ---------- Authority inference ----------
authorities = []

if hasattr(cyclone, "handledBy") and cyclone.handledBy:
    authorities = [auth.name for auth in cyclone.handledBy]

# ---------- Final JSON-like response ----------
response = {
    "cyclone_name": cyclone.name,
    "severity": severity_value,
    "evacuation_required": evacuation_required,
    "evacuation_plans": evacuation_plans,
    "authority": authorities,
    "classes": class_names
}

print("\nFINAL JSON OUTPUT:")
print(response)

