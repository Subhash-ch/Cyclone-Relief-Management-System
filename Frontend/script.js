document.getElementById("cycloneForm").addEventListener("submit", function (e) {
    e.preventDefault();

    // -------------------------------
    // STEP 1: Collect input values
    // -------------------------------
    const cycloneName = document.getElementById("cycloneName").value;
    const windSpeed = Number(document.getElementById("windSpeed").value);
    const waterLevel = Number(document.getElementById("waterLevel").value);
    const location = document.getElementById("location").value;
    const population = parseInt(document.getElementById("population").value);
    if (isNaN(population) || population <= 0) {
        alert("Please enter a valid affected population.");
        return;
    }






    // -------------------------------
    // STEP 2: Prepare request payload
    // -------------------------------
    const payload = {
        cyclone_name: cycloneName,
        wind_speed: windSpeed,
        water_level: waterLevel,
        location_type: location.toLowerCase()
    };


    document.getElementById("foodPackets").textContent = "--";
    document.getElementById("waterUnits").textContent = "--";
    document.getElementById("medicalTeams").textContent = "--";
    document.getElementById("shelters").textContent = "--";
    document.getElementById("rescueVehicles").textContent = "--";

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
            // STEP 5: Resource Allocation Logic
            // -------------------------------
            const severity = data.severity.toLowerCase();
            const population = parseInt(document.getElementById("population").value);

            let foodPackets = 0;
            let waterUnits = 0;
            let medicalTeams = 0;
            let shelters = 0;
            let rescueVehicles = 0;

            // Food & water (same for all)
            
           

            if (severity === "high") {
                foodPackets = population * 2;
                waterUnits = population * 3;
                medicalTeams = Math.ceil(population / 500);
                shelters = Math.ceil(population / 1000);
                rescueVehicles = Math.ceil(population / 1000);
            }
            else if (severity === "medium") {
                foodPackets = population*1.5;
                waterUnits = population*2;
                medicalTeams = Math.ceil(population / 1000);
                shelters = Math.ceil(population / 1500);
                rescueVehicles = Math.ceil(population / 1200);
            }
            else {
                foodPackets = population*1.15;
                waterUnits = population*1.5;
                medicalTeams = Math.ceil(population / 1200);
                shelters = Math.ceil(population / 2000);
                rescueVehicles = Math.ceil(population / 1500);
            }

            // -------------------------------
            // Update UI
            // -------------------------------
            document.getElementById("foodPackets").textContent = foodPackets;
            document.getElementById("waterUnits").textContent = waterUnits;
            document.getElementById("medicalTeams").textContent = medicalTeams;
            document.getElementById("shelters").textContent = shelters;
            document.getElementById("rescueVehicles").textContent = rescueVehicles;

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
