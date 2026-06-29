const API = "http://127.0.0.1:8000/api";

async function loadDashboard() {

    try {

        // ---------------- Summary ----------------
        const summaryResponse = await fetch(`${API}/summary`);
        const summary = await summaryResponse.json();

        document.getElementById("totalStates").innerText =
            summary.states_loaded;

        document.getElementById("avgRisk").innerText =
            summary.average_risk;

        document.getElementById("criticalStates").innerText =
            summary.critical_states;

        document.getElementById("clusters").innerText =
            summary.clusters;


        // ---------------- States ----------------
        const statesResponse = await fetch(`${API}/states`);
        const states = await statesResponse.json();

        loadTopStates(states);

        loadAlerts(states);

        renderChart(states);

    }

    catch(error){

        console.error(error);

    }

}


// ======================================
// TOP STATES TABLE
// ======================================

function loadTopStates(states){

    const tbody = document.getElementById("topStatesBody");

    tbody.innerHTML = "";

    states
    .sort((a,b)=>b.risk_score-a.risk_score)
    .slice(0,5)
    .forEach(state=>{

        tbody.innerHTML += `

        <tr>

            <td>${state.state}</td>

            <td>${state.risk_score}</td>

            <td>${state.risk_level}</td>

            <td>

                <progress
                    value="${state.risk_score}"
                    max="1">
                </progress>

            </td>

        </tr>

        `;

    });

}



// ======================================
// ALERTS
// ======================================

function loadAlerts(states){

    const card = document.querySelector(".alert-card");

    card.innerHTML = "<h3>Recent Alerts</h3>";

    states
    .filter(s=>s.risk_level==="Critical")
    .forEach(state=>{

        card.innerHTML += `

        <div class="alert-item alert-critical">

            ⚠ ${state.state} requires immediate intervention

        </div>

        `;

    });

}



// ======================================
// CHART
// ======================================

function renderChart(states){

    const ctx = document.getElementById("riskChart");

    const labels = states
        .slice(0,10)
        .map(s=>s.state);

    const values = states
        .slice(0,10)
        .map(s=>s.risk_score);

    new Chart(ctx,{

        type:"bar",

        data:{

            labels:labels,

            datasets:[{

                label:"Risk Score",

                data:values

            }]

        },

        options:{

            responsive:true,

            scales:{
                y:{
                    beginAtZero:true,
                    max:1
                }
            }

        }

    });

}


document.addEventListener(
    "DOMContentLoaded",
    loadDashboard
);