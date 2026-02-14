


# import streamlit as st
# import pandas as pd

# from raw_user_input import validate_raw_input
# from LR_input_vector import LRInputVector
# from XGB_input_vector import XGBInputVector
# from LR_PD_predictor import LRPDPredictor
# from XGB_PD_predictor import XGBPDPredictor
# from PD_to_decision_engine import PDDecisionEngine


# st.set_page_config(page_title="Credit Risk PD Engine", layout="wide")
# st.title("📊 Credit Risk PD Engine")
# st.markdown("### Dual Model Evaluation: Logistic Regression & XGBoost")


# # =====================================================
# # LOAD MODELS (CACHED)
# # =====================================================

# @st.cache_resource
# def load_lr():
#     return LRPDPredictor("LR_model.joblib")

# @st.cache_resource
# def load_xgb():
#     return XGBPDPredictor("XGB_model.joblib")

# lr_predictor = load_lr()
# xgb_predictor = load_xgb()
# decision_engine = PDDecisionEngine()


# # =====================================================
# # USER INPUT (SIDEBAR)
# # =====================================================

# with st.sidebar:

#     st.header("🏦 Loan Details")
#     loan_amnt = st.number_input("Loan Amount", min_value=0.0, value=10000.0)
#     term = st.selectbox("Term (Months)", [36, 60])
#     int_rate = st.number_input("Interest Rate (%)", min_value=0.0, max_value=40.0, value=12.0)
#     grade = st.selectbox("Grade", ["A","B","C","D","E","F","G"])
#     sub_grade = st.selectbox("Sub Grade",
#         ["A1","A2","A3","A4","A5",
#          "B1","B2","B3","B4","B5",
#          "C1","C2","C3","C4","C5"]
#     )
#     purpose = st.selectbox("Purpose",
#         ["credit_card","debt_consolidation",
#          "home_improvement","major_purchase",
#          "small_business","other"]
#     )

#     st.divider()

#     st.header("👤 Employment & Income")
#     emp_length = st.number_input("Employment Length (Years)", min_value=0, value=5)
#     annual_inc = st.number_input("Annual Income", min_value=0.0, value=60000.0)
#     verification_status = st.selectbox(
#         "Verification Status",
#         ["Verified","Source Verified","Not Verified"]
#     )

#     st.divider()

#     st.header("🏠 Housing Profile")
#     home_ownership = st.selectbox(
#         "Home Ownership",
#         ["RENT","OWN","MORTGAGE","OTHER"]
#     )
#     mort_acc = st.number_input("Mortgage Accounts", min_value=0, value=1)

#     st.divider()

#     st.header("📊 Credit Score & Age")
#     fico = st.number_input("FICO Score", min_value=300, max_value=900, value=700)
#     credit_age = st.number_input("Credit Age (Months)", min_value=0, value=120)

#     st.divider()

#     st.header("📉 Credit Utilization")
#     revol_util = st.number_input("Revolving Utilization (%)", min_value=0.0, max_value=100.0, value=30.0)
#     bc_util = st.number_input("BC Utilization (%)", min_value=0.0, max_value=100.0, value=40.0)
#     percent_bc_gt_75 = st.number_input("Percent BC > 75%", min_value=0.0, max_value=100.0, value=10.0)
#     revol_bal = st.number_input("Revolving Balance", min_value=0.0, value=5000.0)
#     total_bc_limit = st.number_input("Total BC Limit", min_value=0.0, value=20000.0)
#     avg_cur_bal = st.number_input("Average Current Balance", min_value=0.0, value=10000.0)
#     tot_cur_bal = st.number_input("Total Current Balance", min_value=0.0, value=50000.0)
#     bc_open_to_buy = st.number_input("BC Open To Buy", min_value=0.0, value=10000.0)

#     st.divider()

#     st.header("📈 Credit Behavior")
#     inq_last_6mths = st.number_input("Inquiries Last 6 Months", min_value=0, value=1)
#     acc_open_past_24mths = st.number_input("Accounts Open Past 24 Months", min_value=0, value=2)
#     num_actv_bc_tl = st.number_input("Active BC TL", min_value=0, value=3)
#     num_actv_rev_tl = st.number_input("Active Rev TL", min_value=0, value=4)

