import streamlit as st
import pandas as pd
import joblib
import base64
import mysql.connector
from datetime import datetime

# --- DATABASE CONNECTION ---
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="dibyangna21@",
        database="customer_churn"
    )

# --- PAGE CONFIG ---
st.set_page_config(page_title="Customer Churn Prediction", layout="wide")

# --- FUNCTION: CONVERT LOCAL IMAGE TO BASE64 ---
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    return encoded

# --- LOAD LOCAL LOGO ---
logo_path = "netnova-logo.png"
try:
    logo_base64 = get_base64_image(logo_path)
    logo_html = f"""
        <style>
            [data-testid="stAppViewContainer"] {{
                padding-top: 80px;
            }}
            .fixed-logo {{
                position: fixed;
                top: 10px;
                left: 20px;
                z-index: 1000;
                background-color: rgba(255, 255, 255, 0.6);
                border-radius: 12px;
                padding: 6px 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.15);
            }}
        </style>
        <div class="fixed-logo">
            <img src="data:image/png;base64,{logo_base64}" width="120">
        </div>
    """
    st.markdown(logo_html, unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("Logo file not found. Please make sure 'netnova-logo.png' is in the same folder as app.py")

# --- LOAD MODEL ---
try:
    model = joblib.load("model.pkl")
except FileNotFoundError:
    st.error("'model.pkl' not found. Please place it in the same folder as this script.")
    st.stop()

# --- CUSTOM CSS ---
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://img.freepik.com/premium-vector/antenna-transmission-communication-tower-background_115579-760.jpg?semt=ais_hybrid&w=740&q=80");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    position: relative;
}

[data-testid="stAppViewContainer"]::before {
    content: "";
    position: absolute;
    inset: 0;
    background: rgba(255, 255, 255, 0.3);
    z-index: 0;
}

[data-testid="stAppViewContainer"] > * { position: relative; z-index: 1; }

[data-testid="stHeader"] { background: rgba(0,0,0,0); }
[data-testid="stToolbar"] { right: 2rem; }
[data-testid="stDecoration"] { display: none !important; }

.title-text {
    color: #ffffff;
    font-size: 3rem;
    font-weight: 800;
    margin-top: 5rem;
    margin-bottom: 1rem;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
}

.subtitle {
    color: #222;
    font-size: 1.1rem;
    width: 85%;
    line-height: 1.6;
}

.form-box {
    background: rgba(255, 255, 255, 0.97);
    padding: 2rem 2.5rem;
    border-radius: 20px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.3);
}

