from pathlib import Path
import json
import numpy as np
import pandas as pd
import streamlit as st
import joblib
import sklearn

ROOT = Path(__file__).resolve().parent
ARTIFACT_DIR = ROOT / "artifacts"
MODEL_PATH = ARTIFACT_DIR / "insurance_fraud_pipeline.joblib"
THRESHOLD_PATH = ARTIFACT_DIR / "decision_threshold.joblib"
METADATA_PATH = ARTIFACT_DIR / "model_metadata.json"

st.set_page_config(page_title="Insurance Fraud Detection", page_icon="🛡️", layout="wide")
st.title("🛡️ Insurance Fraud Detection")
st.caption("Logistic Regression · Educational demonstration")

st.warning(
    "Educational use only. This model predicts a historical label, not proven fraud. "
    "Do not use it to deny claims, determine premiums, or make automated decisions about people."
)

@st.cache_resource
def load_artifacts():
    missing = [p.name for p in (MODEL_PATH, THRESHOLD_PATH, METADATA_PATH) if not p.exists()]
    if missing:
        raise FileNotFoundError(
            "Missing artifacts: " + ", ".join(missing) +
            ". Run the notebook through the artifact-saving section first."
        )
    model = joblib.load(MODEL_PATH)  # Only load artifacts from a trusted project source.
    threshold = float(joblib.load(THRESHOLD_PATH))
    metadata = json.loads(METADATA_PATH.read_text())
    return model, threshold, metadata

try:
    model, default_threshold, metadata = load_artifacts()
except Exception as exc:
    st.error(f"The prediction service could not start: {exc}")
    st.info("Run insurance_logistic_regression.ipynb and place its artifacts in the artifacts/ folder.")
    st.stop()

if metadata.get("sklearn_version") != sklearn.__version__:
    st.error(
        f"Version mismatch: model trained with scikit-learn {metadata.get('sklearn_version')}, "
        f"app has {sklearn.__version__}. Install the matching requirements and retrain if needed."
    )
    st.stop()

with st.sidebar:
    st.header("Model information")
    st.write("**Algorithm:** Logistic Regression")
    st.write(f"**Training scikit-learn:** {metadata.get('sklearn_version')}")
    st.write(f"**Dataset rows:** training source snapshot SHA-256 `{metadata.get('dataset_sha256', '')[:12]}…`")
    threshold = st.slider("Classification threshold", 0.05, 0.95, float(default_threshold), 0.05)
    st.caption("Changing the threshold changes the class label, not the predicted probability.")

tab_predict, tab_batch, tab_metrics, tab_about = st.tabs(
    ["Single prediction", "Batch CSV", "Model evaluation", "About & limitations"]
)

feature_columns = metadata["feature_columns"]
numeric_features = metadata.get("numeric_features", [])
categorical_features = metadata.get("categorical_features", [])

def validate_frame(frame):
    missing = [c for c in feature_columns if c not in frame.columns]
    extra = [c for c in frame.columns if c not in feature_columns]
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(missing))
    if extra:
        st.info("Extra columns will be ignored: " + ", ".join(extra[:20]))
    clean = frame[feature_columns].copy()
    for col in numeric_features:
        clean[col] = pd.to_numeric(clean[col], errors="coerce")
    if clean[numeric_features].isna().all(axis=None) if numeric_features else False:
        raise ValueError("All numeric inputs are missing or invalid.")
    return clean

