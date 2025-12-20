import os
from owlready2 import *

# --------------------------------------------------
# STEP 1: Load Ontology
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ONTO_PATH = os.path.join(BASE_DIR, "cyclone.rdf")

onto = get_ontology(ONTO_PATH).load()
print("Ontology loaded successfully!")

# --------------------------------------------------
# STEP 2: Create Cyclone Individual
# --------------------------------------------------
with onto:
    cyclone = onto.Cyclone("Cyclone_Test_003")
    cyclone.windSpeed = [120]
    cyclone.waterLevel = [4]

print("\nCyclone individual created:")
print("Name:", cyclone.name)
print("Wind Speed:", cyclone.windSpeed[0])
print("Water Level:", cyclone.waterLevel[0])

# --------------------------------------------------
# STEP 3: Initial Severity Classification (Numeric)
# --------------------------------------------------
wind = cyclone.windSpeed[0]
water = cyclone.waterLevel[0]

with onto:
    if wind > 120 or water > 5:
        cyclone.is_a.append(onto.HighSeverityCyclone)
    elif wind > 80 or water > 3:
        cyclone.is_a.append(onto.MediumSeverityCyclone)

# --------------------------------------------------
# STEP 4: Location-based Classification
# --------------------------------------------------
location_type = "coastal"

with onto:
    if location_type == "coastal":
        cyclone.is_a.append(onto.CoastalCyclone)

print("\nInitial class membership:")
for cls in cyclone.is_a:
    print(" -", cls.name)

# --------------------------------------------------
# STEP 5: Run OWL Reasoner (AXIOM-BASED)
# --------------------------------------------------
print("\nRunning ontology reasoner (Pellet)...")

with onto:
    sync_reasoner_pellet(
        infer_property_values=True,
        infer_data_property_values=True
    )

print("Reasoning completed successfully.")

# --------------------------------------------------
# STEP 6: Extract Inferred Knowledge
# --------------------------------------------------
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

response = {
    "cyclone_name": cyclone.name,
    "severity": severity,
    "evacuation_required": evacuation_required,
    "authority": authorities,
    "classes": class_names
}

print("\nFINAL JSON OUTPUT:")
print(response)