.stButton>button {
    background: linear-gradient(to right, #ff6a00, #ee0979);
    color: white !important;
    border: none;
    padding: 0.6rem 1.2rem;
    border-radius: 10px;
    font-size: 1rem;
    cursor: pointer;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# --- SESSION STATE ---
if "step" not in st.session_state:
    st.session_state.step = 0

# --- PAGE CONTENT ---
if st.session_state.step == 0:

    st.markdown("<div class='title-text'> Hello Admin!</div>", unsafe_allow_html=True)

    st.markdown(
        "<div class='subtitle'>Welcome to <b>NetNova's Customer Churn Prediction Model</b>.<br><br>"
        "Let's predict which customers are likely to stay and which might churn.</div>",
        unsafe_allow_html=True,
    )

    if st.button("Let's Go ", use_container_width=True):
        st.session_state.step = 1
        st.rerun()

elif st.session_state.step >= 1:

    left_col, right_col = st.columns([1.3, 1])

    with left_col:
        st.markdown("<div class='title-text'>Welcome to Customer Churn Prediction</div>", unsafe_allow_html=True)

        st.markdown(
            "<div class='subtitle'>Predicting churn helps businesses retain their most valuable asset — their customers.</div>",
            unsafe_allow_html=True,
        )

    with right_col:

        st.markdown("<div class='form-box'>", unsafe_allow_html=True)
        st.subheader("Enter Customer Details")

        # STEP 1
        if st.session_state.step == 1:

            customer_name = st.text_input("Customer Name")
            gender = st.selectbox("Gender", ["Select", "Male", "Female"])
            senior_citizen = st.selectbox("Senior Citizen", ["Select", "No", "Yes"])
            partner = st.selectbox("Partner", ["Select", "No", "Yes"])
            dependents = st.selectbox("Dependents", ["Select", "No", "Yes"])

            if st.button("Next", use_container_width=True):

                if "Select" in [gender, senior_citizen, partner, dependents]:
                    st.warning("Please fill all fields before continuing.")

                else:
                    st.session_state.customer_name = customer_name
                    st.session_state.gender = gender
                    st.session_state.senior_citizen = senior_citizen
                    st.session_state.partner = partner
                    st.session_state.dependents = dependents
                    st.session_state.step = 2
                    st.rerun()

        # STEP 2
        elif st.session_state.step == 2:

            tenure = st.slider("Tenure (months)", 0, 72, 12)
            monthly_charges = st.number_input("Monthly Charges", min_value=0.0, step=1.0)
            total_charges = st.number_input("Total Charges", min_value=0.0, step=1.0)

            contract = st.selectbox("Contract Type", ["Select", "Month-to-month", "One year", "Two year"])

            paperless_billing = st.selectbox("Paperless Billing", ["Select", "No", "Yes"])

            payment_method = st.selectbox(
                "Payment Method",
                [
                    "Select",
                    "Electronic check",
                    "Mailed check",
                    "Bank transfer (automatic)",
                    "Credit card (automatic)"
                ]
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button(" Back", use_container_width=True):
                    st.session_state.step = 1
                    st.rerun()

            with col2:

                if st.button("Predict Churn", use_container_width=True):

                    if (
                        tenure == 0 or monthly_charges == 0 or total_charges == 0
                        or "Select" in [contract, paperless_billing, payment_method]
                    ):
                        st.warning(" Please fill in all fields before predicting.")

                    else:

                        input_data = pd.DataFrame({
                            'gender_Male': [1 if st.session_state.gender == "Male" else 0],
                            'SeniorCitizen': [1 if st.session_state.senior_citizen == "Yes" else 0],
                            'Partner_Yes': [1 if st.session_state.partner == "Yes" else 0],
                            'Dependents_Yes': [1 if st.session_state.dependents == "Yes" else 0],
                            'tenure': [tenure],
                            'MonthlyCharges': [monthly_charges],
                            'TotalCharges': [total_charges],
                            'Contract_One year': [1 if contract == "One year" else 0],
                            'Contract_Two year': [1 if contract == "Two year" else 0],
                            'PaperlessBilling_Yes': [1 if paperless_billing == "Yes" else 0],
                            'PaymentMethod_Credit card (automatic)': [1 if payment_method == "Credit card (automatic)" else 0],
                            'PaymentMethod_Electronic check': [1 if payment_method == "Electronic check" else 0],
                            'PaymentMethod_Mailed check': [1 if payment_method == "Mailed check" else 0]
                        })

                        for col in model.feature_names_in_:
                            if col not in input_data.columns:
                                input_data[col] = 0

                        input_data = input_data[model.feature_names_in_]

                        prediction = int(model.predict(input_data)[0])
                        proba = float(model.predict_proba(input_data)[0][prediction])

                        if prediction == 1:
                            st.error(f"This customer is **likely to churn** ({proba*100:.2f}% confidence).")
                        else:
                            st.success(f"This customer is **not likely to churn** ({proba*100:.2f}% confidence).")

                        probabilities = model.predict_proba(input_data)[0]

                        prob_df = pd.DataFrame({
                            "Outcome": ["Not Churn", "Churn"],
                            "Probability": probabilities
                        })

                        st.bar_chart(prob_df.set_index("Outcome"))

                        try:
                            conn = get_db_connection()
                            cursor = conn.cursor()

                            pred_text = "Likely to Churn" if prediction == 1 else "Not Likely to Churn"

                            cursor.execute("""
                                INSERT INTO churn_customers
                                (customer_name, gender, senior_citizen, partner, dependents,
                                tenure, monthly_charges, total_charges, contract,
                                paperless_billing, payment_method, prediction)
                                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                            """, (
                                st.session_state.customer_name,
                                st.session_state.gender,
                                st.session_state.senior_citizen,
                                st.session_state.partner,
                                st.session_state.dependents,
                                tenure,
                                monthly_charges,
                                total_charges,
                                contract,
                                paperless_billing,
                                payment_method,
                                pred_text
                            ))

                            conn.commit()
                            cursor.close()
                            conn.close()

                            st.success("Prediction saved to database successfully!")

                        except Exception as e:
                            st.error(f"Database Error: {e}")

        st.markdown("</div>", unsafe_allow_html=True)

# ADMIN PANEL
st.sidebar.markdown("### Admin Panel")

if st.sidebar.button("View Saved Predictions"):

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM churn_customers ORDER BY id DESC")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        if rows:
            history_df = pd.DataFrame(rows)
            st.subheader("Saved Predictions")
            st.dataframe(history_df)
        else:
            st.info("No prediction records found.")

    except Exception as e:
        st.error(f"Database Error: {e}")

if 'history_df' in locals():

    csv = history_df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="Download Prediction Data",
        data=csv,
        file_name="churn_predictions.csv",
        mime="text/csv"
    )