
# ============================================================
# LOGISTIC REGRESSION — CREDIT DEFAULT DEMO
# ============================================================

from pathlib import Path

import joblib
import pandas as pd
import streamlit as st


# ------------------------------------------------------------
# 1. LOAD THE SAVED MODEL
# ------------------------------------------------------------

APP_DIR = Path(__file__).resolve().parent

model = joblib.load(APP_DIR / "logistic_regression_pipeline.joblib")
threshold = float(joblib.load(APP_DIR / "decision_threshold.joblib"))

st.set_page_config(
    page_title="Logistic Regression Lab",
    page_icon="📊",
    layout="wide",
)

# ------------------------------------------------------------
# 2. PAGE HEADER
# ------------------------------------------------------------

st.title("📊 Logistic Regression Lab")
st.subheader("Credit Card Default Prediction")

st.write(
    "Explore how Logistic Regression estimates the probability "
    "of a customer defaulting on a credit-card payment next month."
)

st.info(
    f"Decision threshold: {threshold:.2f}. "
    "This is an educational demonstration, not a lending decision tool."
)

# ------------------------------------------------------------
# 3. HUMAN-READABLE DROPDOWN LABELS
# ------------------------------------------------------------

sex_labels = {
    1: "Male",
    2: "Female",
}

education_labels = {
    1: "Graduate school",
    2: "University",
    3: "High school",
    4: "Other",
    5: "Unknown",
    6: "Unknown",
    0: "Unknown",
}

marriage_labels = {
    1: "Married",
    2: "Single",
    3: "Other",
    0: "Unknown",
}

pay_labels = {
    -2: "No consumption",
    -1: "Paid duly",
    0: "Revolving credit / no delay recorded",
    1: "Payment delayed by 1 month",
    2: "Payment delayed by 2 months",
    3: "Payment delayed by 3 months",
    4: "Payment delayed by 4 months",
    5: "Payment delayed by 5 months",
    6: "Payment delayed by 6 months",
    7: "Payment delayed by 7 months",
    8: "Payment delayed by 8 months",
}

# ------------------------------------------------------------
# 4. INPUT FORM
# ------------------------------------------------------------

with st.form("credit_prediction_form"):

    st.header("Customer details")

    col1, col2 = st.columns(2)

    with col1:
        limit_bal = st.number_input(
            "Credit limit",
            min_value=0,
            value=50000,
            step=1000,
            help="Credit limit in the dataset's currency units.",
        )

        sex = st.selectbox(
            "Sex",
            options=[1, 2],
            format_func=lambda value: sex_labels[value],
        )

        education = st.selectbox(
            "Education",
            options=[1, 2, 3, 4, 5, 6, 0],
            index=1,
            format_func=lambda value: education_labels[value],
        )

        marriage = st.selectbox(
            "Marital status",
            options=[1, 2, 3, 0],
            index=0,
            format_func=lambda value: marriage_labels[value],
        )

        age = st.number_input(
            "Age",
            min_value=18,
            max_value=100,
            value=30,
        )

    with col2:
        st.markdown("**Repayment status**")
        st.caption(
            "Choose the recorded repayment status for each month."
        )

        pay_options = list(pay_labels.keys())

        pay_0 = st.selectbox(
            "Most recent month (PAY_0)",
            pay_options,
            format_func=lambda value: pay_labels[value],
        )

        pay_2 = st.selectbox(
            "Two months ago (PAY_2)",
            pay_options,
            format_func=lambda value: pay_labels[value],
        )

        pay_3 = st.selectbox(
            "Three months ago (PAY_3)",
            pay_options,
            format_func=lambda value: pay_labels[value],
        )

        pay_4 = st.selectbox(
            "Four months ago (PAY_4)",
            pay_options,
            format_func=lambda value: pay_labels[value],
        )

        pay_5 = st.selectbox(
            "Five months ago (PAY_5)",
            pay_options,
            format_func=lambda value: pay_labels[value],
        )

        pay_6 = st.selectbox(
            "Six months ago (PAY_6)",
            pay_options,
            format_func=lambda value: pay_labels[value],
        )

    st.divider()
    st.header("Monthly bill amounts")

    bill_amounts = {}

    bill_cols = st.columns(3)

    for month in range(1, 7):
        with bill_cols[(month - 1) % 3]:
            bill_amounts[f"BILL_AMT{month}"] = st.number_input(
                f"Bill amount — month {month}",
                value=0,
                step=1000,
            )

    st.divider()
    st.header("Monthly payment amounts")

    payment_amounts = {}

    payment_cols = st.columns(3)

    for month in range(1, 7):
        with payment_cols[(month - 1) % 3]:
            payment_amounts[f"PAY_AMT{month}"] = st.number_input(
                f"Payment amount — month {month}",
                min_value=0,
                value=0,
                step=1000,
            )

    submitted = st.form_submit_button(
        "Predict default probability",
        type="primary",
        use_container_width=True,
    )

