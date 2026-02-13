# raw_user_input.py

from typing import Dict, List
import math


# ==========================================================
# FEATURE SEGREGATION (SYSTEM CONTRACT)
# ==========================================================

# ---------- LR MODEL RAW FEATURES ----------
LR_RAW_FEATURES: List[str] = [
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

# ---------- XGB ADDITIONAL RAW FEATURES ----------
XGB_ADDITIONAL_RAW_FEATURES: List[str] = [
    'grade',
    'sub_grade',
    'mort_acc',
    'avg_cur_bal',
    'tot_cur_bal',
    'total_bc_limit',
    'revol_bal',
    'num_actv_bc_tl',
    'num_actv_rev_tl',
    'mo_sin_old_rev_tl_op',
    'mths_since_recent_bc',
    'bc_open_to_buy'
]

# ---------- SYSTEM-WIDE REQUIRED RAW FEATURES ----------
ALL_REQUIRED_RAW_FEATURES: List[str] = (
    LR_RAW_FEATURES + XGB_ADDITIONAL_RAW_FEATURES
)

# ---------- UI FEATURES ----------
# These are fields user must explicitly provide in UI
UI_INPUT_FEATURES: List[str] = ALL_REQUIRED_RAW_FEATURES.copy()


# ==========================================================
# ALLOWED CATEGORICAL VALUES
# ==========================================================

ALLOWED_HOME = {"MORTGAGE", "OWN", "RENT", "OTHER"}
ALLOWED_TERM = {36, 60}
ALLOWED_VERIFICATION = {"Verified", "Source Verified", "Not Verified"}
ALLOWED_GRADE = {"A", "B", "C", "D", "E", "F", "G"}

ALLOWED_PURPOSE = {
    "credit_card", "debt_consolidation", "home_improvement",
    "major_purchase", "small_business", "other",
    "wedding", "vacation", "car", "house",
    "medical", "moving", "renewable_energy",
    "educational"
}


# ==========================================================
# VALIDATION HELPERS
# ==========================================================

def _is_missing(x):
    return x is None or (isinstance(x, float) and math.isnan(x))


def _require_field_presence(raw: Dict):
    missing = [f for f in ALL_REQUIRED_RAW_FEATURES if f not in raw]
    if missing:
        raise ValueError(f"Missing required raw fields: {missing}")


def _require_non_negative(name, value):
    if value < 0:
        raise ValueError(f"{name} cannot be negative.")


def _require_percentage(name, value):
    if value < 0 or value > 100:
        raise ValueError(f"{name} must be between 0 and 100.")


def _require_range(name, value, min_v, max_v):
    if value < min_v or value > max_v:
        raise ValueError(f"{name} must be between {min_v} and {max_v}.")


def _require_category(name, value, allowed_set):
    if value not in allowed_set:
        raise ValueError(
            f"{name} must be one of {sorted(list(allowed_set))}. "
            f"Received: {value}"
        )


# ==========================================================
# ENTERPRISE VALIDATION ENGINE
# ==========================================================

def validate_raw_input(raw: Dict) -> Dict:
    """
    Enterprise-grade validation layer.
    Ensures:
        - All required features present
        - Correct logical ranges
        - Valid categorical values
        - No silent type mismatches
        - Business constraints enforced
    Returns:
        Cleaned & validated raw dictionary
    """

    _require_field_presence(raw)

    # ==============================
    # CATEGORICAL VALIDATION
    # ==============================

    _require_category("home_ownership", raw["home_ownership"], ALLOWED_HOME)
    _require_category("verification_status", raw["verification_status"], ALLOWED_VERIFICATION)
    _require_category("term", raw["term"], ALLOWED_TERM)
    _require_category("grade", raw["grade"], ALLOWED_GRADE)
    _require_category("purpose", raw["purpose"], ALLOWED_PURPOSE)

    # ==============================
    # NUMERIC VALIDATION (LR + XGB)
    # ==============================

    numeric_non_negative = [
        "emp_length",
        "credit_age",
        "int_rate",
        "loan_amnt",
        "annual_inc",
        "inq_last_6mths",
        "acc_open_past_24mths",
        "mo_sin_rcnt_tl",
        "mths_since_recent_inq",
        "mort_acc",
        "avg_cur_bal",
        "tot_cur_bal",
        "total_bc_limit",
        "revol_bal",
        "num_actv_bc_tl",
        "num_actv_rev_tl",
        "mo_sin_old_rev_tl_op",
        "mths_since_recent_bc",
        "bc_open_to_buy"
    ]

    for field in numeric_non_negative:
        if _is_missing(raw[field]):
            raise ValueError(f"{field} cannot be missing.")
        _require_non_negative(field, raw[field])

    # Percentage features
    percentage_fields = [
        "dti",
        "revol_util",
        "bc_util",
        "percent_bc_gt_75"
    ]

    for field in percentage_fields:
        if _is_missing(raw[field]):
            raise ValueError(f"{field} cannot be missing.")
        _require_percentage(field, raw[field])

    # FICO strict enforcement
    _require_range("fico", raw["fico"], 300, 900)

    # ==============================
    # TYPE NORMALIZATION
    # ==============================

    # Convert all numeric values to float
    for key, value in raw.items():
        if isinstance(value, int):
            raw[key] = float(value)

    return raw


# ==========================================================
# QC UTILITIES
# ==========================================================

def get_feature_summary():
    """
    Returns structured feature segregation for inspection / logging.
    """

    return {
        "LR_features": LR_RAW_FEATURES,
        "XGB_only_features": XGB_ADDITIONAL_RAW_FEATURES,
        "All_required_features": ALL_REQUIRED_RAW_FEATURES,
        "UI_input_features": UI_INPUT_FEATURES,
        "Total_feature_count": len(ALL_REQUIRED_RAW_FEATURES)
    }