#     st.divider()

#     st.header("⏳ Account Vintage")
#     mo_sin_old_rev_tl_op = st.number_input("Months Since Oldest Rev TL", min_value=0, value=120)
#     mo_sin_rcnt_tl = st.number_input("Months Since Recent TL", min_value=0, value=6)
#     mths_since_recent_bc = st.number_input("Months Since Recent BC", min_value=0, value=5)
#     mths_since_recent_inq = st.number_input("Months Since Recent Inquiry", min_value=0, value=2)

#     st.divider()

#     st.header("💰 Risk Ratios")
#     dti = st.number_input("Debt To Income Ratio", min_value=0.0, max_value=100.0, value=15.0)

#     generate_btn = st.button("Generate PD Scores")


# # =====================================================
# # RAW DICTIONARY
# # =====================================================

# raw_input = {
#     "grade": grade,
#     "sub_grade": sub_grade,
#     "term": term,
#     "int_rate": int_rate,
#     "loan_amnt": loan_amnt,
#     "annual_inc": annual_inc,
#     "dti": dti,
#     "fico": fico,
#     "emp_length": emp_length,
#     "mort_acc": mort_acc,
#     "home_ownership": home_ownership,
#     "verification_status": verification_status,
#     "purpose": purpose,
#     "credit_age": credit_age,
#     "revol_util": revol_util,
#     "bc_util": bc_util,
#     "percent_bc_gt_75": percent_bc_gt_75,
#     "acc_open_past_24mths": acc_open_past_24mths,
#     "avg_cur_bal": avg_cur_bal,
#     "tot_cur_bal": tot_cur_bal,
#     "total_bc_limit": total_bc_limit,
#     "revol_bal": revol_bal,
#     "inq_last_6mths": inq_last_6mths,
#     "mths_since_recent_bc": mths_since_recent_bc,
#     "mths_since_recent_inq": mths_since_recent_inq,
#     "mo_sin_old_rev_tl_op": mo_sin_old_rev_tl_op,
#     "mo_sin_rcnt_tl": mo_sin_rcnt_tl,
#     "num_actv_bc_tl": num_actv_bc_tl,
#     "num_actv_rev_tl": num_actv_rev_tl,
#     "bc_open_to_buy": bc_open_to_buy,
# }


# # =====================================================
# # OUTPUT
# # =====================================================

# if generate_btn:

#     try:

#         validated_raw = validate_raw_input(raw_input)

#         lr_vector = LRInputVector().build(validated_raw)
#         xgb_vector = XGBInputVector().build(validated_raw)

#         lr_pd = lr_predictor.predict_pd_percent(lr_vector)
#         xgb_pd = xgb_predictor.predict_pd_percent(xgb_vector)

#         lr_decision_df = decision_engine.evaluate(lr_pd)
#         xgb_decision_df = decision_engine.evaluate(xgb_pd)

#         st.success("PD Calculation Successful")

#         # =============================
#         # LR BOX
#         # =============================
#         st.markdown("## Logistic Regression Predictions")

#         lr_cols = st.columns(4)

#         lr_cols[0].metric("PD (%)", f"{lr_pd:.2f}%")
#         lr_cols[1].metric("Credit Score", int(lr_decision_df["Score"].iloc[0]))
#         lr_cols[2].metric("Rating Band", lr_decision_df["Rating Band"].iloc[0])
#         lr_cols[3].metric("Final Decision", lr_decision_df["Decision"].iloc[0])

#         st.divider()

#         # =============================
#         # XGB BOX
#         # =============================
#         st.markdown("## XGBoost Predictions")

#         xgb_cols = st.columns(4)

#         xgb_cols[0].metric("PD (%)", f"{xgb_pd:.2f}%")
#         xgb_cols[1].metric("Credit Score", int(xgb_decision_df["Score"].iloc[0]))
#         xgb_cols[2].metric("Rating Band", xgb_decision_df["Rating Band"].iloc[0])
#         xgb_cols[3].metric("Final Decision", xgb_decision_df["Decision"].iloc[0])

#     except Exception as e:
#         st.error(f"Validation / Prediction Error: {str(e)}")









# import streamlit as st
# import pandas as pd

