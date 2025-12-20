document.getElementById("cycloneForm").addEventListener("submit", function (e) {
    e.preventDefault();

    // -------------------------------
    // STEP 1: Collect input values
    // -------------------------------
    const cycloneName = document.getElementById("cycloneName").value;
    const windSpeed = Number(document.getElementById("windSpeed").value);
    const waterLevel = Number(document.getElementById("waterLevel").value);
    const location = document.getElementById("location").value;

    // -------------------------------
    // STEP 2: Prepare request payload
    // -------------------------------
    const payload = {
        cyclone_name: cycloneName,
        wind_speed: windSpeed,
        water_level: waterLevel,
        location_type: location.toLowerCase()
    };

    // -------------------------------
    // STEP 3: Call Flask backend
    // -------------------------------
    fetch("http://127.0.0.1:5000/analyze", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        // -------------------------------
        // STEP 4: Update UI with results
        // -------------------------------
        document.getElementById("severityResult").textContent = data.severity;
        document.getElementById("evacuationResult").textContent =
            data.evacuation_required ? "Yes" : "No";

        document.getElementById("authorityResult").textContent =
            data.authority.length > 0 ? data.authority.join(", ") : "N/A";
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Failed to analyze cyclone. Check backend server.");
    });
});
