# import streamlit as st
# import pandas as pd
# import joblib
# import numpy as np
# import matplotlib.pyplot as plt
# from utils.auth import get_current_user

# # Load model artifacts
# model = joblib.load("./backend/model/credit_model.pkl")
# scaler = joblib.load("./backend/model/scaler.pkl")
# feature_columns = joblib.load("./backend/model/columns.pkl")

# def show_home():
#     if not st.session_state.get("logged_in"):
#         st.warning("You must login first.")
#         st.session_state["page"] = "login"
#         st.stop()
#         return

#     user = get_current_user()

#     # Sidebar navigation
#     st.sidebar.title("📂 Navigation")
#     section = st.sidebar.radio("Select", ["👤 Profile", "📊 Eligibility"])
#     if st.sidebar.button("Logout"):
#         st.session_state.clear()
#         st.session_state["page"] = "login"
#         st.stop()

#     verified = st.session_state.get("verified", False)
#     badge = "🟢" if verified else "⚪"

#     # Welcome card
#     st.markdown(f"""
#         <style>
#             .welcome-card {{
#                 background-color: #1e1e1e;
#                 padding: 2rem;
#                 border-radius: 16px;
#                 box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
#                 max-width: 400px;
#                 margin: 2rem auto;
#                 text-align: center;
#                 color: white;
#             }}
#         </style>

#         <div class="welcome-card">
#             <h2>Welcome {user['name']} {badge}</h2>
#             <p>Age: {user['age']}</p>
#         </div>
#     """, unsafe_allow_html=True)

#     if section == "👤 Profile":
#         show_profile_section()
#     elif section == "📊 Eligibility":
#         show_eligibility_section()


# def show_profile_section():
#     st.subheader("👤 Profile Verification")

#     aadhaar = st.file_uploader("📄 Upload Aadhaar (PDF)", type="pdf")
#     pan = st.file_uploader("📄 Upload PAN Card (PDF)", type="pdf")

#     if "verified" not in st.session_state:
#         st.session_state["verified"] = False

#     if st.button("✅ Validate"):
#         if aadhaar and pan:
#             st.session_state["verified"] = True
#             st.success("Documents verified ✅")
#         else:
#             st.error("Please upload both Aadhaar and PAN card.")

#     badge = "🟢 Verified" if st.session_state["verified"] else "⚪ Not Verified"
#     st.info(f"Verification Status: {badge}")


# def show_eligibility_section():
#     st.subheader("📋 Credit Eligibility Form")

#     employment_type = st.selectbox("Employment Type", ["Farmer", "Salaried", "Business"])
#     income = st.number_input("Monthly Income (INR)", step=1000)
#     expenses = st.number_input("Monthly Expenses (INR)", step=1000)
#     transactions = st.number_input("Mobile Transactions (INR)", step=1000)
#     dti = st.slider("Debt-to-Income Ratio (%)", 0, 100, 30)
#     emp_length = st.slider("Employment Length (years)", 0, 40, 5)
#     credit_score = st.slider("Credit Score", 300, 900, 650)
#     loan_amount_outstanding = st.number_input("Existing Loan Amount (INR)", min_value=0)
#     existing_loans = st.slider("Number of Existing Loans", 0, 10, 0)
#     has_guarantor = st.checkbox("Has Guarantor?")
#     owns_land = st.checkbox("Owns Land?")
#     land_size = st.slider("Land Size (acres)", 0.0, 20.0, 0.0)
#     location = st.selectbox("Location Type", ["Urban", "Semi-Urban", "Rural"])
#     income_doc_type = st.selectbox("Income Proof Type", ["Bank Statement", "Payslip", "ITR", "None"])
#     purpose = st.selectbox("Loan Purpose", [
#         "credit_card", "debt_consolidation", "home_improvement", "house",
#         "major_purchase", "medical", "moving", "other", "renewable_energy",
#         "small_business", "vacation"
#     ])

#     if st.button("🔍 Predict Eligibility"):
#         input_data = {
#             'income': income,
#             'expenses': expenses,
#             'transactions': transactions,
#             'dti': dti,
#             'emp_length': emp_length,
#             'credit_score': credit_score,
#             'loan_amount_outstanding': loan_amount_outstanding,
#             'existing_loans': existing_loans,
#             'has_guarantor': int(has_guarantor),
#             'owns_land': int(owns_land),
#             'land_size': land_size,
#             f"employment_type_{employment_type}": 1,
#             f"income_doc_type_{income_doc_type}": 1,
#             f"location_{location}": 1,
#             f"purpose_{purpose}": 1
#         }