# from raw_user_input import validate_raw_input
# from LR_input_vector import LRInputVector
# from XGB_input_vector import XGBInputVector
# from LR_PD_predictor import LRPDPredictor
# from XGB_PD_predictor import XGBPDPredictor
# from pd_to_decision_engine import PDDecisionEngine


# # =====================================================
# # PAGE CONFIG
# # =====================================================

# st.set_page_config(page_title="Credit Risk PD Engine", layout="wide")

# st.title("📊 Credit Risk PD Engine")
# st.markdown("### Dual Model Evaluation: Logistic Regression & XGBoost")


# # =====================================================
# # LOAD MODELS (CACHED)
# # =====================================================

# @st.cache_resource
# def load_lr():
#     return LRPDPredictor("LR_model.joblib")

# @st.cache_resource
# def load_xgb():
#     return XGBPDPredictor("XGB_model.joblib")

# lr_predictor = load_lr()
# xgb_predictor = load_xgb()
# decision_engine = PDDecisionEngine()


# # =====================================================
# # SIDEBAR INPUT
# # =====================================================

# with st.sidebar:

#     st.header("🏦 Loan Details")
#     loan_amnt = st.number_input("Loan Amount", min_value=0.0, value=10000.0)
#     term = st.selectbox("Term (Months)", [36, 60])
#     int_rate = st.number_input("Interest Rate (%)", min_value=0.0, max_value=40.0, value=12.0)
#     grade = st.selectbox("Grade", ["A","B","C","D","E","F","G"])
#     sub_grade = st.selectbox("Sub Grade",
#         ["A1","A2","A3","A4","A5",
#          "B1","B2","B3","B4","B5",
#          "C1","C2","C3","C4","C5"]
#     )
#     purpose = st.selectbox("Purpose",
#         ["credit_card","debt_consolidation",
#          "home_improvement","major_purchase",
#          "small_business","other"]
#     )

#     st.divider()

#     st.header("👤 Employment & Income")
#     emp_length = st.number_input("Employment Length (Years)", min_value=0, value=5)
#     annual_inc = st.number_input("Annual Income", min_value=0.0, value=60000.0)
#     verification_status = st.selectbox(
#         "Verification Status",
#         ["Verified","Source Verified","Not Verified"]
#     )

#     st.divider()

#     st.header("🏠 Housing Profile")
#     home_ownership = st.selectbox(
#         "Home Ownership",
#         ["RENT","OWN","MORTGAGE","OTHER"]
#     )
#     mort_acc = st.number_input("Mortgage Accounts", min_value=0, value=1)

#     st.divider()

#     st.header("📊 Credit Score & Age")
#     fico = st.number_input("FICO Score", min_value=300, max_value=900, value=700)
#     credit_age = st.number_input("Credit Age (Months)", min_value=0, value=120)

#     st.divider()

#     st.header("📉 Credit Utilization")
#     revol_util = st.number_input("Revolving Utilization (%)", min_value=0.0, max_value=100.0, value=30.0)
#     bc_util = st.number_input("BC Utilization (%)", min_value=0.0, max_value=100.0, value=40.0)
#     percent_bc_gt_75 = st.number_input("Percent BC > 75%", min_value=0.0, max_value=100.0, value=10.0)
#     revol_bal = st.number_input("Revolving Balance", min_value=0.0, value=5000.0)
#     total_bc_limit = st.number_input("Total BC Limit", min_value=0.0, value=20000.0)
#     avg_cur_bal = st.number_input("Average Current Balance", min_value=0.0, value=10000.0)
#     tot_cur_bal = st.number_input("Total Current Balance", min_value=0.0, value=50000.0)
#     bc_open_to_buy = st.number_input("BC Open To Buy", min_value=0.0, value=10000.0)

#     st.divider()

#     st.header("📈 Credit Behavior")
#     inq_last_6mths = st.number_input("Inquiries Last 6 Months", min_value=0, value=1)
#     acc_open_past_24mths = st.number_input("Accounts Open Past 24 Months", min_value=0, value=2)
#     num_actv_bc_tl = st.number_input("Active BC TL", min_value=0, value=3)
#     num_actv_rev_tl = st.number_input("Active Rev TL", min_value=0, value=4)

#     st.divider()

