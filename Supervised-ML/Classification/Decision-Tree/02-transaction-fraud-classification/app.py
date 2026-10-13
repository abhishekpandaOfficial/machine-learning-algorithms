"""Friendly Streamlit interface for the Transaction Fraud Lab."""
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
FEATURES = ["Time", *[f"V{i}" for i in range(1, 29)], "Amount"]


@st.cache_resource
def load_model_assets():
    if not MODEL_PATH.is_file() or not METADATA_PATH.is_file():
        raise FileNotFoundError(
            "The model files are not available. Run train_model.py before starting the app."
        )
    return joblib.load(MODEL_PATH), json.loads(METADATA_PATH.read_text(encoding="utf-8"))


def example_frame(kind: str) -> pd.DataFrame:
    """Return understandable demo inputs without exposing the PCA controls."""
    values = {feature: 0.0 for feature in FEATURES}
    if kind == "Higher review signal":
        values.update({"Time": 120000.0, "V4": 3.2, "V10": -4.5, "V12": -3.5, "V14": -6.0, "Amount": 850.0})
    elif kind == "Large online purchase":
        values.update({"Time": 90000.0, "V4": 1.8, "V10": -2.0, "V14": -2.5, "Amount": 1200.0})
    else:
        values.update({"Time": 50000.0, "V4": 0.2, "V10": 0.1, "V14": 0.0, "Amount": 45.0})
    return pd.DataFrame([values], columns=FEATURES)


def validate_frame(frame: pd.DataFrame, expected_features: list[str]) -> pd.DataFrame:
    missing = sorted(set(expected_features) - set(frame.columns))
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(missing))
    cleaned = frame[expected_features].apply(pd.to_numeric, errors="coerce")
    if cleaned.isna().any().any():
        bad = cleaned.columns[cleaned.isna().any()].tolist()
        raise ValueError("These columns must contain numbers: " + ", ".join(bad))
    return cleaned


st.set_page_config(
    page_title="Transaction Fraud Lab",
    page_icon=Image.open(LOGO_PATH),
    layout="wide",
    initial_sidebar_state="expanded",
)

logo = "data:image/png;base64," + base64.b64encode(LOGO_PATH.read_bytes()).decode("ascii")
st.markdown(
    f"""
    <style>
    .stApp {{ background:linear-gradient(180deg,#fff 0,#fff7f8 48%,#fff 100%); }}
    .block-container {{ max-width:1180px; padding-top:1.5rem; padding-bottom:4rem; }}
    .brand-hero {{ display:flex; gap:1.25rem; align-items:center; padding:1.7rem 1.85rem;
      border-radius:22px; background:linear-gradient(125deg,#4c0519,#9f1239 50%,#e11d48);
      color:white; box-shadow:0 18px 45px rgba(136,19,55,.22); }}
    .brand-hero img {{ width:78px; height:78px; object-fit:contain; border-radius:18px;
      background:white; padding:7px; }}
    .brand-hero h1 {{ color:white; margin:0; font-size:clamp(1.8rem,4vw,2.65rem); }}
    .brand-hero p {{ color:#ffe4e6; margin:.5rem 0 0; max-width:760px; }}
    .help-card {{ padding:1rem 1.15rem; border:1px solid #fecdd3; border-radius:14px;
      background:#fff; margin: .5rem 0 1rem; }}
    div[data-testid="stMetric"], div[data-testid="stForm"] {{ background:white;
      border:1px solid #fecdd3; border-radius:16px; padding:1rem; }}
    button[kind="primary"] {{ background:#be123c !important; border-color:#be123c !important;
      border-radius:999px !important; }}
    [data-testid="stSidebar"] {{ background:#fff7f8; border-right:1px solid #fecdd3; }}
    </style>
    <section class="brand-hero"><img src="{logo}" alt="A brand logo"><div>
      <div style="color:#fecdd3;text-transform:uppercase;letter-spacing:.16em;font-size:.75rem;font-weight:800">
        Decision Tree · Educational review tool</div>
      <h1>Transaction Fraud Lab</h1>
      <p>Try a guided example or upload a transaction record to receive a model-based review signal.</p>
    </div></section>
    """,
    unsafe_allow_html=True,
)

try:
    model, metadata = load_model_assets()
except FileNotFoundError as error:
    st.error(str(error))
    st.stop()

threshold = float(metadata["selected_threshold"])
with st.sidebar:
    st.image(LOGO_PATH, width=70)
    st.markdown("### How to use this page")
    st.markdown("1. Choose a simple example or upload a CSV.\n2. Click **Check transaction**.\n3. Treat the result as a review signal only.")
    st.divider()
    st.markdown("### Model information")
    st.write(f"Training transactions: **{metadata['train_rows']:,}**")
    st.write(f"Holdout transactions: **{metadata['test_rows']:,}**")
    st.write(f"Holdout PR-AUC: **{metadata['holdout_pr_auc']:.3f}**")
    st.write(f"Review threshold: **{threshold:.2f}**")
    st.divider()
    st.link_button("View dataset information", metadata["dataset"]["source"])

