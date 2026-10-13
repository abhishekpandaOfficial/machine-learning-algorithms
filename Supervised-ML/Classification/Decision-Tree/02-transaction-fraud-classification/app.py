from __future__ import annotations

import base64
import json
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st
from PIL import Image

ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "artifacts" / "transaction_fraud_tree_pipeline.joblib"
METADATA_PATH = ROOT / "artifacts" / "model_metadata.json"
LOGO_PATH = ROOT / "assets" / "a-logo.png"


@st.cache_resource
def load_model_assets():
    if not MODEL_PATH.is_file() or not METADATA_PATH.is_file():
        raise FileNotFoundError("Model artifacts are missing. Run train_model.py first.")
    return joblib.load(MODEL_PATH), json.loads(METADATA_PATH.read_text(encoding="utf-8"))


st.set_page_config(page_title="Transaction Fraud Lab", page_icon=Image.open(LOGO_PATH), layout="wide")
logo = "data:image/png;base64," + base64.b64encode(LOGO_PATH.read_bytes()).decode("ascii")
st.markdown(
    f"""<style>
    .stApp {{ background:linear-gradient(180deg,#fff 0,#fff7f8 48%,#fff 100%); }}
    .block-container {{ max-width:1200px; padding-top:1.5rem; padding-bottom:4rem; }}
    .brand-hero {{ display:flex; gap:1.25rem; align-items:center; padding:1.7rem 1.85rem; border-radius:22px;
      background:linear-gradient(125deg,#4c0519,#9f1239 50%,#e11d48); color:white; }}
    .brand-hero img {{ width:78px; height:78px; object-fit:contain; border-radius:18px; background:white; padding:7px; }}
    .brand-hero h1 {{ color:white; margin:0; }} .brand-hero p {{ color:#ffe4e6; margin:.5rem 0 0; }}
    </style><section class="brand-hero"><img src="{logo}" alt="A brand logo"><div>
    <h1>Transaction Fraud Lab</h1><p>Real-data Decision Tree review signal using the ULB credit-card fraud dataset.</p>
    </div></section>""",
    unsafe_allow_html=True,
)

try:
    model, metadata = load_model_assets()
except FileNotFoundError as error:
    st.error(str(error))
    st.stop()

st.warning(
    "Educational decision-support only. This score is not proof of fraud and must not "
    "automatically decline a transaction."
)
with st.sidebar:
    st.image(LOGO_PATH, width=74)
    st.subheader("Model contract")
    st.write(f"Rows used for training: {metadata['train_rows']:,}")
    st.write(f"Time-ordered holdout rows: {metadata['test_rows']:,}")
    st.write(f"Holdout PR-AUC: {metadata['holdout_pr_auc']:.3f}")
    st.write(f"Review threshold: {metadata['selected_threshold']:.2f}")

st.subheader("Authorisation-time transaction features")
st.caption("The source dataset uses anonymised PCA components. Defaults are neutral values; replace them with a reviewed transaction record.")
with st.form("fraud_prediction"):
    col1, col2 = st.columns(2)
    with col1:
        transaction_time = st.number_input("Time (seconds from dataset start)", min_value=0.0, value=100000.0)
        amount = st.number_input("Amount", min_value=0.0, value=100.0)
    with col2:
        st.info("V1–V28 are anonymised PCA features from the public dataset.")
    values = {}
    feature_cols = [f"V{i}" for i in range(1, 29)]
    for start in range(0, len(feature_cols), 7):
        cols = st.columns(7)
        for col, feature in zip(cols, feature_cols[start:start + 7]):
            with col:
                values[feature] = st.number_input(feature, value=0.0, format="%.6f")
    submitted = st.form_submit_button("Assess review signal", type="primary", use_container_width=True)

if submitted:
    row = {"Time": transaction_time, **values, "Amount": amount}
    frame = pd.DataFrame([row], columns=metadata["input_features"])
    probability = float(model.predict_proba(frame)[0, list(model.classes_).index(1)])
    threshold = float(metadata["selected_threshold"])
    st.metric("Estimated fraud probability", f"{probability:.2%}")
    if probability >= threshold:
        st.error("Review signal: this transaction is above the configured review threshold.")
    else:
        st.success("Review signal: this transaction is below the configured review threshold.")
    st.caption("The result is a model score for human review, not a final decision.")

st.divider()
st.caption("Dataset: ULB Machine Learning Group · Model: DecisionTreeClassifier · Streamlit educational lab")