#     st.header("⏳ Account Vintage")
#     mo_sin_old_rev_tl_op = st.number_input("Months Since Oldest Rev TL", min_value=0, value=120)
#     mo_sin_rcnt_tl = st.number_input("Months Since Recent TL", min_value=0, value=6)
#     mths_since_recent_bc = st.number_input("Months Since Recent BC", min_value=0, value=5)
#     mths_since_recent_inq = st.number_input("Months Since Recent Inquiry", min_value=0, value=2)

#     st.divider()

#     st.header("💰 Risk Ratios")
#     dti = st.number_input("Debt To Income Ratio", min_value=0.0, max_value=100.0, value=15.0)

#     generate_btn = st.button("Generate PD Scores")


# # =====================================================
# # RAW INPUT DICTIONARY
# # =====================================================

# raw_input = {
#     "grade": grade,
#     "sub_grade": sub_grade,
#     "term": term,
#     "int_rate": int_rate,
#     "loan_amnt": loan_amnt,
#     "annual_inc": annual_inc,
#     "dti": dti,
#     "fico": fico,
#     "emp_length": emp_length,
#     "mort_acc": mort_acc,
#     "home_ownership": home_ownership,
#     "verification_status": verification_status,
#     "purpose": purpose,
#     "credit_age": credit_age,
#     "revol_util": revol_util,
#     "bc_util": bc_util,
#     "percent_bc_gt_75": percent_bc_gt_75,
#     "acc_open_past_24mths": acc_open_past_24mths,
#     "avg_cur_bal": avg_cur_bal,
#     "tot_cur_bal": tot_cur_bal,
#     "total_bc_limit": total_bc_limit,
#     "revol_bal": revol_bal,
#     "inq_last_6mths": inq_last_6mths,
#     "mths_since_recent_bc": mths_since_recent_bc,
#     "mths_since_recent_inq": mths_since_recent_inq,
#     "mo_sin_old_rev_tl_op": mo_sin_old_rev_tl_op,
#     "mo_sin_rcnt_tl": mo_sin_rcnt_tl,
#     "num_actv_bc_tl": num_actv_bc_tl,
#     "num_actv_rev_tl": num_actv_rev_tl,
#     "bc_open_to_buy": bc_open_to_buy,
# }


# # =====================================================
# # OUTPUT SECTION
# # =====================================================

# if generate_btn:

#     try:

#         validated_raw = validate_raw_input(raw_input)

#         lr_vector = LRInputVector().build(validated_raw)
#         xgb_vector = XGBInputVector().build(validated_raw)

#         lr_pd = lr_predictor.predict_pd_percent(lr_vector)
#         xgb_pd = xgb_predictor.predict_pd_percent(xgb_vector)

#         lr_decision = decision_engine.evaluate(lr_pd)
#         xgb_decision = decision_engine.evaluate(xgb_pd)

#         st.success("PD Calculation Successful")

#         # ------------------------------
#         # Decision Badge Function
#         # ------------------------------

#         def decision_badge(text):
#             if "Approve" in text:
#                 color = "#155724"
#                 bg = "#d4edda"
#             elif "Review" in text:
#                 color = "#856404"
#                 bg = "#fff3cd"
#             elif "Decline" in text:
#                 color = "#721c24"
#                 bg = "#f8d7da"
#             else:
#                 color = "#383d41"
#                 bg = "#e2e3e5"

#             return f"""
#             <div style="
#                 padding:10px;
#                 background:{bg};
#                 color:{color};
#                 border-radius:8px;
#                 text-align:center;
#                 font-weight:600;">
#                 {text}
#             </div>
#             """

#         # =====================================================
#         # LR RESULTS BOX
#         # =====================================================

#         st.markdown("## Logistic Regression Predictions")
#         lr_cols = st.columns(4)

#         lr_cols[0].metric("PD (%)", f"{lr_decision['pd_percent']:.2f}%")
#         lr_cols[1].metric("Credit Score", lr_decision["credit_score"])
#         lr_cols[2].metric("Rating Band", lr_decision["rating_band"])
#         lr_cols[3].markdown(decision_badge(lr_decision["decision"]), unsafe_allow_html=True)

#         st.divider()

#         # =====================================================
#         # XGB RESULTS BOX
#         # =====================================================

