from __future__ import annotations

import base64
from pathlib import Path

import streamlit as st
from PIL import Image

ROOT = Path(__file__).resolve().parent
LOGO_PATH = ROOT / "assets" / "a-logo.png"

st.set_page_config(
    page_title="Transaction Fraud Lab",
    page_icon=Image.open(LOGO_PATH),
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp { background:linear-gradient(180deg,#fff 0,#fff7f8 48%,#fff 100%); }
    .block-container { max-width:1200px; padding-top:1.5rem; padding-bottom:4rem; }
    .brand-hero { display:flex; gap:1.25rem; align-items:center; padding:1.7rem 1.85rem; border-radius:22px;
      background:linear-gradient(125deg,#4c0519,#9f1239 50%,#e11d48); color:white; box-shadow:0 18px 45px rgba(136,19,55,.22); }
    .brand-hero img { width:78px; height:78px; object-fit:contain; border-radius:18px; background:white; padding:7px; }
    .brand-hero h1 { color:white; margin:0; font-size:clamp(1.8rem,4vw,2.65rem); }
    .brand-hero p { color:#ffe4e6; margin:.5rem 0 0; max-width:760px; }
    .eyebrow { color:#fecdd3; text-transform:uppercase; letter-spacing:.16em; font-size:.75rem; font-weight:800; }
    div[data-testid="stMetric"], div[data-testid="stForm"] { background:white; border:1px solid #fecdd3; border-radius:16px; padding:1rem; }
    button[kind="primary"] { background:#be123c !important; border-color:#be123c !important; border-radius:999px !important; }
    [data-testid="stSidebar"] { background:#fff7f8; border-right:1px solid #fecdd3; }
    </style>
    """,
    unsafe_allow_html=True,
)

logo = "data:image/png;base64," + base64.b64encode(LOGO_PATH.read_bytes()).decode("ascii")
st.markdown(
    f"""<section class="brand-hero"><img src="{logo}" alt="A brand logo"><div>
    <div class="eyebrow">Decision Tree · Planning workspace</div><h1>Transaction Fraud Lab</h1>
    <p>Design a clear, leakage-aware fraud-classification experiment before training the first model.</p></div></section>""",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.image(LOGO_PATH, width=74)
    st.markdown("### Fraud Lab")
    page = st.radio("Choose a workspace", ["Scenario builder", "Implementation plan", "Safety notes"])
    st.divider()
    st.info("Planning stage: no trained model or prediction is included yet.")

if page == "Scenario builder":
    st.subheader("Describe a synthetic transaction")
    st.caption("These controls help define a future dataset. They do not produce a fraud verdict.")
    with st.form("scenario"):
        c1, c2, c3 = st.columns(3)
        with c1:
            channel = st.selectbox("Payment channel", ["Card present", "Online checkout", "Mobile wallet", "Bank transfer"])
            amount_band = st.selectbox("Transaction amount", ["Under ₹1,000", "₹1,000–₹10,000", "₹10,001–₹50,000", "Over ₹50,000"])
        with c2:
            location = st.selectbox("Location pattern", ["Usual location", "New domestic location", "International location"])
            device = st.selectbox("Device familiarity", ["Known device", "Recently seen device", "New device"])
        with c3:
            velocity = st.selectbox("Recent activity", ["Normal frequency", "Several transactions", "Unusually rapid transactions"])
            authentication = st.selectbox("Authentication", ["Strong authentication passed", "Standard authentication", "Authentication failed"])
        submitted = st.form_submit_button("Review scenario design", type="primary", use_container_width=True)
    if submitted:
        st.success("Scenario captured for the future synthetic-data specification.")
        a, b, c = st.columns(3)
        a.metric("Channel", channel)
        b.metric("Device", device)
        c.metric("Activity", velocity)
        st.warning("No prediction was made. A real model must be trained, evaluated and documented before this app can display a score.")
        with st.expander("Scenario details", expanded=True):
            st.write({"amount_band": amount_band, "location_pattern": location, "authentication": authentication})

elif page == "Implementation plan":
    st.subheader("Path to a verified demonstration")
    steps = [
        ("1", "Generate synthetic data", "Use a deterministic seed and document every rule."),
        ("2", "Prevent leakage", "Exclude post-outcome fields and anything derived from the target."),
        ("3", "Create a baseline", "Compare the tree with a simple majority-class strategy."),
        ("4", "Evaluate trade-offs", "Report precision, recall, F1, PR-AUC and confusion matrix."),
        ("5", "Package and test", "Save the full pipeline and verify loading with unseen categories."),
    ]
    for number, title, detail in steps:
        with st.container(border=True):
            st.markdown(f"### {number}. {title}")
            st.write(detail)
    st.progress(0.2, text="Planning notebook and UI shell completed")

else:
    st.subheader("Safety and interpretation")
    st.error("Never describe a synthetic-data score as proof of fraud.")
    st.markdown("""
    - Fraud labels can reflect investigation practices and reporting bias.
    - False positives can harm legitimate customers; false negatives can miss harmful activity.
    - Any real workflow requires governance, human review, privacy safeguards and ongoing monitoring.
    - The current project contains no trained model, validated metrics or production deployment.
    """)

st.caption("Built with Streamlit · Crimson A brand system · Planning-only educational interface")