# ------------------------------------------------------------
# 5. BUILD INPUT USING THE ORIGINAL DATASET COLUMN ORDER
# ------------------------------------------------------------

if submitted:

    # These are the original dataset feature names and order.
    original_feature_names = [
        "LIMIT_BAL",
        "SEX",
        "EDUCATION",
        "MARRIAGE",
        "AGE",
        "PAY_0",
        "PAY_2",
        "PAY_3",
        "PAY_4",
        "PAY_5",
        "PAY_6",
        "BILL_AMT1",
        "BILL_AMT2",
        "BILL_AMT3",
        "BILL_AMT4",
        "BILL_AMT5",
        "BILL_AMT6",
        "PAY_AMT1",
        "PAY_AMT2",
        "PAY_AMT3",
        "PAY_AMT4",
        "PAY_AMT5",
        "PAY_AMT6",
    ]

    customer = {
        "LIMIT_BAL": limit_bal,
        "SEX": sex,
        "EDUCATION": education,
        "MARRIAGE": marriage,
        "AGE": age,
        "PAY_0": pay_0,
        "PAY_2": pay_2,
        "PAY_3": pay_3,
        "PAY_4": pay_4,
        "PAY_5": pay_5,
        "PAY_6": pay_6,
        **bill_amounts,
        **payment_amounts,
    }

    # Start with the descriptive names used in the form.
    input_df = pd.DataFrame(
        [[customer[name] for name in original_feature_names]],
        columns=original_feature_names,
    )

    # The saved notebook model expects x1, x2, ..., x23.
    feature_mapping = {
        name: f"x{index}"
        for index, name in enumerate(original_feature_names, start=1)
    }

    input_df = input_df.rename(columns=feature_mapping)

    # Enforce the exact column order stored by the trained pipeline.
    expected_columns = list(model.feature_names_in_)

    missing_columns = [
        name for name in expected_columns
        if name not in input_df.columns
    ]

    if missing_columns:
        st.error(
            f"Model input mismatch. Missing columns: {missing_columns}"
        )
        st.stop()

    input_df = input_df[expected_columns]

    # --------------------------------------------------------
    # 6. PREDICT
    # --------------------------------------------------------

    try:
        probabilities = model.predict_proba(input_df)[0]

        # Find the probability associated with class 1.
        class_labels = list(model.classes_)
        default_index = class_labels.index(1)
        probability = float(probabilities[default_index])

        # Apply the threshold saved from notebook validation.
        prediction = int(probability >= threshold)

        st.divider()
        st.header("Prediction result")

        result_col1, result_col2 = st.columns(2)

        with result_col1:
            st.metric(
                "Estimated default probability",
                f"{probability:.1%}",
            )

            st.progress(probability)

        with result_col2:
            if prediction == 1:
                st.warning("Classification: Higher default risk")
            else:
                st.success("Classification: Lower default risk")

            st.caption(
                f"Threshold used: {threshold:.2f}"
            )

        with st.expander("View submitted model inputs"):
            st.dataframe(
                pd.DataFrame([customer]),
                use_container_width=True,
            )

        st.caption(
            "Educational estimate only. It is not a guarantee of "
            "future behavior and must not be used as the sole basis "
            "for a real credit decision."
        )

    except Exception as error:
        st.error(
            "Prediction failed. Please inspect the app logs "
            "to identify the model compatibility or input issue."
        )
        st.exception(error)
