from __future__ import annotations

import base64
import json
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st
from PIL import Image

ROOT = Path(__file__).resolve().parent
LOGO_PATH = ROOT / "assets" / "a-logo.png"
ARTIFACT_DIR = ROOT / "artifacts"
DATA_PATH = ROOT / "data" / "insurance_claims.csv"
MODEL_PATH = ARTIFACT_DIR / "insurance_fraud_pipeline.joblib"
THRESHOLD_PATH = ARTIFACT_DIR / "decision_threshold.joblib"
METADATA_PATH = ARTIFACT_DIR / "model_metadata.json"

st.set_page_config(page_title="Insurance Claim Review Studio", page_icon=Image.open(LOGO_PATH), layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
.stApp {background:linear-gradient(180deg,#fff 0,#fff7f8 46%,#fff 100%)}
.block-container {max-width:1320px;padding-top:1.5rem;padding-bottom:4rem}
.brand-hero {display:flex;gap:1.25rem;align-items:center;padding:1.65rem 1.8rem;border-radius:22px;background:linear-gradient(125deg,#4c0519,#9f1239 48%,#e11d48);color:white;box-shadow:0 18px 45px rgba(136,19,55,.22)}
.brand-hero img {width:78px;height:78px;object-fit:contain;border-radius:18px;background:white;padding:7px}
.brand-hero h1 {color:white;margin:0;font-size:clamp(1.8rem,4vw,2.65rem);line-height:1.05}
.brand-hero p {color:#ffe4e6;margin:.5rem 0 0;max-width:780px}.eyebrow {color:#fecdd3;text-transform:uppercase;letter-spacing:.16em;font-size:.75rem;font-weight:800}
div[data-testid="stMetric"],div[data-testid="stForm"] {background:white;border:1px solid #fecdd3;border-radius:16px;padding:1rem}
button[kind="primary"] {background:#be123c!important;border-color:#be123c!important;border-radius:999px!important}.stDownloadButton button{border-radius:999px!important}
[data-testid="stSidebar"] {background:#fff7f8;border-right:1px solid #fecdd3}
</style>
""", unsafe_allow_html=True)


@st.cache_resource(show_spinner="Loading the claim-review model...")
def load_assets():
    missing = [path.name for path in (MODEL_PATH, THRESHOLD_PATH, METADATA_PATH) if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing model files: " + ", ".join(missing) + ". Run the notebook first.")
    return joblib.load(MODEL_PATH), float(joblib.load(THRESHOLD_PATH)), json.loads(METADATA_PATH.read_text(encoding="utf-8"))


@st.cache_data(show_spinner=False)
def load_reference_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH) if DATA_PATH.exists() else pd.DataFrame()


model, threshold, metadata = load_assets()
reference = load_reference_data()
features = metadata["feature_columns"]
numeric_features = set(metadata["numeric_features"])
categorical_features = set(metadata["categorical_features"])

logo = "data:image/png;base64," + base64.b64encode(LOGO_PATH.read_bytes()).decode("ascii")
st.markdown(f"""<section class="brand-hero"><img src="{logo}" alt="A brand logo"><div><div class="eyebrow">Logistic Regression · Claim analytics</div><h1>Insurance Claim Review Studio</h1><p>Explore the dataset's reported-fraud label with guided choices, clear explanations, and downloadable results.</p></div></section>""", unsafe_allow_html=True)

with st.sidebar:
    st.image(LOGO_PATH, width=74)
    st.markdown("### Claim Review Studio")
    page = st.radio("Choose a workspace", ["Claim check", "Batch scoring", "Model performance", "About & limitations"])
    st.divider()
    st.metric("Decision threshold", f"{threshold:.0%}")
    st.warning("Educational demonstration only. A model score is not proof of fraud and must not be used to deny a claim.")

LABELS = {
    "months_as_customer":"Months as a customer","age":"Customer age","policy_state":"Policy state","policy_csl":"Coverage limit","policy_deductable":"Policy deductible","policy_annual_premium":"Annual premium","umbrella_limit":"Umbrella coverage limit","insured_sex":"Customer gender","insured_education_level":"Education level","insured_occupation":"Occupation","insured_hobbies":"Primary hobby","insured_relationship":"Relationship on policy","capital-gains":"Capital gains","capital-loss":"Capital loss","incident_type":"Incident type","collision_type":"Collision type","incident_severity":"Incident severity","authorities_contacted":"Authority contacted","incident_state":"Incident state","incident_city":"Incident city","incident_hour_of_the_day":"Incident hour","number_of_vehicles_involved":"Vehicles involved","property_damage":"Property damage reported","bodily_injuries":"Bodily injuries","witnesses":"Witnesses","police_report_available":"Police report available","total_claim_amount":"Total claim amount","injury_claim":"Injury claim amount","property_claim":"Property claim amount","vehicle_claim":"Vehicle claim amount","auto_make":"Vehicle make","auto_model":"Vehicle model","auto_year":"Vehicle year",
}
SECTIONS = {
    "Customer and policy":["months_as_customer","age","policy_state","policy_csl","policy_deductable","policy_annual_premium","umbrella_limit","insured_sex","insured_education_level","insured_occupation","insured_hobbies","insured_relationship"],
    "Incident details":["incident_type","collision_type","incident_severity","authorities_contacted","incident_state","incident_city","incident_hour_of_the_day","number_of_vehicles_involved","property_damage","bodily_injuries","witnesses","police_report_available"],
    "Claim amounts":["capital-gains","capital-loss","total_claim_amount","injury_claim","property_claim","vehicle_claim"],
    "Vehicle":["auto_make","auto_model","auto_year"],
}


def category_options(column: str) -> list[str]:
    if column in reference.columns:
        return sorted(reference[column].dropna().astype(str).unique().tolist())
    return ["Unknown"]


def numeric_default(column: str) -> float:
    if column in reference.columns:
        values = pd.to_numeric(reference[column], errors="coerce").dropna()
        if not values.empty:
            return float(values.median())
    return 0.0


def render_claim_form() -> dict[str, object]:
    values: dict[str, object] = {}
    integer_fields = {"months_as_customer","age","incident_hour_of_the_day","number_of_vehicles_involved","bodily_injuries","witnesses","auto_year"}
    for section, columns in SECTIONS.items():
        with st.expander(section, expanded=section in {"Customer and policy","Incident details"}):
            grid = st.columns(3)
            for index, column in enumerate(columns):
                with grid[index % 3]:
                    label = LABELS.get(column, column.replace("_", " ").title())
                    if column in categorical_features:
                        values[column] = st.selectbox(label, category_options(column), key=f"claim_{column}")
                    else:
                        default = numeric_default(column)
                        is_integer = column in integer_fields
                        values[column] = st.number_input(label, value=int(default) if is_integer else float(default), step=1 if is_integer else 100.0, key=f"claim_{column}")
    return values


if page == "Claim check":
    st.subheader("Build a claim profile")
    st.caption("Dropdowns contain categories from the documented training snapshot. Numeric fields start at representative median values.")
    with st.form("claim_form"):
        values = render_claim_form()
        submitted = st.form_submit_button("Estimate reported-fraud signal", type="primary", use_container_width=True)
    if submitted:
        row = pd.DataFrame([{column: values[column] for column in features}])
        probability = float(model.predict_proba(row)[0, 1])
        predicted = int(probability >= threshold)
        st.divider()
        a,b,c = st.columns(3)
        a.metric("Estimated label probability", f"{probability:.1%}")
        b.metric("Saved threshold", f"{threshold:.0%}")
        c.metric("Model class", "Reported fraud label" if predicted else "No reported fraud label")
        st.progress(probability, text=f"Estimated probability for the dataset's positive label: {probability:.1%}")
        st.warning("This result predicts a historical dataset label. It does not establish whether fraud occurred.")
        report = row.assign(reported_fraud_probability=probability, predicted_class=predicted)
        st.download_button("Download this result", report.to_csv(index=False), "claim_review_result.csv", "text/csv")

elif page == "Batch scoring":
    st.subheader("Score a claim file")
    st.write("Upload a CSV with the expected model columns. Extra columns are preserved in the downloaded output.")
    st.download_button("Download CSV template", pd.DataFrame(columns=features).to_csv(index=False), "insurance_claim_template.csv", "text/csv")
    upload = st.file_uploader("Choose a CSV file", type="csv")
    if upload is not None:
        try:
            batch = pd.read_csv(upload)
            missing = [column for column in features if column not in batch.columns]
            if missing:
                st.error("Missing columns: " + ", ".join(missing))
            elif len(batch) > 10_000:
                st.error("This educational app accepts up to 10,000 rows per file.")
            else:
                clean = batch[features].copy()
                for column in numeric_features:
                    clean[column] = pd.to_numeric(clean[column], errors="coerce")
                probabilities = model.predict_proba(clean)[:, 1]
                result = batch.copy()
                result["reported_fraud_probability"] = probabilities
                result["predicted_class"] = (probabilities >= threshold).astype(int)
                st.success(f"Scored {len(result):,} claim rows.")
                st.dataframe(result.head(100), use_container_width=True)
                st.download_button("Download scored CSV", result.to_csv(index=False), "insurance_claim_predictions.csv", "text/csv")
        except Exception as exc:
            st.error(f"Could not score this file: {exc}")

elif page == "Model performance":
    st.subheader("Held-out notebook metrics")
    columns = st.columns(3)
    for index,(name,value) in enumerate(metadata.get("metrics_test", {}).items()):
        columns[index % 3].metric(name.replace("_", " ").title(), f"{value:.3f}")
    st.info("These metrics describe one held-out split from the educational notebook. They are not independently validated production performance.")

else:
    st.subheader("Dataset and limitations")
    st.markdown(f"- **Target:** `{metadata.get('target_column')}`\n- **Positive label:** {metadata.get('positive_class_label')}\n- **Model inputs:** {len(features)}\n- **Dataset source:** [Documented source record]({metadata.get('dataset_record')})")
    st.error("Historical labels may reflect investigation and reporting practices. Some fields may contain post-event information and require a documented leakage review.")
    st.write("Do not use this demonstration to deny claims, change premiums, accuse a person, or automate any consequential decision.")

st.caption("Built with Streamlit · Crimson A brand system · Python 3.12")
