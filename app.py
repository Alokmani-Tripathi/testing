import streamlit as st
import pandas as pd

st.set_page_config(page_title="Feature Segregation App", layout="wide")

st.title("Common Input → XGB & LR Feature Segregation")

# =====================================================
# 1️⃣ Define Feature Lists
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

ALL_FEATURES = sorted(list(set(XGB_FEATURES + LR_FEATURES)))

# =====================================================
# 2️⃣ Input Layer (All 34 Unique Features)
# =====================================================

st.header("Enter All Feature Inputs")

input_data = {}

for feature in ALL_FEATURES:
    input_data[feature] = st.text_input(feature)

# =====================================================
# 3️⃣ On Button Click → Segregate
# =====================================================

if st.button("Segregate Features"):

    # Convert to DataFrame
    input_df = pd.DataFrame([input_data])

    # Segregate
    xgb_input = input_df[XGB_FEATURES]
    lr_input = input_df[LR_FEATURES]

    st.success("Segregation Complete")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("XGB Model Input")
        st.dataframe(xgb_input)

    with col2:
        st.subheader("LR Model Input")
        st.dataframe(lr_input)
