const API = "http://127.0.0.1:8000/api";

async function loadAnalytics() {

    try {

        // ------------------------
        // Load API Data
        // ------------------------

        const summaryRes = await fetch(`${API}/summary`);
        const summary = await summaryRes.json();

        const statesRes = await fetch(`${API}/states`);
        const states = await statesRes.json();

        // ------------------------
        // Risk Distribution
        // ------------------------

        const riskCount = {
            Low: 0,
            Moderate: 0,
            High: 0,
            Critical: 0
        };

        states.forEach(state => {
            riskCount[state.risk_level]++;
        });

        new Chart(document.getElementById("riskChart"), {

            type: "doughnut",

            data: {

                labels: Object.keys(riskCount),

                datasets: [{

                    data: Object.values(riskCount),

                    backgroundColor: [
                        "#22c55e",
                        "#facc15",
                        "#f97316",
                        "#dc2626"
                    ]

                }]

            }

        });

        // ------------------------
        // Top Risk States
        // ------------------------

        const sortedStates = [...states]
            .sort((a, b) => b.risk_score - a.risk_score)
            .slice(0, 10);

        new Chart(document.getElementById("topStatesChart"), {

            type: "bar",

            data: {

                labels: sortedStates.map(s => s.state),

                datasets: [{

                    label: "Risk Score",

                    data: sortedStates.map(s => s.risk_score),

                    backgroundColor: "#2563eb"

                }]

            },

            options: {

                scales: {

                    y: {

                        beginAtZero: true,
                        max: 1

                    }

                }

            }

        });

        // ------------------------
        // Top Drivers
        // ------------------------

        const drivers = {};

        states.forEach(state => {

            if (!drivers[state.top_driver]) {

                drivers[state.top_driver] = 0;

            }

            drivers[state.top_driver]++;

        });

        new Chart(document.getElementById("indicatorChart"), {

            type: "pie",

            data: {

                labels: Object.keys(drivers),

                datasets: [{

                    data: Object.values(drivers),

                    backgroundColor: [

                        "#2563eb",
                        "#14b8a6",
                        "#f97316",
                        "#dc2626",
                        "#8b5cf6",
                        "#22c55e",
                        "#eab308",
                        "#ec4899"

                    ]

                }]

            }

        });

        // ------------------------
        // Cluster Distribution
        // ------------------------

        const clusters = {};

        states.forEach(state => {

            if (!clusters[state.cluster]) {

                clusters[state.cluster] = 0;

            }

            clusters[state.cluster]++;

        });

        new Chart(document.getElementById("urbanRuralChart"), {

            type: "bar",

            data: {

                labels: Object.keys(clusters).map(c => `Cluster ${c}`),

                datasets: [{

                    label: "States",

                    data: Object.values(clusters),

                    backgroundColor: "#14b8a6"

                }]

            }

        });

    }

    catch (err) {

        console.error(err);

    }

}

document.addEventListener("DOMContentLoaded", loadAnalytics);