#         st.markdown("## XGBoost Predictions")
#         xgb_cols = st.columns(4)

#         xgb_cols[0].metric("PD (%)", f"{xgb_decision['pd_percent']:.2f}%")
#         xgb_cols[1].metric("Credit Score", xgb_decision["credit_score"])
#         xgb_cols[2].metric("Rating Band", xgb_decision["rating_band"])
#         xgb_cols[3].markdown(decision_badge(xgb_decision["decision"]), unsafe_allow_html=True)

#         st.divider()

#         # =====================================================
#         # INPUT VECTOR TABLES
#         # =====================================================

#         col1, col2 = st.columns(2)

#         with col1:
#             st.subheader("📘 LR Model Input Vector")
#             st.dataframe(lr_vector, use_container_width=True)

#         with col2:
#             st.subheader("📗 XGB Model Input Vector")
#             st.dataframe(xgb_vector, use_container_width=True)

#     except Exception as e:
#         st.error(f"Validation / Prediction Error: {str(e)}")






























import streamlit as st
import pandas as pd

from raw_user_input import validate_raw_input
from LR_input_vector import LRInputVector
from XGB_input_vector import XGBInputVector
from LR_PD_predictor import LRPDPredictor
from XGB_PD_predictor import XGBPDPredictor
from pd_to_decision_engine import PDDecisionEngine


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(page_title="Credit Risk PD Engine", layout="wide")

st.title("📊 Credit Risk PD Engine")
st.markdown("### Dual Model Evaluation: Logistic Regression & XGBoost")

