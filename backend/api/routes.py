from fastapi import APIRouter, HTTPException
from backend.analytics.recommendation import RecommendationEngine
from backend.etl.pipeline import ETLPipeline
from backend.analytics.risk_engine import RiskEngine
from backend.algorithms.cluster import StateCluster

router = APIRouter(prefix="/api", tags=["HealthWatch"])

# ---------- Load data once when server starts ----------

df, summary = ETLPipeline.run("data/raw/NFHS-5-States.csv")

df = RiskEngine.run(df)

df = StateCluster.attach_clusters(df)


# ---------- Helper Function ----------

def state_to_json(row):

    return {

        "state": row["state"],

        "risk_score": round(float(row["Risk Score"]),4),

        "risk_level": row["Risk Level"],

        "cluster": int(row["Cluster"]),

        "top_driver": row["Top Driver"],

        "indicators": {

            "Obesity_W": row["Obesity_W"],
            "Obesity_M": row["Obesity_M"],
            "Anaemia_Child": row["Anaemia_Child"],
            "Anaemia_W": row["Anaemia_W"],
            "BloodSugar_W": row["BloodSugar_W"],
            "BloodSugar_M": row["BloodSugar_M"],
            "Hypertension_W": row["Hypertension_W"],
            "Hypertension_M": row["Hypertension_M"]

        },

        "recommendations":

            RecommendationEngine.get_recommendations(

                row["Top Driver"],

                row["Risk Level"]

            )
    }

# =====================================================
# SUMMARY
# =====================================================

@router.get("/summary")
def summary_api():

    return {

        "states_loaded": summary["states_loaded"],

        "columns": summary["columns"],

        "critical_states":
            int((df["Risk Level"] == "Critical").sum()),

        "high_states":
            int((df["Risk Level"] == "High").sum()),

        "moderate_states":
            int((df["Risk Level"] == "Moderate").sum()),

        "low_states":
            int((df["Risk Level"] == "Low").sum()),

        "clusters":
            int(df["Cluster"].nunique()),

        "average_risk":
            round(float(df["Risk Score"].mean()), 4)
    }


# =====================================================
# ALL STATES
# =====================================================

@router.get("/states")
def all_states():

    data = df.sort_values(
        by="Risk Score",
        ascending=False
    )

    return [
        state_to_json(row)
        for _, row in data.iterrows()
    ]


# =====================================================
# SINGLE STATE
# =====================================================

@router.get("/state/{state_name}")
def single_state(state_name: str):

    state = df[
        df["state"].str.lower() ==
        state_name.lower()
    ]

    if state.empty:

        raise HTTPException(
            status_code=404,
            detail="State not found"
        )

    return state_to_json(state.iloc[0])


# =====================================================
# CLUSTERS
# =====================================================

@router.get("/clusters")
def clusters():

    output = []

    for cluster_id in sorted(df["Cluster"].unique()):

        cluster = df[
            df["Cluster"] == cluster_id
        ]

        output.append({

            "cluster":

                int(cluster_id),

            "states":

                cluster["state"].tolist(),

            "average_risk":

                round(
                    float(cluster["Risk Score"].mean()),
                    4
                )
        })

    return output

@router.get("/recommendations/{state_name}")

def recommendations(state_name: str):

    state = df[

        df["state"].str.lower() ==

        state_name.lower()

    ]

    if state.empty:

        raise HTTPException(

            status_code=404,

            detail="State not found"

        )

    row = state.iloc[0]

    return {

        "state": row["state"],

        "top_driver": row["Top Driver"],

        "risk_level": row["Risk Level"],

        "recommendations":

            RecommendationEngine.get_recommendations(

                row["Top Driver"],

                row["Risk Level"]

            )

    }

@router.get("/compare/{state1}/{state2}")
def compare_states(state1: str, state2: str):

    first = df[
        df["state"].str.lower() == state1.lower()
    ]

    second = df[
        df["state"].str.lower() == state2.lower()
    ]

    if first.empty or second.empty:

        raise HTTPException(
            status_code=404,
            detail="One or both states not found."
        )

    return {

        "state1": state_to_json(first.iloc[0]),

        "state2": state_to_json(second.iloc[0])

    }
@router.get("/correlation")
def correlation():

    columns = [

        "Obesity_W",
        "Obesity_M",
        "Anaemia_Child",
        "Anaemia_W",
        "BloodSugar_W",
        "BloodSugar_M",
        "Hypertension_W",
        "Hypertension_M"

    ]

    return df[columns].corr().round(3).to_dict()