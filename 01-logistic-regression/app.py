

# Import the libraries needed for the web app.
import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

# Find the folder containing this Python file.
APP_DIR = Path(__file__).parent

# Load the trained model pipeline and selected decision threshold.
model = joblib.load(APP_DIR / "logistic_regression_pipeline.joblib")
threshold = float(joblib.load(APP_DIR / "decision_threshold.joblib"))

# Configure the browser tab and page layout.
st.set_page_config(
    page_title="Logistic Regression",
    page_icon="📊",
    layout="wide"
)

# Display the app title and explain its purpose.
st.title("📊 Logistic Regression: Credit Default")
st.write(
    "Enter customer information to estimate the probability "
    "of credit card default next month."
)

# Explain the model's probability and decision threshold.
st.info(
    f"The saved model uses a decision threshold of {threshold:.2f}. "
    "This is an educational demonstration, not a real lending tool."
)

# Collect the customer's input features.
with st.form("customer_form"):
    st.subheader("Customer Information")

    col1, col2 = st.columns(2)

    # Collect numerical and categorical inputs.
    with col1:
        limit_bal = st.number_input(
            "Credit limit (LIMIT_BAL)",
            min_value=0,
            value=50000,
            step=1000
        )

        age = st.number_input(
            "Age",
            min_value=18,
            max_value=100,
            value=30
        )

        sex = st.selectbox("SEX", [1, 2], index=0)
        education = st.selectbox("EDUCATION", [1, 2, 3, 4], index=1)
        marriage = st.selectbox("MARRIAGE", [1, 2, 3], index=0)

    with col2:
        # Payment status codes represent repayment status.
        pay_options = [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8]

        pay_0 = st.selectbox("PAY_0 (most recent status)", pay_options)
        pay_2 = st.selectbox("PAY_2", pay_options)
        pay_3 = st.selectbox("PAY_3", pay_options)
        pay_4 = st.selectbox("PAY_4", pay_options)
        pay_5 = st.selectbox("PAY_5", pay_options)
        pay_6 = st.selectbox("PAY_6", pay_options)

    st.subheader("Bill Amounts")

    # Collect the six monthly bill amounts.
    bill_amounts = {}
    bill_cols = st.columns(3)

    for i in range(1, 7):
        with bill_cols[(i - 1) % 3]:
            bill_amounts[f"BILL_AMT{i}"] = st.number_input(
                f"BILL_AMT{i}",
                value=0,
                step=1000
            )

    st.subheader("Previous Payments")

    # Collect the six monthly payment amounts.
    payment_amounts = {}
    payment_cols = st.columns(3)

    for i in range(1, 7):
        with payment_cols[(i - 1) % 3]:
            payment_amounts[f"PAY_AMT{i}"] = st.number_input(
                f"PAY_AMT{i}",
                min_value=0,
                value=0,
                step=1000
            )

    # Run the prediction only when the user submits the form.
    submitted = st.form_submit_button("Predict")

# Prepare the inputs and display the prediction.
if submitted:
    # Use the exact feature names expected by the trained pipeline.
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
        **payment_amounts
    }

    # Convert the inputs into a one-row DataFrame.
    # The pipeline handles scaling and categorical encoding.
    input_df = pd.DataFrame([customer])

    # Estimate the probability of default (class 1).
    probability = model.predict_proba(input_df)[0, 1]

    # Apply the saved threshold to convert probability into a class.
    prediction = int(probability >= threshold)

    # Display the probability as a percentage.
    st.metric("Estimated default probability", f"{probability:.1%}")

    # Explain the resulting classification.
    if prediction == 1:
        st.warning("Model classification: Higher default risk")
    else:
        st.success("Model classification: Lower default risk")

    # Clarify that the result is not a guaranteed outcome.
    st.caption(
        "This is a statistical estimate, not a certainty or a "
        "recommendation to approve or reject credit."
    )