# Smaller metric font
st.markdown("""
<style>
div[data-testid="metric-container"] {
    font-size: 14px !important;
}
div[data-testid="metric-container"] > div {
    font-size: 22px !important;
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# LOAD MODELS
# =====================================================

@st.cache_resource
def load_lr():
    return LRPDPredictor("LR_model.joblib")

@st.cache_resource
def load_xgb():
    return XGBPDPredictor("XGB_model.joblib")

lr_predictor = load_lr()
xgb_predictor = load_xgb()
decision_engine = PDDecisionEngine()


# =====================================================
# SIDEBAR INPUT
# =====================================================

with st.sidebar:

    st.header("🏦 Loan Details")
    loan_amnt = st.number_input("Loan Amount", min_value=0.0, value=10000.0)
    term = st.selectbox("Term (Months)", [36, 60])
    int_rate = st.number_input("Interest Rate (%)", min_value=0.0, max_value=40.0, value=12.0)
    grade = st.selectbox("Grade", ["A","B","C","D","E","F","G"])
    sub_grade = st.selectbox("Sub Grade",
        ["A1","A2","A3","A4","A5",
         "B1","B2","B3","B4","B5",
         "C1","C2","C3","C4","C5"]
    )
    purpose = st.selectbox("Purpose",
        ["credit_card","debt_consolidation",
         "home_improvement","major_purchase",
         "small_business","other"]
    )

    st.divider()

    st.header("👤 Employment & Income")
    emp_length = st.number_input("Employment Length (Years)", min_value=0, value=5)
    annual_inc = st.number_input("Annual Income", min_value=0.0, value=60000.0)
    verification_status = st.selectbox(
        "Verification Status",
        ["Verified","Source Verified","Not Verified"]
    )

    st.divider()

    st.header("🏠 Housing Profile")
    home_ownership = st.selectbox(
        "Home Ownership",
        ["RENT","OWN","MORTGAGE","OTHER"]
    )
    mort_acc = st.number_input("Mortgage Accounts", min_value=0, value=1)

    st.divider()

    st.header("📊 Credit Score & Age")
    fico = st.number_input("FICO Score", min_value=300, max_value=900, value=700)
    credit_age = st.number_input("Credit Age (Months)", min_value=0, value=120)

    st.divider()

    st.header("📉 Credit Utilization")
    revol_util = st.number_input("Revolving Utilization (%)", min_value=0.0, max_value=100.0, value=30.0)
    bc_util = st.number_input("BC Utilization (%)", min_value=0.0, max_value=100.0, value=40.0)
    percent_bc_gt_75 = st.number_input("Percent BC > 75%", min_value=0.0, max_value=100.0, value=10.0)
    revol_bal = st.number_input("Revolving Balance", min_value=0.0, value=5000.0)
    total_bc_limit = st.number_input("Total BC Limit", min_value=0.0, value=20000.0)
    avg_cur_bal = st.number_input("Average Current Balance", min_value=0.0, value=10000.0)
    tot_cur_bal = st.number_input("Total Current Balance", min_value=0.0, value=50000.0)
    bc_open_to_buy = st.number_input("BC Open To Buy", min_value=0.0, value=10000.0)

    st.divider()

    st.header("📈 Credit Behavior")
    inq_last_6mths = st.number_input("Inquiries Last 6 Months", min_value=0, value=1)
    acc_open_past_24mths = st.number_input("Accounts Open Past 24 Months", min_value=0, value=2)
    num_actv_bc_tl = st.number_input("Active BC TL", min_value=0, value=3)
    num_actv_rev_tl = st.number_input("Active Rev TL", min_value=0, value=4)

    st.divider()

    st.header("⏳ Account Vintage")
    mo_sin_old_rev_tl_op = st.number_input("Months Since Oldest Rev TL", min_value=0, value=120)
    mo_sin_rcnt_tl = st.number_input("Months Since Recent TL", min_value=0, value=6)
    mths_since_recent_bc = st.number_input("Months Since Recent BC", min_value=0, value=5)
    mths_since_recent_inq = st.number_input("Months Since Recent Inquiry", min_value=0, value=2)

    st.divider()

    st.header("💰 Risk Ratios")
    dti = st.number_input("Debt To Income Ratio", min_value=0.0, max_value=100.0, value=15.0)

    generate_btn = st.button("Generate PD Scores")


# =====================================================
# RAW INPUT
# =====================================================

raw_input = locals()


# =====================================================
# OUTPUT
# =====================================================

if generate_btn:

    try:

        validated_raw = validate_raw_input(raw_input)

        lr_vector = LRInputVector().build(validated_raw)
        xgb_vector = XGBInputVector().build(validated_raw)

        lr_pd = lr_predictor.predict_pd_percent(lr_vector)
        xgb_pd = xgb_predictor.predict_pd_percent(xgb_vector)

        lr_decision = decision_engine.evaluate(lr_pd)
        xgb_decision = decision_engine.evaluate(xgb_pd)

        st.success("PD Calculation Successful")

        # =====================================================
        # LR BOX
        # =====================================================

        st.markdown("## Logistic Regression Predictions")
        cols = st.columns(4)

        cols[0].metric("PD (%)", f"{lr_decision['pd_percent']:.2f}%")
        cols[1].metric("Credit Score", lr_decision["credit_score"])
        cols[2].metric("Rating Band", lr_decision["rating_band"])
        cols[3].metric("Final Decision", lr_decision["decision"])

        st.divider()

        # =====================================================
        # XGB BOX
        # =====================================================

        st.markdown("## XGBoost Predictions")
        cols = st.columns(4)

        cols[0].metric("PD (%)", f"{xgb_decision['pd_percent']:.2f}%")
        cols[1].metric("Credit Score", xgb_decision["credit_score"])
        cols[2].metric("Rating Band", xgb_decision["rating_band"])
        cols[3].metric("Final Decision", xgb_decision["decision"])

        st.divider()

        # =====================================================
        # VERTICAL INPUT TABLES (3 COLUMN)
        # =====================================================

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📘 LR Model Input Details")

            lr_display = pd.DataFrame({
                "Feature": lr_vector.columns,
                "Raw User Input": [validated_raw.get(f, None) for f in lr_vector.columns],
                "Model Ready (WOE)": lr_vector.iloc[0].values
            })

            st.dataframe(lr_display, use_container_width=True)

        with col2:
            st.subheader("📗 XGB Model Input Details")

            xgb_display = pd.DataFrame({
                "Feature": xgb_vector.columns,
                "Raw User Input": [validated_raw.get(f, None) for f in xgb_vector.columns],
                "Model Ready (Encoded)": xgb_vector.iloc[0].values
            })

            st.dataframe(xgb_display, use_container_width=True)

    except Exception as e:
        st.error(f"Validation / Prediction Error: {str(e)}")























