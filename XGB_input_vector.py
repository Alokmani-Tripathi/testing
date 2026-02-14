# XGB_input_vector.py

import pandas as pd


class XGBInputVector:

    # =====================================================
    # EXACT TRAINING FEATURE ORDER (DO NOT CHANGE)
    # =====================================================

    FEATURE_ORDER = [
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

    # =====================================================
    # TRAINING DTYPE MAP
    # =====================================================

    DTYPE_MAP = {
        'grade': 'int64',
        'sub_grade': 'int64',
        'term': 'float64',
        'int_rate': 'float64',
        'acc_open_past_24mths': 'float64',
        'avg_cur_bal': 'float64',
        'home_ownership_MORTGAGE': 'bool',
        'dti': 'float64',
        'fico': 'float64',
        'home_ownership_RENT': 'bool',
        'mort_acc': 'float64',
        'annual_inc': 'float64',
        'emp_length': 'float64',
        'purpose_small_business': 'bool',
        'loan_amnt': 'float64',
        'verification_status_Source Verified': 'bool',
        'tot_cur_bal': 'float64',
        'mths_since_recent_bc': 'float64',
        'num_actv_rev_tl': 'float64',
        'mths_since_recent_inq': 'float64',
        'total_bc_limit': 'float64',
        'inq_last_6mths': 'float64',
        'mo_sin_old_rev_tl_op': 'float64',
        'mo_sin_rcnt_tl': 'float64',
        'bc_open_to_buy': 'float64',
        'num_actv_bc_tl': 'float64',
        'revol_bal': 'float64'
    }

    # =====================================================
    # CATEGORY MAPS FROM TRAINING
    # =====================================================

    GRADE_MAP = {'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7}

    EMP_LENGTH_MAP = {
        '< 1 year':0,'1 year':1,'2 years':2,'3 years':3,'4 years':4,
        '5 years':5,'6 years':6,'7 years':7,'8 years':8,'9 years':9,
        '10+ years':10
    }

    # sub_grade mapping
    SUB_GRADE_MAP = {
        f"{g}{i}": (g_idx * 5 + i)
        for g_idx, g in enumerate(['A','B','C','D','E','F','G'])
        for i in range(1,6)
    }

    # =====================================================
    # MAIN TRANSFORM
    # =====================================================

    def build(self, raw: dict) -> pd.DataFrame:

        df = pd.DataFrame([raw])

        # ---------------------------
        # Grade Mapping
        # ---------------------------
        if df["grade"].iloc[0] not in self.GRADE_MAP:
            raise ValueError("Invalid grade value.")
        df["grade"] = df["grade"].map(self.GRADE_MAP)

        # ---------------------------
        # Sub Grade Mapping
        # ---------------------------
        if df["sub_grade"].iloc[0] not in self.SUB_GRADE_MAP:
            raise ValueError("Invalid sub_grade value.")
        df["sub_grade"] = df["sub_grade"].map(self.SUB_GRADE_MAP)

        # ---------------------------
        # Term: 36/60
        # ---------------------------
        df["term"] = df["term"].astype(float)

        # ---------------------------
        # Employment Length (numeric years already)
        # ---------------------------
        df["emp_length"] = df["emp_length"].astype(float)

        # ---------------------------
        # One Hot Encoding (drop_first=True logic)
        # ---------------------------

        df["home_ownership_MORTGAGE"] = df["home_ownership"] == "MORTGAGE"
        df["home_ownership_RENT"] = df["home_ownership"] == "RENT"

        df["purpose_small_business"] = df["purpose"] == "small_business"

        df["verification_status_Source Verified"] = (
            df["verification_status"] == "Source Verified"
        )

        # ---------------------------
        # Drop original categorical cols
        # ---------------------------

        df = df.drop(columns=[
            "home_ownership",
            "purpose",
            "verification_status"
        ])

        # ---------------------------
        # Strict Feature Order
        # ---------------------------

        missing = set(self.FEATURE_ORDER) - set(df.columns)
        if missing:
            raise ValueError(f"Missing required features: {missing}")

        df = df[self.FEATURE_ORDER]

        # ---------------------------
        # Strict Dtype Casting
        # ---------------------------

        for col, dtype in self.DTYPE_MAP.items():
            if dtype == "bool":
                df[col] = df[col].astype(bool)
            else:
                df[col] = df[col].astype(dtype)

        return df
