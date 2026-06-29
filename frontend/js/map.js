const API = "http://127.0.0.1:8000/api";

// Create map
const map = L.map("map").setView([22.5, 80], 5);

// OpenStreetMap tiles
L.tileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
        attribution: "© OpenStreetMap"
    }
).addTo(map);

// Load everything
async function loadMap() {

    try {

        // -----------------------------
        // Load GeoJSON
        // -----------------------------
        const geoResponse = await fetch("assets/india.geojson");

        if (!geoResponse.ok) {
            throw new Error(
                "Could not load india.geojson"
            );
        }

        const geojson = await geoResponse.json();

        console.log("GeoJSON Loaded");
        console.log("Features:", geojson.features.length);

        // -----------------------------
        // Load Backend Data
        // -----------------------------
        const apiResponse = await fetch(`${API}/states`);

        if (!apiResponse.ok) {
            throw new Error(
                "Could not load backend data"
            );
        }

        const states = await apiResponse.json();

        console.log("Backend Loaded");
        console.log(states);

        // -----------------------------
        // Create lookup table
        // -----------------------------
        const stateMap = {};

        states.forEach(state => {

            stateMap[state.state.trim()] = state;

        });

        console.log(stateMap);

        // -----------------------------
        // Risk colours
        // -----------------------------
        function getColor(level) {

            switch (level) {

                case "Critical":
                    return "#dc2626";

                case "High":
                    return "#f97316";

                case "Moderate":
                    return "#facc15";

                case "Low":
                    return "#22c55e";

                default:
                    return "#d1d5db";

            }

        }

        // -----------------------------
        // Draw GeoJSON
        // -----------------------------
        L.geoJSON(geojson, {

            style: function (feature) {

                // Your GeoJSON uses st_nm
                const stateName =
                    feature.properties.st_nm.trim();

                const state =
                    stateMap[stateName];

                return {

                    fillColor: state
                        ? getColor(state.risk_level)
                        : "#d1d5db",

                    weight: 0.5,

                    opacity: 1,

                    color: "#ffffff",

                    fillOpacity: 0.8

                };

            },

            onEachFeature: function (feature, layer) {

                const stateName =
                    feature.properties.st_nm.trim();

                const state =
                    stateMap[stateName];

                if (!state) {

                    layer.bindPopup(
                        `<b>${stateName}</b><br>No Data`
                    );

                    return;

                }

                layer.bindPopup(`

                    <h3>${state.state}</h3>

                    <b>Risk Score:</b> ${state.risk_score}<br>

                    <b>Risk Level:</b> ${state.risk_level}<br>

                    <b>Cluster:</b> ${state.cluster}<br>

                    <b>Top Driver:</b> ${state.top_driver}

                `);

            }

        }).addTo(map);

    }

    catch (error) {

        console.error(error);

        alert(error.message);

    }

}

loadMap();