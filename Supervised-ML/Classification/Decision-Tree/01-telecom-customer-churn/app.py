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
MODEL_PATH = ROOT / "artifacts" / "decision_tree_churn_pipeline.joblib"
METADATA_PATH = ROOT / "artifacts" / "model_metadata.json"

st.set_page_config(
    page_title="Customer Churn Studio",
    page_icon=Image.open(LOGO_PATH),
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    :root { --brand:#be123c; --brand-dark:#881337; --ink:#1f1720; --soft:#fff1f2; }
    .stApp { background: linear-gradient(180deg,#fff 0,#fff8f9 42%,#fff 100%); }
    .block-container { max-width: 1280px; padding-top: 1.5rem; padding-bottom: 4rem; }
    .brand-hero { display:flex; gap:1.25rem; align-items:center; padding:1.65rem 1.8rem;
      border-radius:22px; color:white; background:linear-gradient(125deg,#4c0519 0%,#9f1239 48%,#e11d48 100%);
      box-shadow:0 18px 45px rgba(136,19,55,.22); margin-bottom:1.25rem; }
    .brand-hero img { width:78px; height:78px; object-fit:contain; border-radius:18px; background:white; padding:7px; }
    .brand-hero h1 { color:white; margin:0; font-size:clamp(1.8rem,4vw,2.65rem); line-height:1.05; }
    .brand-hero p { color:#ffe4e6; margin:.55rem 0 0; max-width:760px; font-size:1.02rem; }
    .eyebrow { color:#fecdd3; text-transform:uppercase; letter-spacing:.16em; font-size:.75rem; font-weight:800; }
    div[data-testid="stMetric"] { background:white; border:1px solid #fecdd3; border-radius:16px; padding:1rem; }
    div[data-testid="stForm"] { background:rgba(255,255,255,.82); border:1px solid #fecdd3; border-radius:18px; padding:1.1rem; }
    .stButton button, .stDownloadButton button, button[kind="primary"] { border-radius:999px !important; }
    button[kind="primary"] { background:#be123c !important; border-color:#be123c !important; }
    [data-testid="stSidebar"] { background:#fff7f8; border-right:1px solid #fecdd3; }
    </style>
    """,
    unsafe_allow_html=True,
)


def logo_uri() -> str:
    return "data:image/png;base64," + base64.b64encode(LOGO_PATH.read_bytes()).decode("ascii")


@st.cache_resource(show_spinner="Loading the churn model...")
def load_model_assets():
    if not MODEL_PATH.exists() or not METADATA_PATH.exists():
        raise FileNotFoundError("Run decision_tree_churn.ipynb to create the artifacts folder.")
    return joblib.load(MODEL_PATH), json.loads(METADATA_PATH.read_text(encoding="utf-8"))


model, metadata = load_model_assets()
positive_index = list(model.classes_).index(metadata.get("positive_class", "Yes"))

st.markdown(
    f"""
    <section class="brand-hero">
      <img src="{logo_uri()}" alt="A brand logo">
      <div><div class="eyebrow">Decision Tree · Customer experience</div>
      <h1>Customer Churn Studio</h1>
      <p>Explore a sample customer profile, understand the model's estimated churn signal, and review the limitations in plain language.</p></div>
    </section>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.image(LOGO_PATH, width=74)
    st.markdown("### Churn Studio")
    page = st.radio("Choose a workspace", ["Customer check", "Batch scoring", "Model guide"])
    st.divider()
    st.caption("Educational demonstration")
    st.warning("This score describes patterns in sample historical data. It is not a reason to penalise or deny service to a customer.")

CATEGORIES = {
    "gender": ["Female", "Male"],
    "SeniorCitizen": [0, 1],
    "Partner": ["No", "Yes"],
    "Dependents": ["No", "Yes"],
    "PhoneService": ["No", "Yes"],
    "MultipleLines": ["No", "Yes", "No phone service"],
    "InternetService": ["DSL", "Fiber optic", "No"],
    "OnlineSecurity": ["No", "Yes", "No internet service"],
    "OnlineBackup": ["No", "Yes", "No internet service"],
    "DeviceProtection": ["No", "Yes", "No internet service"],
    "TechSupport": ["No", "Yes", "No internet service"],
    "StreamingTV": ["No", "Yes", "No internet service"],
    "StreamingMovies": ["No", "Yes", "No internet service"],
    "Contract": ["Month-to-month", "One year", "Two year"],
    "PaperlessBilling": ["No", "Yes"],
    "PaymentMethod": ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"],
}

LABELS = {
    "gender": "Customer gender", "SeniorCitizen": "Senior citizen", "Partner": "Has a partner",
    "Dependents": "Has dependents", "tenure": "Months with the service", "PhoneService": "Phone service",
    "MultipleLines": "Multiple phone lines", "InternetService": "Internet service", "OnlineSecurity": "Online security",
    "OnlineBackup": "Online backup", "DeviceProtection": "Device protection", "TechSupport": "Technical support",
    "StreamingTV": "Streaming TV", "StreamingMovies": "Streaming movies", "Contract": "Contract type",
    "PaperlessBilling": "Paperless billing", "PaymentMethod": "Payment method", "MonthlyCharges": "Monthly charge",
    "TotalCharges": "Total charges",
}


def select_value(key: str, default):
    options = CATEGORIES[key]
    index = options.index(default) if default in options else 0
    if key == "SeniorCitizen":
        return st.selectbox(
            LABELS[key], options, index=index,
            format_func=lambda value: "Yes" if value == 1 else "No",
        )
    return st.selectbox(LABELS[key], options, index=index)


if page == "Customer check":
    st.subheader("Build a customer profile")
    st.caption("Choose familiar values. The app converts them into the exact schema used by the trained pipeline.")
    with st.form("churn_profile"):
        st.markdown("#### Household and account")
        c1, c2, c3 = st.columns(3)
        with c1:
            gender = select_value("gender", "Female")
            senior = select_value("SeniorCitizen", 0)
            partner = select_value("Partner", "Yes")
        with c2:
            dependents = select_value("Dependents", "No")
            tenure = st.slider(LABELS["tenure"], 0, 72, 24)
            contract = select_value("Contract", "Month-to-month")
        with c3:
            paperless = select_value("PaperlessBilling", "Yes")
            payment = select_value("PaymentMethod", "Electronic check")
            phone = select_value("PhoneService", "Yes")

        st.markdown("#### Services and billing")
        s1, s2, s3 = st.columns(3)
        with s1:
            multiple = select_value("MultipleLines", "No")
            internet = select_value("InternetService", "Fiber optic")
            security = select_value("OnlineSecurity", "No")
        with s2:
            backup = select_value("OnlineBackup", "No")
            protection = select_value("DeviceProtection", "No")
            support = select_value("TechSupport", "No")
        with s3:
            tv = select_value("StreamingTV", "Yes")
            movies = select_value("StreamingMovies", "Yes")
            monthly = st.number_input(LABELS["MonthlyCharges"], min_value=0.0, value=79.50, step=1.0)
            total = st.number_input(LABELS["TotalCharges"], min_value=0.0, value=float(monthly * max(tenure, 1)), step=10.0)
        submitted = st.form_submit_button("Estimate churn signal", type="primary", use_container_width=True)

    if submitted:
        row = pd.DataFrame([{
            "gender": gender, "SeniorCitizen": senior, "Partner": partner, "Dependents": dependents,
            "tenure": tenure, "PhoneService": phone, "MultipleLines": multiple, "InternetService": internet,
            "OnlineSecurity": security, "OnlineBackup": backup, "DeviceProtection": protection,
            "TechSupport": support, "StreamingTV": tv, "StreamingMovies": movies, "Contract": contract,
            "PaperlessBilling": paperless, "PaymentMethod": payment, "MonthlyCharges": monthly,
            "TotalCharges": total,
        }])
        probability = float(model.predict_proba(row)[0, positive_index])
        prediction = str(model.predict(row)[0])
        st.divider()
        a, b, c = st.columns(3)
        a.metric("Estimated churn signal", f"{probability:.1%}")
        b.metric("Model class", prediction)
        c.metric("Profile completeness", "19 / 19")
        st.progress(probability, text=f"Estimated probability of the historical 'Yes' label: {probability:.1%}")
        if prediction == "Yes":
            st.warning("The model found a stronger churn pattern. Review service quality and customer needs; do not treat this as a confirmed future action.")
        else:
            st.success("The model found a lower churn pattern for this profile. Continue monitoring service experience and changing needs.")
        report = row.assign(churn_probability=probability, predicted_label=prediction)
        st.download_button("Download this result", report.to_csv(index=False), "churn_profile_result.csv", "text/csv")

elif page == "Batch scoring":
    st.subheader("Score a customer file")
    st.write("Upload a CSV containing the 19 fields listed below. Extra columns are ignored.")
    template = pd.DataFrame(columns=metadata["input_features"])
    st.download_button("Download CSV template", template.to_csv(index=False), "churn_input_template.csv", "text/csv")
    upload = st.file_uploader("Choose a CSV file", type="csv")
    if upload is not None:
        try:
            raw = pd.read_csv(upload)
            missing = [column for column in metadata["input_features"] if column not in raw.columns]
            if missing:
                st.error("Missing columns: " + ", ".join(missing))
            else:
                clean = raw[metadata["input_features"]].copy()
                probabilities = model.predict_proba(clean)[:, positive_index]
                result = raw.copy()
                result["churn_probability"] = probabilities
                result["predicted_label"] = model.predict(clean)
                st.success(f"Scored {len(result):,} customer rows.")
                st.dataframe(result.head(100), use_container_width=True)
                st.download_button("Download scored CSV", result.to_csv(index=False), "churn_predictions.csv", "text/csv")
        except Exception as exc:
            st.error(f"Could not score this file: {exc}")

else:
    st.subheader("How to read this model")
    a, b, c = st.columns(3)
    a.metric("Algorithm", "Decision Tree")
    b.metric("Inputs", len(metadata["input_features"]))
    c.metric("Positive class", metadata["positive_class"])
    st.markdown("""
    **What the result means**

    The percentage is the fitted tree's estimate for the historical `Churn = Yes` label. It is based on the training examples that reached the same tree leaf. It is not a calibrated promise about what a real customer will do.

    **Responsible use**

    Use the result to learn how a Decision Tree pipeline behaves. Any real retention workflow needs current representative data, privacy review, subgroup evaluation, monitoring, and human judgement.
    """)
    with st.expander("Exact model inputs"):
        st.code("\n".join(metadata["input_features"]))

st.caption("Built with Streamlit · Crimson A brand system · Python 3.12")
