"""Two-mode, non-technical Transaction Fraud Lab interface."""
from __future__ import annotations

import base64
import io
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


def csv_template() -> bytes:
    """Create an empty, correctly ordered bulk-upload template."""
    return pd.DataFrame([{feature: 0.0 for feature in FEATURES}]).to_csv(index=False).encode("utf-8")


def score_questionnaire(
    amount: float,
    channel: str,
    location: str,
    device: str,
    velocity: str,
    authentication: str,
    account_age: str,
) -> tuple[int, list[str]]:
    """Return an educational, rule-based screening score, not a model prediction."""
    score = 0
    reasons: list[str] = []
    if amount > 1000:
        score += 25
        reasons.append("The transaction amount is high.")
    elif amount > 500:
        score += 12
        reasons.append("The transaction amount is above the usual small-purchase range.")
    if channel in {"Online checkout", "Bank transfer"}:
        score += 15
        reasons.append("This channel commonly receives additional verification.")
    if location == "International location":
        score += 20
        reasons.append("The location is different from the usual domestic pattern.")
    elif location == "New domestic location":
        score += 8
        reasons.append("The location is new for this account.")
    if device == "New device":
        score += 18
        reasons.append("The device has not been seen before.")
    elif device == "Recently seen device":
        score += 7
        reasons.append("The device was only recently seen.")
    if velocity == "Unusually rapid transactions":
        score += 18
        reasons.append("Transaction velocity is unusually high.")
    elif velocity == "Several transactions":
        score += 8
        reasons.append("Several recent transactions were reported.")
    if authentication == "Authentication failed":
        score += 25
        reasons.append("Authentication failed.")
    elif authentication == "Standard authentication":
        score += 5
    if account_age == "New account":
        score += 12
        reasons.append("The account is new.")
    elif account_age == "Recently opened account":
        score += 6
        reasons.append("The account was opened recently.")
    return min(score, 100), reasons


def validate_bulk_frame(frame: pd.DataFrame) -> pd.DataFrame:
    missing = sorted(set(FEATURES) - set(frame.columns))
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(missing))
    cleaned = frame[FEATURES].apply(pd.to_numeric, errors="coerce")
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
      background:#fff; margin:.5rem 0 1rem; }}
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
      <p>Answer simple questions for an educational screening score, or upload research-format data for the trained model.</p>
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
    st.markdown("### Start here")
    st.markdown("Choose one of the two tabs. Do not upload personal, confidential, or live customer data.")
    st.divider()
    st.markdown("### Trained model")
    st.write(f"Training transactions: **{metadata['train_rows']:,}**")
    st.write(f"Holdout PR-AUC: **{metadata['holdout_pr_auc']:.3f}**")
    st.write(f"Review threshold: **{threshold:.0%}**")
    st.divider()
    st.link_button("View dataset information", metadata["dataset"]["source"])

st.warning(
    "This educational tool does not prove fraud, approve payments, or decline transactions. "
    "Every result needs trained human review."
)

manual_tab, bulk_tab = st.tabs(["🧭 Manual questionnaire", "📁 Bulk upload"])