with tab_predict:
    st.subheader("Enter claim attributes")
    st.write("Fields reflect the dataset schema. The app starts with a representative row; edit values before prediction.")
    # Initialize defaults from a blank typed row; categorical values use a known source category if available.
    default_row = {}
    for col in feature_columns:
        if col in numeric_features:
            default_row[col] = 0.0
        else:
            default_row[col] = ""
    with st.form("single_prediction_form"):
        edited = {}
        cols = st.columns(2)
        for i, col in enumerate(feature_columns):
            with cols[i % 2]:
                if col in numeric_features:
                    edited[col] = st.number_input(col, value=float(default_row[col]), key=f"single_{col}")
                else:
                    edited[col] = st.text_input(col, value="", key=f"single_{col}")
        submitted = st.form_submit_button("Predict probability")
    if submitted:
        try:
            row = pd.DataFrame([edited])
            row = validate_frame(row)
            # Empty categorical values are treated as missing; the fitted imputer handles them.
            for col in categorical_features:
                row[col] = row[col].replace("", np.nan)
            probability = float(model.predict_proba(row)[0, 1])
            prediction = int(probability >= threshold)
            c1, c2 = st.columns(2)
            c1.metric("Probability of reported fraud label", f"{probability:.1%}")
            c2.metric("Threshold-based class", "Reported fraud (1)" if prediction else "Not reported fraud (0)")
            st.progress(min(max(probability, 0.0), 1.0))
            st.caption("This score is a model estimate for the dataset label, not a finding of actual fraud.")
        except Exception as exc:
            st.error(f"Input validation/prediction failed: {exc}")

with tab_batch:
    st.subheader("Score a CSV file")
    st.write("Upload a CSV containing the model's expected feature columns. The app validates required columns.")
    uploaded = st.file_uploader("Choose CSV", type=["csv"])
    if uploaded:
        try:
            batch = pd.read_csv(uploaded)
            st.write(f"Uploaded rows: {len(batch):,}")
            if len(batch) > 10000:
                st.error("Maximum 10,000 rows per upload for this demo.")
            else:
                clean = validate_frame(batch)
                for col in categorical_features:
                    clean[col] = clean[col].replace("", np.nan)
                probabilities = model.predict_proba(clean)[:, 1]
                scored = batch.copy()
                scored["predicted_probability_reported_fraud"] = probabilities
                scored["predicted_class"] = (probabilities >= threshold).astype(int)
                st.dataframe(scored.head(100), use_container_width=True)
                st.download_button(
                    "Download scored CSV",
                    scored.to_csv(index=False).encode("utf-8"),
                    file_name="insurance_fraud_predictions.csv",
                    mime="text/csv"
                )
                fig, ax = __import__("matplotlib.pyplot", fromlist=["pyplot"]).subplots()
                ax.hist(probabilities, bins=20)
                ax.set_title("Predicted probability distribution")
                ax.set_xlabel("Probability")
                ax.set_ylabel("Claims")
                st.pyplot(fig)
        except Exception as exc:
            st.error(f"Could not score uploaded CSV: {exc}")

with tab_metrics:
    st.subheader("Held-out test metrics")
    metrics = metadata.get("metrics_test", {})
    if metrics:
        cols = st.columns(min(3, len(metrics)))
        for i, (name, value) in enumerate(metrics.items()):
            cols[i % len(cols)].metric(name.replace("_", " ").title(), f"{value:.3f}")
        st.caption("Metrics are from the notebook's held-out test set at the saved threshold. They are not independently validated production performance.")
    st.info("Confusion matrix and ROC/precision-recall graphs are generated in the training notebook. This app does not fabricate or reconstruct those curves from summary metrics.")

with tab_about:
    st.subheader("Dataset and limitations")
    st.markdown(f"""
    - **Dataset record:** [Mendeley Data](https://data.mendeley.com/datasets/992mh7dk9y/2)
    - **CSV source:** [GitHub dataset](https://github.com/mwitiderrick/insurancedata/blob/master/insurance_claims.csv)
    - **License reported by source:** CC BY 4.0; verify the record and provide attribution before redistribution.
    - **Target:** `{metadata.get('target_column')}`
    - **Positive class:** {metadata.get('positive_class_label')}
    - **Random seed:** {metadata.get('random_state')}
    - **Test size:** {metadata.get('test_size')}
    """)
    st.markdown("""
    **Important limitations**
    - Historical labels may reflect investigation processes, not independently confirmed fraud.
    - Some columns may be post-event or post-investigation. Conduct a documented leakage review before using this model for any prospective task.
    - Dataset provenance and representativeness may be limited; this is not validated for real insurance operations.
    - Do not use this demo to deny claims, change premiums, or make consequential decisions about individuals.
    """)
