from __future__ import annotations

import io
import base64
import json
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image

# -----------------------------------------------------------------------------
# Configuration and model artifacts
# -----------------------------------------------------------------------------
APP_DIR = Path(__file__).resolve().parent
LOGO_PATH = APP_DIR / "assets" / "a-logo.png"
ARTIFACT_DIR = APP_DIR / "artifacts"
MODEL_PATH = ARTIFACT_DIR / "logistic_regression_pipeline.joblib"
THRESHOLD_PATH = ARTIFACT_DIR / "decision_threshold.joblib"
METADATA_PATH = ARTIFACT_DIR / "model_metadata.json"

st.set_page_config(
    page_title="Credit Default Intelligence",
    page_icon=Image.open(LOGO_PATH),
    layout="wide",
    initial_sidebar_state="expanded",
)

# A small visual system for a clean, accessible dashboard.
st.markdown(
    """
    <style>
      .stApp {background:linear-gradient(180deg,#fff 0,#fff7f8 46%,#fff 100%);}
      .block-container {max-width: 1320px; padding-top: 1.5rem; padding-bottom: 3rem;}
      .hero {display:flex;gap:1.25rem;align-items:center;padding:1.65rem 1.8rem;border-radius:22px;
        background:linear-gradient(125deg,#4c0519 0%,#9f1239 48%,#e11d48 100%);color:white;margin-bottom:1.25rem;
        box-shadow:0 18px 45px rgba(136,19,55,.22);}
      .hero img {width:78px;height:78px;object-fit:contain;border-radius:18px;background:white;padding:7px;}
      .hero h1 {margin:0;font-size:clamp(1.8rem,4vw,2.65rem);line-height:1.05;color:white;}
      .hero p {margin:.5rem 0 0;color:#ffe4e6;max-width:780px;}
      .eyebrow {color:#fecdd3;text-transform:uppercase;letter-spacing:.16em;font-size:.75rem;font-weight:800;}
      .metric-card {border:1px solid #fecdd3;padding:1rem;border-radius:16px;min-height:105px;background:white;}
      .muted {color:#6b5560;font-size:.88rem;}
      div[data-testid="stMetric"], div[data-testid="stForm"] {border:1px solid #fecdd3;padding:12px 14px;border-radius:16px;background:white;}
      button[kind="primary"] {background:#be123c !important;border-color:#be123c !important;border-radius:999px !important;}
      .stDownloadButton button {border-radius:999px !important;}
      [data-testid="stSidebar"] {background:#fff7f8;border-right:1px solid #fecdd3;}
    </style>
    """,
    unsafe_allow_html=True,
)

FEATURE_ORDER = [f"x{i}" for i in range(1, 24)]
CATEGORICAL_DEFAULTS = {
    "x2": [1, 2],
    "x3": [0, 1, 2, 3, 4, 5, 6],
    "x4": [0, 1, 2, 3],
    "x6": [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8],
    "x7": [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8],
    "x8": [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8],
    "x9": [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8],
    "x10": [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8],
    "x11": [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8],
}

@st.cache_resource(show_spinner="Loading trained model...")
def load_artifacts():
    missing = [p.name for p in [MODEL_PATH, THRESHOLD_PATH, METADATA_PATH] if not p.exists()]
    if missing:
        raise FileNotFoundError(
            "Missing required model artifact(s): " + ", ".join(missing) +
            ". Confirm the files are committed under the project's artifacts/ directory."
        )
    model = joblib.load(MODEL_PATH)
    threshold = float(joblib.load(THRESHOLD_PATH))
    metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
    if not 0 <= threshold <= 1:
        raise ValueError("The saved decision threshold must be between 0 and 1.")
    model_features = list(getattr(model, "feature_names_in_", metadata.get("feature_names", [])))
    if model_features and set(model_features) != set(FEATURE_ORDER):
        raise ValueError(
            "Model feature schema does not match the app's x1...x23 mapping. "
            f"Model expects: {model_features}"
        )
    if set(metadata.get("feature_names", [])) != set(FEATURE_ORDER):
        raise ValueError("model_metadata.json must describe all 23 x1...x23 features.")
    return model, threshold, metadata

try:
    model, threshold, metadata = load_artifacts()
except Exception as exc:
    st.error(f"The prediction service could not start: {exc}")
    st.stop()

FEATURES: dict[str, dict[str, Any]] = metadata["features"]

# Labels are only used for rendering. Model inputs remain x1...x23.
def feature_info(key: str) -> dict[str, Any]:
    return FEATURES.get(key, {"label": key, "description": "Feature from the training dataset.", "kind": "numeric"})

