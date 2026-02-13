# import streamlit as st
# import pandas as pd

# st.set_page_config(page_title="Credit Risk Input App", layout="wide")
# st.title("Credit Risk Input Interface")
# st.markdown("### Applicant Risk Profiling Form")

# # =====================================================
# # MODEL FEATURE ORDER (DO NOT CHANGE)
# # =====================================================

# XGB_FEATURES = [
#     'grade','sub_grade','term','int_rate','acc_open_past_24mths',
#     'avg_cur_bal','home_ownership_MORTGAGE','dti','fico',
#     'home_ownership_RENT','mort_acc','annual_inc','emp_length',
#     'purpose_small_business','loan_amnt',
#     'verification_status_Source Verified','tot_cur_bal',
#     'mths_since_recent_bc','num_actv_rev_tl','mths_since_recent_inq',
#     'total_bc_limit','inq_last_6mths','mo_sin_old_rev_tl_op',
#     'mo_sin_rcnt_tl','bc_open_to_buy','num_actv_bc_tl','revol_bal'
# ]

# LR_FEATURES = [
#     'emp_length','home_ownership','purpose','term',
#     'verification_status','credit_age','int_rate',
#     'loan_amnt','fico','annual_inc','inq_last_6mths','dti',
#     'revol_util','bc_util','percent_bc_gt_75',
#     'acc_open_past_24mths','mo_sin_rcnt_tl','mths_since_recent_inq'
# ]

# # =====================================================
# # SIDEBAR INPUT PANEL (VERTICAL + ALL UMBRELLAS)
# # =====================================================

# with st.sidebar:

#     st.header("🏦 Loan Details")
#     loan_amnt = st.number_input("Loan Amount", value=10000.0)
#     term = st.selectbox("Term (Months)", [36, 60])
#     int_rate = st.number_input("Interest Rate (%)", value=12.0)
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
#     emp_length = st.number_input("Employment Length (Years)", value=5)
#     annual_inc = st.number_input("Annual Income", value=60000.0)
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
#     mort_acc = st.number_input("Mortgage Accounts", value=1)

#     st.divider()

#     st.header("📊 Credit Score & Age")
#     fico = st.number_input("FICO Score", value=700)
#     credit_age = st.number_input("Credit Age (Months)", value=120)

#     st.divider()

#     st.header("📉 Credit Utilization")
#     revol_util = st.number_input("Revolving Utilization (%)", value=30.0)
#     bc_util = st.number_input("BC Utilization (%)", value=40.0)
#     percent_bc_gt_75 = st.number_input("Percent BC > 75%", value=10.0)
#     revol_bal = st.number_input("Revolving Balance", value=5000.0)
#     total_bc_limit = st.number_input("Total BC Limit", value=20000.0)
#     avg_cur_bal = st.number_input("Average Current Balance", value=10000.0)
#     tot_cur_bal = st.number_input("Total Current Balance", value=50000.0)
#     bc_open_to_buy = st.number_input("BC Open To Buy", value=10000.0)

#     st.divider()

#     st.header("📈 Credit Behavior")
#     inq_last_6mths = st.number_input("Inquiries Last 6 Months", value=1)
#     acc_open_past_24mths = st.number_input("Accounts Open Past 24 Months", value=2)
#     num_actv_bc_tl = st.number_input("Active BC TL", value=3)
#     num_actv_rev_tl = st.number_input("Active Rev TL", value=4)

#     st.divider()

#     st.header("⏳ Account Vintage")
#     mo_sin_old_rev_tl_op = st.number_input("Months Since Oldest Rev TL", value=120)
#     mo_sin_rcnt_tl = st.number_input("Months Since Recent TL", value=6)
#     mths_since_recent_bc = st.number_input("Months Since Recent BC", value=5)
#     mths_since_recent_inq = st.number_input("Months Since Recent Inquiry", value=2)

#     st.divider()

#     st.header("💰 Risk Ratios")
#     dti = st.number_input("Debt To Income Ratio", value=15.0)

#     generate_btn = st.button("Generate Model Inputs")

# # =====================================================
# # AUTO ONE-HOT (BOOLEAN)
# # =====================================================

# home_ownership_MORTGAGE = home_ownership == "MORTGAGE"
# home_ownership_RENT = home_ownership == "RENT"
# purpose_small_business = purpose == "small_business"
# verification_status_source_verified_bool = (
#     verification_status == "Source Verified"
# )

# # =====================================================
# # BUILD MASTER INPUT
# # =====================================================

