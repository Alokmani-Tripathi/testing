import streamlit as st
import pandas as pd

st.set_page_config(page_title="Feature Segregation App", layout="wide")
st.title("Common Input → XGB & LR Feature Segregation")

# =====================================================
# 1️⃣ Feature Lists
# =====================================================

XGB_FEATURES = [
    'grade',
    'sub_grade',
    'term',
    'int_rate',
    'acc_open_past_24mths',
    'avg_cur_bal',
    'home_ownership_MORTGAGE',
    'dti',
    'fico',
    'home_ownership_RENT',
    'mort_acc',
    'annual_inc',
    'emp_length',
    'purpose_small_business',
    'loan_amnt',
    'verification_status_Source Verified',
    'tot_cur_bal',
    'mths_since_recent_bc',
    'num_actv_rev_tl',
    'mths_since_recent_inq',
    'total_bc_limit',
    'inq_last_6mths',
    'mo_sin_old_rev_tl_op',
    'mo_sin_rcnt_tl',
    'bc_open_to_buy',
    'num_actv_bc_tl',
    'revol_bal'
]

LR_FEATURES = [
    'emp_length',
    'home_ownership',
    'purpose',
    'term',
    'verification_status',
    'credit_age',
    'int_rate',
    'loan_amnt',
    'fico',
    'annual_inc',
    'inq_last_6mths',
    'dti',
    'revol_util',
    'bc_util',
    'percent_bc_gt_75',
    'acc_open_past_24mths',
    'mo_sin_rcnt_tl',
    'mths_since_recent_inq'
]

# =====================================================
# 2️⃣ User Inputs (Raw Only)
# =====================================================

st.header("Enter Applicant Details")

# Categorical Inputs
grade = st.selectbox("Grade", ["A","B","C","D","E","F","G"])
sub_grade = st.selectbox("Sub Grade", [
    "A1","A2","A3","A4","A5",
    "B1","B2","B3","B4","B5",
    "C1","C2","C3","C4","C5",
    "D1","D2","D3","D4","D5",
    "E1","E2","E3","E4","E5",
    "F1","F2","F3","F4","F5",
    "G1","G2","G3","G4","G5"
])

term = st.selectbox("Term (Months)", [36, 60])
home_ownership = st.selectbox("Home Ownership", ["RENT","OWN","MORTGAGE","OTHER"])
verification_status = st.selectbox("Verification Status", ["Verified","Source Verified","Not Verified"])
purpose = st.selectbox("Purpose", ["credit_card","debt_consolidation","home_improvement","major_purchase","small_business","other"])

# Numeric Inputs
loan_amnt = st.number_input("Loan Amount", value=10000.0)
int_rate = st.number_input("Interest Rate", value=12.0)
annual_inc = st.number_input("Annual Income", value=60000.0)
dti = st.number_input("DTI", value=15.0)
fico = st.number_input("FICO", value=700)
emp_length = st.number_input("Employment Length (Years)", value=5)
mort_acc = st.number_input("Mortgage Accounts", value=1)
acc_open_past_24mths = st.number_input("Accounts Open Past 24 Months", value=2)
avg_cur_bal = st.number_input("Average Current Balance", value=10000.0)
tot_cur_bal = st.number_input("Total Current Balance", value=50000.0)
total_bc_limit = st.number_input("Total BC Limit", value=20000.0)
revol_bal = st.number_input("Revolving Balance", value=5000.0)
inq_last_6mths = st.number_input("Inquiries Last 6 Months", value=1)
mths_since_recent_bc = st.number_input("Months Since Recent BC", value=5)
mths_since_recent_inq = st.number_input("Months Since Recent Inquiry", value=2)
mo_sin_old_rev_tl_op = st.number_input("Months Since Oldest Rev TL", value=120)
mo_sin_rcnt_tl = st.number_input("Months Since Recent TL", value=6)
num_actv_bc_tl = st.number_input("Active BC TL", value=3)
num_actv_rev_tl = st.number_input("Active Rev TL", value=4)
bc_open_to_buy = st.number_input("BC Open To Buy", value=10000.0)
credit_age = st.number_input("Credit Age (Months)", value=120)
revol_util = st.number_input("Revolving Utilization", value=30.0)
bc_util = st.number_input("BC Utilization", value=40.0)
percent_bc_gt_75 = st.number_input("Percent BC > 75%", value=10.0)

# =====================================================
# 3️⃣ Auto One-Hot Generation (Boolean)
# =====================================================

home_ownership_MORTGAGE = home_ownership == "MORTGAGE"
home_ownership_RENT = home_ownership == "RENT"
verification_status_Source_Verified = verification_status == "Source Verified"
purpose_small_business = purpose == "small_business"

# =====================================================
# 4️⃣ Build Input DataFrame
# =====================================================

input_data = {
    # Raw categorical
    "home_ownership": home_ownership,
    "verification_status": verification_status,
    "purpose": purpose,

    # Auto-generated booleans
    "home_ownership_MORTGAGE": home_ownership_MORTGAGE,
    "home_ownership_RENT": home_ownership_RENT,
    "verification_status_Source Verified": verification_status_Source_Verified,
    "purpose_small_business": purpose_small_business,

    # Other features
    "grade": grade,
    "sub_grade": sub_grade,
    "term": term,
    "loan_amnt": loan_amnt,
    "int_rate": int_rate,
    "annual_inc": annual_inc,
    "dti": dti,
    "fico": fico,
    "emp_length": emp_length,
    "mort_acc": mort_acc,
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
    "credit_age": credit_age,
    "revol_util": revol_util,
    "bc_util": bc_util,
    "percent_bc_gt_75": percent_bc_gt_75
}

input_df = pd.DataFrame([input_data])

# =====================================================
# 5️⃣ Segregate for Each Model
# =====================================================

if st.button("Segregate Inputs"):

    xgb_input = input_df[XGB_FEATURES].copy()
    lr_input = input_df[LR_FEATURES].copy()

    # Convert boolean columns to True/False text
    for col in xgb_input.columns:
        if xgb_input[col].dtype == bool:
            xgb_input[col] = xgb_input[col].astype(str)

    for col in lr_input.columns:
        if lr_input[col].dtype == bool:
            lr_input[col] = lr_input[col].astype(str)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("XGB Model Input")
        st.dataframe(xgb_input)

    with col2:
        st.subheader("LR Model Input")
        st.dataframe(lr_input)