#         # Fill missing dummy features
#         for col in feature_columns:
#             if col not in input_data:
#                 input_data[col] = 0

#         df = pd.DataFrame([input_data])
#         numeric_cols = ['income', 'expenses', 'transactions', 'dti', 'emp_length',
#                         'credit_score', 'loan_amount_outstanding', 'existing_loans', 'land_size']
#         df[numeric_cols] = scaler.transform(df[numeric_cols])
#         df = df[feature_columns]

#         prediction = model.predict(df)[0]
#         st.session_state["show_popup"] = True
#         st.session_state["eligibility_result"] = prediction
#         st.session_state["df_input"] = df

#     if st.session_state.get("show_popup"):
#         prediction = st.session_state["eligibility_result"]
#         df = st.session_state["df_input"]

#         with st.expander("📊 Prediction Result", expanded=True):
#             if prediction == 1:
#                 st.success("✅ You are Eligible for Credit!")

#                 tabs = st.tabs(["📈 Prediction", "📊 Graph Explanation", "⛓️ Smart Contract"])

#                 with tabs[0]:
#                     proba = model.predict_proba(df)[0][1]
#                     user_credit_score = int(300 + proba * 600)  # scale 0–1 to 300–900
#                     st.info(f"Credit Score: {user_credit_score} \nLoan Approved ✅")

#                 with tabs[1]:
#                     st.markdown("### 🔍 Top Contributing Features (User-Based)")
#                     global_importance = model.feature_importances_
#                     feature_means = scaler.transform([np.zeros(len(feature_columns))])[0]

#                     contributions = (df.values[0] - feature_means) * global_importance
#                     top_idx = np.argsort(np.abs(contributions))[::-1][:5]
#                     top_feats = [feature_columns[i] for i in top_idx]
#                     top_vals = [contributions[i] for i in top_idx]

#                     fig, ax = plt.subplots()
#                     ax.barh(top_feats[::-1], top_vals[::-1], color='green')
#                     ax.set_xlabel("Estimated Impact")
#                     ax.set_title("Top Feature Contributions (You)")
#                     st.pyplot(fig)

#                 with tabs[2]:
#                     if not st.session_state.get("verified"):
#                         st.error("Profile not verified. Please complete verification.")
#                     else:
#                         st.success("Smart contract simulated ✅ TxHash: `0xabc123...`")
#             else:
#                 st.error("❌ Loan Rejected")

#                 reasons = []
#                 if income < 10000:
#                     reasons.append("Low monthly income")
#                 if dti > 35:
#                     reasons.append("High debt-to-income ratio")
#                 if credit_score < 600:
#                     reasons.append("Low credit score")
#                 if not has_guarantor:
#                     reasons.append("No guarantor provided")
#                 if existing_loans >= 3:
#                     reasons.append("Too many existing loans")
#                 if income_doc_type == "None":
#                     reasons.append("No income documentation")
#                 if employment_type == "Farmer" and not owns_land:
#                     reasons.append("Farmer without land ownership")

#                 st.markdown("### ❗ Rejection Reasons:")
#                 for r in reasons:
#                     st.markdown(f"- {r}")

#         if st.button("❌ Close"):
#             st.session_state["show_popup"] = False

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from utils.auth import get_current_user

# Load artifacts
model = joblib.load("./backend/model/credit_model.pkl")
scaler = joblib.load("./backend/model/scaler.pkl")
feature_columns = joblib.load("./backend/model/columns.pkl")

def show_home():
    if not st.session_state.get("logged_in"):
        st.warning("You must login first.")
        st.session_state["page"] = "login"
        st.stop()
        return

    user = get_current_user()

    st.sidebar.title("📂 Navigation")
    section = st.sidebar.radio("Select", ["👤 Profile", "📊 Eligibility"])
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.session_state["page"] = "login"
        st.stop()

    verified = st.session_state.get("verified", False)
    badge = "🟢" if verified else "⚪"

    st.markdown(f"""
        <style>
            html, body, .stApp {{
                background-color: #0d0d0d !important;
                color: white;
            }}
            .welcome-card {{
                background-color: #1e1e1e;
                padding: 2rem;
                border-radius: 16px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
                max-width: 400px;
                margin: 2rem auto;
                text-align: center;
                color: white;
            }}
        </style>
        <div class="welcome-card">
            <h2>Welcome {user['name']} {badge}</h2>
            <p>Age: {user['age']}</p>
        </div>
    """, unsafe_allow_html=True)

    if section == "👤 Profile":
        show_profile_section()
    elif section == "📊 Eligibility":
        show_eligibility_section()