def show_range(key: str) -> str:
    item = feature_info(key)
    if "min" not in item or "max" not in item:
        return "Training range unavailable"
    return f"Observed training range: {item['min']:,.4g} to {item['max']:,.4g}"

def categorical_options(key: str) -> list[int | float]:
    cats = feature_info(key).get("categories") or CATEGORICAL_DEFAULTS.get(key, [])
    return sorted(cats)

def pretty_category(key: str, value: int | float) -> str:
    code = int(value) if float(value).is_integer() else value
    if key == "x2":
        return {1: "1 — Male", 2: "2 — Female"}.get(code, str(code))
    if key == "x3":
        return {0: "0 — Unknown/unspecified", 1: "1 — Graduate school", 2: "2 — University", 3: "3 — High school", 4: "4 — Other", 5: "5 — Unknown", 6: "6 — Unknown"}.get(code, f"{code} — Other/observed code")
    if key == "x4":
        return {0: "0 — Unknown/unspecified", 1: "1 — Married", 2: "2 — Single", 3: "3 — Other"}.get(code, str(code))
    if key in {"x6", "x7", "x8", "x9", "x10", "x11"}:
        descriptions = {-2: "No consumption", -1: "Paid duly", 0: "Revolving credit / no delay recorded", 1: "Delayed by 1 month", 2: "Delayed by 2 months", 3: "Delayed by 3 months", 4: "Delayed by 4 months", 5: "Delayed by 5 months", 6: "Delayed by 6 months", 7: "Delayed by 7 months", 8: "Delayed by 8+ months"}
        return f"{code} — {descriptions.get(code, 'Observed category')}"
    return str(code)

def make_input_form() -> dict[str, int | float]:
    values: dict[str, int | float] = {}
    sections = [
        ("Customer profile", ["x1", "x2", "x3", "x4", "x5"]),
        ("Repayment history", ["x6", "x7", "x8", "x9", "x10", "x11"]),
        ("Bill statements", ["x12", "x13", "x14", "x15", "x16", "x17"]),
        ("Payment history", ["x18", "x19", "x20", "x21", "x22", "x23"]),
    ]
    defaults = {"x1": 50000, "x2": 1, "x3": 2, "x4": 2, "x5": 35,
                "x6": -1, "x7": -1, "x8": -1, "x9": -1, "x10": -1, "x11": -1}
    for section, keys in sections:
        st.subheader(section)
        st.caption("Enter values in the same units and coding scheme as the training dataset.")
        cols = st.columns(2)
        for idx, key in enumerate(keys):
            item = feature_info(key)
            label = item.get("label", key)
            help_text = f"{item.get('description', '')}\n\n{show_range(key)}"
            with cols[idx % 2]:
                if item.get("kind") == "categorical" or key in CATEGORICAL_DEFAULTS:
                    options = categorical_options(key)
                    if not options:
                        st.warning(f"No valid category metadata found for {key}.")
                        continue
                    default_value = defaults.get(key, options[0])
                    default_index = options.index(default_value) if default_value in options else 0
                    chosen = st.selectbox(
                        label,
                        options=options,
                        index=default_index,
                        format_func=lambda v, k=key: pretty_category(k, v),
                        help=help_text,
                        key=f"single_{key}",
                    )
                    values[key] = int(chosen) if float(chosen).is_integer() else float(chosen)
                else:
                    lo = float(item.get("min", -1_000_000_000))
                    hi = float(item.get("max", 1_000_000_000))
                    median = float(item.get("median", 0))
                    # Do not clamp to the observed training range: permit entry but warn later.
                    broad_min = min(lo, -1_000_000_000.0)
                    broad_max = max(hi, 1_000_000_000.0)
                    default_value = float(defaults.get(key, median))
                    values[key] = st.number_input(
                        label,
                        min_value=broad_min,
                        max_value=broad_max,
                        value=default_value,
                        step=1.0,
                        help=help_text,
                        key=f"single_{key}",
                    )
    return values