# input_data = {
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
#     "home_ownership_MORTGAGE": home_ownership_MORTGAGE,
#     "home_ownership_RENT": home_ownership_RENT,
#     "purpose_small_business": purpose_small_business,
#     "verification_status_Source Verified": verification_status_source_verified_bool
# }

# input_df = pd.DataFrame([input_data])

# # =====================================================
# # OUTPUT AREA
# # =====================================================

# if generate_btn:

#     st.success("Model Inputs Generated Successfully")

#     xgb_input = input_df[XGB_FEATURES]
#     lr_input = input_df[LR_FEATURES]

#     col1, col2 = st.columns(2)

#     with col1:
#         st.subheader("XGB Model Input (Order Preserved)")
#         st.dataframe(xgb_input.astype(str), use_container_width=True)

#     with col2:
#         st.subheader("LR Model Input (Order Preserved)")
#         st.dataframe(lr_input.astype(str), use_container_width=True)




























# import streamlit as st
# import pandas as pd
# from woe_transformer import transform_to_woe

# st.set_page_config(page_title="Credit Risk Input App", layout="wide")
# st.title("Credit Risk Input Interface")
# st.markdown("### Applicant Risk Profiling Form")

# # =====================================================
# # MODEL FEATURE ORDER (DO NOT CHANGE)
# # =====================================================

# XGB_FEATURES = [
#     'grade','sub_grade','term','int_rate','acc_open_past_24mths',
#     'avg_cur_bal','home_ownership_MORTGAGE','dti','fico',
#     'home_ownership_RENT','mort_acc','annual_inc','emp_length',
#     'purpose_small_business','loan_amnt',
#     'verification_status_Source Verified','tot_cur_bal',
#     'mths_since_recent_bc','num_actv_rev_tl','mths_since_recent_inq',
#     'total_bc_limit','inq_last_6mths','mo_sin_old_rev_tl_op',
#     'mo_sin_rcnt_tl','bc_open_to_buy','num_actv_bc_tl','revol_bal'
# ]

# LR_FEATURES = [
#     'emp_length','home_ownership','purpose','term',
#     'verification_status','credit_age','int_rate',
#     'loan_amnt','fico','annual_inc','inq_last_6mths','dti',
#     'revol_util','bc_util','percent_bc_gt_75',
#     'acc_open_past_24mths','mo_sin_rcnt_tl','mths_since_recent_inq'
# ]

# # =====================================================
# # SIDEBAR INPUT PANEL WITH VALID LIMITS
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

#     generate_btn = st.button("Generate Model Inputs")

# # =====================================================
# # AUTO ONE HOT
# # =====================================================

# home_ownership_MORTGAGE = home_ownership == "MORTGAGE"
# home_ownership_RENT = home_ownership == "RENT"
# purpose_small_business = purpose == "small_business"
# verification_status_source_verified_bool = (
#     verification_status == "Source Verified"
# )

# # =====================================================
# # BUILD RAW INPUT DICT
# # =====================================================

# input_data = {
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
#     "home_ownership_MORTGAGE": home_ownership_MORTGAGE,
#     "home_ownership_RENT": home_ownership_RENT,
#     "purpose_small_business": purpose_small_business,
#     "verification_status_Source Verified": verification_status_source_verified_bool
# }

# input_df = pd.DataFrame([input_data])

# # =====================================================
# # OUTPUT
# # =====================================================

# if generate_btn:

#     try:

#         st.success("Model Inputs Generated Successfully")

#         # Raw Segregation
#         xgb_input = input_df[XGB_FEATURES]
#         lr_input = input_df[LR_FEATURES]

#         # WOE Transformation
#         woe_dict = transform_to_woe(input_data)
#         lr_woe_df = pd.DataFrame([woe_dict])[LR_FEATURES]

#         st.write("WOE Dtypes:")
#         st.write(lr_woe_df.dtypes)


#         col1, col2, col3 = st.columns(3)

#         with col1:
#             st.subheader("XGB Raw Input")
#             st.dataframe(xgb_input, use_container_width=True)

#         with col2:
#             st.subheader("LR Raw Input")
#             st.dataframe(lr_input, use_container_width=True)

#         with col3:
#             st.subheader("LR WOE Input")
#             st.dataframe(lr_woe_df, use_container_width=True)

#     except Exception as e:
#         st.error(f"Input Validation Error: {str(e)}")
































import streamlit as st
import pandas as pd
from woe_transformer import transform_to_woe
from LR_PD_predictor import LRPDPredictor

st.set_page_config(page_title="Credit Risk Input App", layout="wide")
st.title("Credit Risk Input Interface")
st.markdown("### Applicant Risk Profiling Form")

