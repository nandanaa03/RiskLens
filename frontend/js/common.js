/* =====================================================
   RiskLens - Common JS (Global Utilities)
   This file will be used across ALL pages
===================================================== */

/* ===============================
   Global State (for future API)
=============================== */

const AppState = {
    dashboard: null,
    analytics: null,
    states: null
};

/* ===============================
   Utility: Format numbers
=============================== */

function formatNumber(num) {
    if (num === null || num === undefined) return "-";
    return Number(num).toFixed(2);
}

/* ===============================
   Utility: Get DOM element
=============================== */

function get(id) {
    return document.getElementById(id);
}

async function loadDashboardData() {

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/api/summary"
        );

        const data = await response.json();

        AppState.dashboard = data;

        if (get("totalStates"))
            get("totalStates").innerText = data.states_loaded;

        if (get("avgRisk"))
            get("avgRisk").innerText = data.average_risk;

        if (get("criticalStates"))
            get("criticalStates").innerText = data.critical_states;

        if (get("clusters"))
            get("clusters").innerText = data.clusters;

    }

    catch(error){

        console.error(error);

    }

}
/* ===============================
   Highlight Active Sidebar Link
=============================== */

function setActiveMenu() {

    const links = document.querySelectorAll(".menu a");

    links.forEach(link => {

        if (link.href === window.location.href) {
            link.classList.add("active");
        }

    });

}

/* ===============================
   Simple Loader (future use)
=============================== */

function showLoader() {
    console.log("Loading...");
}

/* ===============================
   Init function (runs on every page)
=============================== */

function initApp() {

    setActiveMenu();

    loadDashboardData();

}

/* ===============================
   Run on page load
=============================== */

document.addEventListener("DOMContentLoaded", initApp);