def show_profile_section():
    st.subheader("👤 Profile Verification")
    aadhaar = st.file_uploader("📄 Upload Aadhaar (PDF)", type="pdf")
    pan = st.file_uploader("📄 Upload PAN Card (PDF)", type="pdf")

    if "verified" not in st.session_state:
        st.session_state["verified"] = False

    if st.button("✅ Validate"):
        if aadhaar and pan:
            st.session_state["verified"] = True
            st.success("Documents verified ✅")
        else:
            st.error("Please upload both Aadhaar and PAN card.")

    badge = "🟢 Verified" if st.session_state["verified"] else "⚪ Not Verified"
    st.info(f"Verification Status: {badge}")

def show_eligibility_section():
    st.subheader("📋 Credit Eligibility Form")

    # Form inputs
    employment_type = st.selectbox("Employment Type", ["Farmer", "Salaried", "Business"])
    income = st.number_input("Monthly Income", step=1000)
    expenses = st.number_input("Monthly Expenses", step=1000)
    transactions = st.number_input("Mobile Transactions", step=1000)
    dti = st.slider("Debt-to-Income Ratio (%)", 0, 100, 30)
    emp_length = st.slider("Employment Length (years)", 0, 40, 5)
    credit_score = st.slider("Credit Score", 300, 900, 650)
    loan_amount_outstanding = st.number_input("Existing Loan Amount", step=1000)
    existing_loans = st.slider("Existing Loans", 0, 10, 0)
    has_guarantor = st.checkbox("Has Guarantor?")
    owns_land = st.checkbox("Owns Land?")
    land_size = st.slider("Land Size (acres)", 0.0, 20.0, 0.0)
    location = st.selectbox("Location", ["Urban", "Semi-Urban", "Rural"])
    income_doc_type = st.selectbox("Income Proof Type", ["Bank Statement", "Payslip", "ITR", "None"])
    purpose = st.selectbox("Loan Purpose", [
        "credit_card", "debt_consolidation", "home_improvement", "house",
        "major_purchase", "medical", "moving", "other", "renewable_energy",
        "small_business", "vacation"
    ])

    if st.button("🔍 Predict Eligibility"):
        input_data = {
            'income': income,
            'expenses': expenses,
            'transactions': transactions,
            'dti': dti,
            'emp_length': emp_length,
            'credit_score': credit_score,
            'loan_amount_outstanding': loan_amount_outstanding,
            'existing_loans': existing_loans,
            'has_guarantor': int(has_guarantor),
            'owns_land': int(owns_land),
            'land_size': land_size,
            f"employment_type_{employment_type}": 1,
            f"income_doc_type_{income_doc_type}": 1,
            f"location_{location}": 1,
            f"purpose_{purpose}": 1
        }

        for col in feature_columns:
            if col not in input_data:
                input_data[col] = 0

        df = pd.DataFrame([input_data])
        numeric_cols = ['income', 'expenses', 'transactions', 'dti', 'emp_length',
                        'credit_score', 'loan_amount_outstanding', 'existing_loans', 'land_size']
        df[numeric_cols] = scaler.transform(df[numeric_cols])
        df = df[feature_columns]

        prediction = model.predict(df)[0]
        st.session_state["show_popup"] = True
        st.session_state["prediction_result"] = prediction
        st.session_state["credit_score_user"] = credit_score
        st.session_state["df_input"] = df

    if st.session_state.get("show_popup"):
        prediction = st.session_state["prediction_result"]
        df_input = st.session_state["df_input"]
        credit_score = st.session_state["credit_score_user"]

        with st.expander("📊 Prediction Result", expanded=True):
            if prediction == 1:
                st.success("✅ You are Eligible for Credit!")
            else:
                st.error("❌ Loan Rejected")

            tabs = st.tabs(["📈 Prediction", "📊 Feature Contribution", "⛓️ Smart Contract"])

            with tabs[0]:
                st.info(f"Credit Score: {credit_score} ✅")

            with tabs[1]:
                importances = model.feature_importances_
                top_indices = np.argsort(importances)[-5:]
                top_features = [feature_columns[i] for i in top_indices]
                top_scores = [importances[i] for i in top_indices]

                fig, ax = plt.subplots()
                ax.barh(top_features, top_scores, color='green')
                ax.set_xlabel("Importance")
                ax.set_title("Top Feature Contribution")
                st.pyplot(fig)

            with tabs[2]:
                if not st.session_state.get("verified"):
                    st.error("Profile not verified. Please complete verification.")
                else:
                    st.success("Smart contract simulated. TxHash: 0xabc123...")

        if st.button("❌ Close"):
            st.session_state["show_popup"] = False