# =====================================================
# LOAD LR MODEL (CACHED)
# =====================================================

@st.cache_resource
def load_lr_predictor():
    return LRPDPredictor("LR_model.joblib")

lr_predictor = load_lr_predictor()

# =====================================================
# MODEL FEATURE ORDER (DO NOT CHANGE)
# =====================================================

XGB_FEATURES = [
    'grade','sub_grade','term','int_rate','acc_open_past_24mths',
    'avg_cur_bal','home_ownership_MORTGAGE','dti','fico',
    'home_ownership_RENT','mort_acc','annual_inc','emp_length',
    'purpose_small_business','loan_amnt',
    'verification_status_Source Verified','tot_cur_bal',
    'mths_since_recent_bc','num_actv_rev_tl','mths_since_recent_inq',
    'total_bc_limit','inq_last_6mths','mo_sin_old_rev_tl_op',
    'mo_sin_rcnt_tl','bc_open_to_buy','num_actv_bc_tl','revol_bal'
]

LR_FEATURES = [
    'emp_length','home_ownership','purpose','term',
    'verification_status','credit_age','int_rate',
    'loan_amnt','fico','annual_inc','inq_last_6mths','dti',
    'revol_util','bc_util','percent_bc_gt_75',
    'acc_open_past_24mths','mo_sin_rcnt_tl','mths_since_recent_inq'
]

# =====================================================
# SIDEBAR INPUT PANEL
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

    generate_btn = st.button("Generate Model Inputs")

# =====================================================
# AUTO ONE HOT
# =====================================================

home_ownership_MORTGAGE = home_ownership == "MORTGAGE"
home_ownership_RENT = home_ownership == "RENT"
purpose_small_business = purpose == "small_business"
verification_status_source_verified_bool = (
    verification_status == "Source Verified"
)

# =====================================================
# BUILD RAW INPUT
# =====================================================

input_data = {
    "grade": grade,
    "sub_grade": sub_grade,
    "term": term,
    "int_rate": int_rate,
    "loan_amnt": loan_amnt,
    "annual_inc": annual_inc,
    "dti": dti,
    "fico": fico,
    "emp_length": emp_length,
    "mort_acc": mort_acc,
    "home_ownership": home_ownership,
    "verification_status": verification_status,
    "purpose": purpose,
    "credit_age": credit_age,
    "revol_util": revol_util,
    "bc_util": bc_util,
    "percent_bc_gt_75": percent_bc_gt_75,
    "acc_open_past_24mths": acc_open_past_24mths,
    "avg_cur_bal": avg_cur_bal,
    "tot_cur_bal": tot_cur_bal,
    "total_bc_limit": total_bc_limit,
    "revol_bal": revol_bal,
    "inq_last_6mths": inq_last_6mths,
    "mths_since_recent_bc": mths_since_recent_bc,
    "mths_since_recent_inq": mths_since_recent_inq,
    "mo_sin_old_rev_tl_op": mo_sin_old_rev_tl_op,
    "mo_sin_rcnt_tl": mo_sin_rcnt_tl,
    "num_actv_bc_tl": num_actv_bc_tl,
    "num_actv_rev_tl": num_actv_rev_tl,
    "bc_open_to_buy": bc_open_to_buy,
    "home_ownership_MORTGAGE": home_ownership_MORTGAGE,
    "home_ownership_RENT": home_ownership_RENT,
    "purpose_small_business": purpose_small_business,
    "verification_status_Source Verified": verification_status_source_verified_bool
}

input_df = pd.DataFrame([input_data])

# =====================================================
# OUTPUT
# =====================================================

if generate_btn:

    try:

        st.success("Model Inputs Generated Successfully")

        xgb_input = input_df[XGB_FEATURES]
        lr_input = input_df[LR_FEATURES]

        woe_dict = transform_to_woe(input_data)
        lr_woe_df = pd.DataFrame([woe_dict])[LR_FEATURES]

        # Predict PD%
        pd_percent = lr_predictor.predict_pd_percent(lr_woe_df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.subheader("XGB Raw Input")
            st.dataframe(xgb_input, use_container_width=True)

        with col2:
            st.subheader("LR Raw Input")
            st.dataframe(lr_input, use_container_width=True)

        with col3:
            st.subheader("LR WOE Input")
            st.dataframe(lr_woe_df, use_container_width=True)

        with col4:
            st.subheader("Predicted PD")
            st.metric("Probability of Default (%)", f"{pd_percent} %")

    except Exception as e:
        st.error(f"Validation / Prediction Error: {str(e)}")


