with manual_tab:
    st.markdown(
        '<div class="help-card"><strong>For everyone:</strong> answer the questions below using '
        "the information you have. This is a transparent educational screening score; it is not "
        "the trained ULB model because that dataset uses anonymised research features.</div>",
        unsafe_allow_html=True,
    )
    with st.form("manual_questionnaire"):
        left, middle, right = st.columns(3)
        with left:
            amount = st.number_input("Transaction amount", min_value=0.0, value=100.0, step=10.0)
            channel = st.selectbox(
                "How was it paid?",
                ["Card present", "Online checkout", "Mobile wallet", "Bank transfer"],
            )
            location = st.selectbox(
                "Where was it made?",
                ["Usual location", "New domestic location", "International location"],
            )
        with middle:
            device = st.selectbox(
                "Is the device familiar?",
                ["Known device", "Recently seen device", "New device"],
            )
            velocity = st.selectbox(
                "Recent transaction activity",
                ["Normal frequency", "Several transactions", "Unusually rapid transactions"],
            )
            authentication = st.selectbox(
                "Authentication result",
                ["Strong authentication passed", "Standard authentication", "Authentication failed"],
            )
        with right:
            account_age = st.selectbox(
                "How old is the account?",
                ["Established account", "Recently opened account", "New account"],
            )
            st.info("These questions are intentionally simple. They are not claims about the anonymised research features.")
        manual_submitted = st.form_submit_button("Calculate screening score", type="primary", use_container_width=True)

    if manual_submitted:
        score, reasons = score_questionnaire(
            amount, channel, location, device, velocity, authentication, account_age
        )
        st.divider()
        st.subheader("Educational screening result")
        result_col, detail_col = st.columns([1, 1.5])
        with result_col:
            st.metric("Screening score", f"{score}/100")
            st.progress(score / 100)
        with detail_col:
            if score >= 60:
                st.error("🔎 Consider additional human review")
            elif score >= 30:
                st.warning("⚠️ Consider verifying the transaction details")
            else:
                st.success("✅ Lower screening concern")
            st.caption("This rule-based score is a teaching aid, not a trained-model probability.")
        with st.expander("Why did the score change?"):
            if reasons:
                for reason in reasons:
                    st.write(f"- {reason}")
            else:
                st.write("No elevated indicators were selected.")

with bulk_tab:
    st.markdown(
        '<div class="help-card"><strong>For analysts:</strong> use the trained Decision Tree with '
        "one or many rows from the real ULB dataset. The model expects anonymised research columns, "
        "not business questions.</div>",
        unsafe_allow_html=True,
    )
    st.download_button(
        "⬇️ Download CSV template",
        data=csv_template(),
        file_name="transaction_fraud_model_template.csv",
        mime="text/csv",
        use_container_width=True,
    )
    st.caption("The template contains `Time`, `V1`–`V28`, and `Amount`. Do not rename or reorder columns.")
    uploaded = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])
    if uploaded is not None:
        try:
            if uploaded.name.lower().endswith(".xlsx"):
                bulk_frame = pd.read_excel(io.BytesIO(uploaded.getvalue()))
            else:
                bulk_frame = pd.read_csv(uploaded)
            clean_bulk = validate_bulk_frame(bulk_frame)
            st.success(f"Loaded {len(clean_bulk):,} transaction row(s).")
            st.dataframe(bulk_frame.head(5), use_container_width=True, hide_index=True)
            if st.button("Calculate model scores", type="primary", use_container_width=True):
                probabilities = model.predict_proba(clean_bulk)[:, list(model.classes_).index(1)]
                results = bulk_frame.copy()
                results["fraud_probability"] = probabilities
                results["review_signal"] = probabilities >= threshold
                st.subheader("Trained model results")
                metric_a, metric_b, metric_c = st.columns(3)
                metric_a.metric("Rows checked", f"{len(results):,}")
                metric_b.metric("Rows for review", f"{int(results['review_signal'].sum()):,}")
                metric_c.metric("Highest score", f"{probabilities.max():.2%}")
                st.dataframe(results[["fraud_probability", "review_signal"]].head(100), use_container_width=True)
                st.download_button(
                    "⬇️ Download scored results",
                    data=results.to_csv(index=False).encode("utf-8"),
                    file_name="transaction_fraud_scored_results.csv",
                    mime="text/csv",
                    use_container_width=True,
                )
        except (ValueError, pd.errors.ParserError, UnicodeDecodeError, ImportError) as error:
            st.error(f"Could not process this file: {error}")

st.divider()
st.caption(
    "Dataset: ULB Machine Learning Group · Model: DecisionTreeClassifier · "
    "Educational demonstration only"
)