def validate_rows(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Validate schema and numeric values; return (valid rows, row errors)."""
    data = frame.copy()
    data.columns = [str(c).strip() for c in data.columns]
    # Accept either raw dataset column names x1...x23 or descriptive UCI names.
    aliases = {
        "LIMIT_BAL":"x1", "SEX":"x2", "EDUCATION":"x3", "MARRIAGE":"x4", "AGE":"x5", "PAY_0":"x6",
        "PAY_2":"x7", "PAY_3":"x8", "PAY_4":"x9", "PAY_5":"x10", "PAY_6":"x11",
        "BILL_AMT1":"x12", "BILL_AMT2":"x13", "BILL_AMT3":"x14", "BILL_AMT4":"x15", "BILL_AMT5":"x16", "BILL_AMT6":"x17",
        "PAY_AMT1":"x18", "PAY_AMT2":"x19", "PAY_AMT3":"x20", "PAY_AMT4":"x21", "PAY_AMT5":"x22", "PAY_AMT6":"x23",
    }
    data = data.rename(columns={c: aliases[c] for c in data.columns if c in aliases})
    missing = [c for c in FEATURE_ORDER if c not in data.columns]
    if missing:
        raise ValueError("Missing required input columns: " + ", ".join(missing))
    data = data[FEATURE_ORDER].copy()
    for col in FEATURE_ORDER:
        data[col] = pd.to_numeric(data[col], errors="coerce")
    errors = []
    valid_mask = data.notna().all(axis=1)
    for idx in data.index[~valid_mask]:
        bad = [c for c in FEATURE_ORDER if pd.isna(data.loc[idx, c])]
        errors.append({"row": int(idx) + 1, "issue": "Missing or non-numeric values: " + ", ".join(bad)})
    # Category validation uses categories recorded in the training set.
    for col in CATEGORICAL_DEFAULTS:
        allowed = set(categorical_options(col))
        bad_mask = data[col].notna() & ~data[col].isin(allowed)
        for idx in data.index[bad_mask]:
            errors.append({"row": int(idx) + 1, "issue": f"{col} has unsupported category {data.loc[idx, col]}"})
            valid_mask.loc[idx] = False
    # Training-range warnings are not hard errors; show them after predictions.
    valid = data.loc[valid_mask].copy()
    error_df = pd.DataFrame(errors, columns=["row", "issue"]).drop_duplicates()
    return valid, error_df

# -----------------------------------------------------------------------------
# Sidebar and header
# -----------------------------------------------------------------------------
st.sidebar.image(LOGO_PATH, width=74)
st.sidebar.title("Credit Default")
st.sidebar.caption("Model-powered educational demonstration")
page = st.sidebar.radio("Workspace", ["Single prediction", "Bulk predictions", "Model information"])
st.sidebar.divider()
st.sidebar.metric("Decision threshold", f"{threshold:.2%}")
st.sidebar.caption("Class 1 is the dataset's default-payment label.")
st.sidebar.warning("Educational demonstration only. Do not use as the sole basis for lending or credit decisions.")

logo_data = base64.b64encode(LOGO_PATH.read_bytes()).decode("ascii")
st.markdown(
    f"<div class='hero'><img src='data:image/png;base64,{logo_data}' alt='A brand logo'><div>"
    "<div class='eyebrow'>Logistic Regression · Credit analytics</div><h1>Credit Default Intelligence</h1>"
    "<p>Explore an estimated next-month default signal with guided inputs, clear validation, and downloadable results.</p></div></div>",
    unsafe_allow_html=True,
)

if page == "Single prediction":
    st.info("Training ranges are shown under each field. Values outside the observed range are allowed but flagged because the model has less evidence for them.")
    with st.form("customer_form"):
        values = make_input_form()
        submitted = st.form_submit_button("Run prediction", type="primary", use_container_width=True)
    if submitted:
        row = pd.DataFrame([{k: values[k] for k in FEATURE_ORDER}])
        warnings = []
        for col in FEATURE_ORDER:
            item = feature_info(col)
            value = float(row.iloc[0][col])
            if "min" in item and "max" in item and (value < float(item["min"]) or value > float(item["max"])):
                warnings.append(f"{item.get('label', col)} = {value:,.4g} is outside the observed training range {float(item['min']):,.4g}–{float(item['max']):,.4g}.")
        try:
            probability = float(model.predict_proba(row[FEATURE_ORDER])[0, 1])
            prediction = int(probability >= threshold)
            st.divider()
            st.subheader("Prediction result")
            m1, m2, m3 = st.columns(3)
            m1.metric("Estimated default probability", f"{probability:.4%}")
            m2.metric("Decision threshold", f"{threshold:.2%}")
            m3.metric("Classification", "Higher default risk" if prediction else "Lower default risk")
            st.progress(min(max(probability, 0.0), 1.0), text=f"Probability of class 1: {probability:.4%}")
            st.caption("Classification is determined by comparing the probability with the saved threshold. The threshold does not change the probability itself.")
            if warnings:
                st.warning("Training-range warnings\n\n" + "\n\n".join(warnings))
            else:
                st.success("All numeric inputs are within their observed training ranges.")
            report = pd.DataFrame([{
                "default_probability": probability,
                "decision_threshold": threshold,
                "predicted_class": prediction,
                "classification": "Higher default risk" if prediction else "Lower default risk",
                **{k: values[k] for k in FEATURE_ORDER},
            }])
            st.download_button("Download prediction report (CSV)", report.to_csv(index=False).encode("utf-8"), "prediction_report.csv", "text/csv")
        except Exception as exc:
            st.error(f"Prediction failed. Check model and feature schema. Details: {exc}")

elif page == "Bulk predictions":
    st.subheader("Bulk prediction workspace")
    st.write("Upload a CSV or Excel file containing one row per customer and all 23 model input features.")
    st.caption("Accepted column names: x1...x23 or the original dataset names (LIMIT_BAL, SEX, ..., PAY_AMT6). Do not include the target column as a model input.")
    template = pd.DataFrame(columns=FEATURE_ORDER)
    st.download_button("Download empty CSV template", template.to_csv(index=False).encode("utf-8"), "credit_default_input_template.csv", "text/csv")
    uploaded = st.file_uploader("Upload customer data", type=["csv", "xlsx"])
    if uploaded is not None:
        try:
            if uploaded.name.lower().endswith(".xlsx"):
                raw = pd.read_excel(uploaded)
            else:
                raw = pd.read_csv(uploaded)
            st.write(f"Uploaded **{len(raw):,}** rows and **{len(raw.columns)}** columns.")
            st.dataframe(raw.head(20), use_container_width=True)
            if len(raw) > 100_000:
                st.error("This demo limits one upload to 100,000 rows. Split the file into smaller batches.")
            elif st.button("Validate and predict", type="primary"):
                valid, errors = validate_rows(raw)
                st.write(f"Valid rows: **{len(valid):,}** · Invalid rows: **{len(errors):,}**")
                if len(valid):
                    chunks = []
                    batch_size = 5_000
                    progress = st.progress(0.0, text="Predicting in batches...")
                    for start in range(0, len(valid), batch_size):
                        batch = valid.iloc[start:start + batch_size]
                        probs = model.predict_proba(batch[FEATURE_ORDER])[:, 1]
                        out = batch.copy()
                        out["default_probability"] = probs
                        out["decision_threshold"] = threshold
                        out["predicted_class"] = (probs >= threshold).astype(int)
                        out["classification"] = np.where(out["predicted_class"] == 1, "Higher default risk", "Lower default risk")
                        chunks.append(out)
                        progress.progress(min((start + len(batch)) / len(valid), 1.0), text=f"Processed {min(start + len(batch), len(valid)):,} of {len(valid):,} rows")
                    result = pd.concat(chunks, ignore_index=True)
                    st.success("Batch prediction completed.")
                    a, b, c = st.columns(3)
                    a.metric("Predictions generated", f"{len(result):,}")
                    b.metric("Classified higher risk", f"{int((result['predicted_class'] == 1).sum()):,}")
                    c.metric("Classified lower risk", f"{int((result['predicted_class'] == 0).sum()):,}")
                    st.dataframe(result.head(100), use_container_width=True)
                    st.download_button("Download predictions (CSV)", result.to_csv(index=False).encode("utf-8"), "credit_default_predictions.csv", "text/csv")
                if len(errors):
                    st.warning("Some rows were not predicted. Review the validation report.")
                    st.dataframe(errors, use_container_width=True)
                    st.download_button("Download validation errors (CSV)", errors.to_csv(index=False).encode("utf-8"), "validation_errors.csv", "text/csv")
        except Exception as exc:
            st.error(f"Could not read or validate this file: {exc}")

else:
    st.subheader("Model information")
    c1, c2, c3 = st.columns(3)
    c1.metric("Model version", metadata.get("model_version", "Not specified"))
    c2.metric("Features", len(metadata.get("feature_names", [])))
    c3.metric("Saved threshold", f"{threshold:.2%}")
    st.write("**Target:** `default_payment_next_month` · **Positive class:** `1` (default payment next month).")
    st.warning("This interface does not establish model calibration, fairness, or fitness for production lending. Evaluate the model on representative, held-out data before any consequential use.")
    rows = []
    for key in FEATURE_ORDER:
        item = feature_info(key)
        rows.append({
            "Model column": key,
            "Input field": item.get("label", key),
            "Section": item.get("section", "Other"),
            "Type": item.get("kind", "numeric"),
            "Training min": item.get("min"),
            "Training max": item.get("max"),
            "Categories": ", ".join(map(str, item.get("categories", []))) if item.get("categories") else "—",
            "Meaning": item.get("description", ""),
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

st.divider()
st.caption("Credit Default Intelligence · Educational ML demo · Probability estimates are model outputs, not guarantees.")