st.warning(
    "This educational tool does not prove fraud, approve payments, or decline transactions. "
    "Every result needs trained human review and a proper production governance process."
)

st.markdown("### Choose how you want to check a transaction")
mode = st.radio(
    "Input method",
    ["Guided example (recommended)", "Upload a CSV", "Advanced feature editor"],
    horizontal=True,
    label_visibility="collapsed",
)

frame: pd.DataFrame | None = None
if mode == "Guided example (recommended)":
    st.markdown(
        '<div class="help-card"><strong>New to fraud models?</strong> Start here. '
        "These examples let you explore the workflow without technical PCA variables.</div>",
        unsafe_allow_html=True,
    )
    with st.form("guided_check"):
        example = st.selectbox(
            "Choose an example",
            ["Typical low-amount purchase", "Large online purchase", "Higher review signal"],
            help="These are educational examples, not real customer records.",
        )
        st.caption("The model uses anonymised research features behind the scenes.")
        submitted = st.form_submit_button("Check transaction", type="primary", use_container_width=True)
    if submitted:
        frame = example_frame(example)

elif mode == "Upload a CSV":
    st.markdown(
        '<div class="help-card"><strong>For analysts:</strong> upload a CSV containing one or '
        "more rows with the exact columns listed below. Do not upload personal or confidential data.</div>",
        unsafe_allow_html=True,
    )
    st.code(", ".join(FEATURES), language="text")
    uploaded = st.file_uploader("Choose a transaction CSV", type=["csv"])
    if uploaded is not None:
        try:
            uploaded_frame = pd.read_csv(uploaded)
            if len(uploaded_frame) == 0:
                st.error("The CSV is empty.")
            else:
                row_number = st.number_input(
                    "Which row should be checked?",
                    min_value=1,
                    max_value=len(uploaded_frame),
                    value=1,
                    step=1,
                )
                st.dataframe(uploaded_frame.head(5), use_container_width=True, hide_index=True)
                if st.button("Check selected row", type="primary", use_container_width=True):
                    frame = uploaded_frame.iloc[[int(row_number) - 1]]
        except (pd.errors.ParserError, UnicodeDecodeError) as error:
            st.error(f"Could not read this CSV: {error}")

else:
    st.markdown(
        '<div class="help-card"><strong>Advanced mode:</strong> the public dataset anonymises '
        "its inputs as V1–V28. Only use this mode if you already have those research features.</div>",
        unsafe_allow_html=True,
    )
    with st.form("advanced_check"):
        left, right = st.columns(2)
        with left:
            transaction_time = st.number_input("Time (seconds)", min_value=0.0, value=100000.0)
            amount = st.number_input("Amount", min_value=0.0, value=100.0)
        with right:
            st.caption("Leave the anonymised features at zero for a neutral baseline.")
        values = {}
        for start in range(0, 28, 7):
            cols = st.columns(7)
            for col, feature in zip(cols, [f"V{i}" for i in range(1 + start, 8 + start)]):
                with col:
                    values[feature] = st.number_input(feature, value=0.0, format="%.5f")
        submitted = st.form_submit_button("Check transaction", type="primary", use_container_width=True)
    if submitted:
        frame = pd.DataFrame([{"Time": transaction_time, **values, "Amount": amount}], columns=FEATURES)

if frame is not None:
    try:
        clean_frame = validate_frame(frame, metadata["input_features"])
        probability = float(model.predict_proba(clean_frame)[0, list(model.classes_).index(1)])
    except ValueError as error:
        st.error(f"Please correct the input: {error}")
    else:
        st.divider()
        st.markdown("### Review result")
        result_col, explanation_col = st.columns([1, 1.5])
        with result_col:
            st.metric("Model-estimated fraud probability", f"{probability:.2%}")
            st.progress(min(probability, 1.0), text=f"Review threshold: {threshold:.0%}")
        with explanation_col:
            if probability >= threshold:
                st.error("🔎 **Send for human review**")
                st.write("This record is above the configured review threshold.")
            else:
                st.success("✅ **Below the review threshold**")
                st.write("This record is below the configured review threshold.")
            st.caption(
                "A below-threshold result does not certify a transaction as legitimate. "
                "Review the evidence and follow your organisation's controls."
            )
        with st.expander("What does this result mean?"):
            st.markdown(
                "- **Probability** is the model's estimated score for the fraud class.\n"
                "- **Threshold** is an operating point selected during evaluation.\n"
                "- **Human review** is required before any customer or payment action.\n"
                "- This research dataset uses anonymised features and may not represent current transaction behaviour."
            )

st.divider()
st.caption(
    "Dataset: ULB Machine Learning Group · Model: DecisionTreeClassifier · "
    "Educational demonstration only"
)
