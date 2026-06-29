const API = "http://127.0.0.1:8000/api";

let statesData = [];

async function loadStates() {

    try {

        const response = await fetch(`${API}/states`);

        statesData = await response.json();

        renderStates(statesData);

    }

    catch (error) {

        console.error(error);

    }

}

function renderStates(data) {

    const grid = document.getElementById("stateGrid");

    grid.innerHTML = "";

    data.forEach(state => {

        const card = document.createElement("div");

        card.className = "state-card";

        card.innerHTML = `

            <h3>${state.state}</h3>

            <p><b>Risk Score:</b> ${state.risk_score}</p>

            <p><b>Risk Level:</b> ${state.risk_level}</p>

            <p><b>Cluster:</b> ${state.cluster}</p>

            <p><b>Top Driver:</b> ${state.top_driver}</p>

            <button
                class="view-btn"
                onclick="viewState('${state.state}')">

                View Details

            </button>

        `;

        grid.appendChild(card);

    });

}

function setupSearch() {

    const input = document.getElementById("searchInput");

    input.addEventListener("input", function () {

        const value = this.value.toLowerCase();

        const filtered = statesData.filter(state =>

            state.state.toLowerCase().includes(value)

        );

        renderStates(filtered);

    });

}

function viewState(name) {

    window.location.href =
        `state.html?name=${encodeURIComponent(name)}`;

}

document.addEventListener("DOMContentLoaded", () => {

    loadStates();

    setupSearch();

});