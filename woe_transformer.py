# woe_transformer.py

import math

# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def is_missing(x):
    return x is None or (isinstance(x, float) and math.isnan(x))


def require_non_negative(name, value):
    if value < 0:
        raise ValueError(f"{name} cannot be negative.")


def require_percentage(name, value):
    if value < 0 or value > 100:
        raise ValueError(f"{name} must be between 0 and 100.")


# ==========================================================
# WOE DICTIONARY
# ==========================================================

WOE_DICT = {
    "emp_length": {
        "10+": 0.075569,
        "5-9": 0.020044,
        "<5": -0.009668,
        "Missing": -0.389095
    },
    "home_ownership": {
        "MORTGAGE": 0.181942,
        "OTHER": 0.025399,
        "OWN": -0.040206,
        "RENT": -0.19211
    },
    "purpose_group": {
        "wedding": 0.265251,
        "vacation": 0.265251,
        "car": 0.265251,
        "credit_card": 0.176408,
        "home_improvement": 0.176408,
        "major_purchase": 0.176408,
        "house": 0.176408,
        "debt_consolidation": -0.082874,
        "medical": -0.082874,
        "moving": -0.082874,
        "renewable_energy": -0.082874,
        "small_business": -0.082874,
        "other": -0.082874,
        "educational": -0.082874,
        "missing": -0.082874
    },
    "term": {
        "36 months": 0.26918,
        "60 months": -0.654419
    },
    "verification_status": {
        "Not Verified": 0.367984,
        "Source Verified": -0.060243,
        "Verified": -0.227229
    },
    "credit_age": {
        "20y+": 0.126171,
        "10-20y": -0.015303,
        "5-10y": -0.09759,
        "<5y": -0.246351
    },
    "annual_inc": {
        "<40k": -0.214757,
        "40-60k": -0.098178,
        "60-80k": 0.015539,
        "80-120k": 0.168065,
        "120k+": 0.323362,
        "Missing": 1.54927
    },
    "fico": {
        "<660": -0.384124,
        "660-679": -0.254997,
        "680-699": -0.023191,
        "700-719": 0.251562,
        "720-759": 0.577379,
        "760+": 1.056444
    },
    "inq_last_6mths": {
        "0-1": 0.05885,
        "2": -0.234536,
        "3+": -0.38363
    },
    "int_rate": {
        "<=7%": 1.714661,
        "7-10%": 0.85143,
        "10-13%": 0.247831,
        "13-16%": -0.172235,
        "16-20%": -0.600758,
        "20%+": -1.015004
    },
    "loan_amnt": {
        "<=5000": 0.284335,
        "5000-10000": 0.181317,
        "10000-15000": -0.049287,
        "15000-20000": -0.158532,
        "20000-30000": -0.176376,
        "30000+": -0.261182
    },
    "dti": {
        "<10": 0.353121,
        "10-20": 0.137611,
        "20-30": -0.182373,
        "30-40": -0.497065,
        "40+": -0.566149,
        "Missing": 0.063321
    },
    "bc_util": {
        "<20": 0.290122,
        "20-40": 0.18103,
        "40-60": 0.039957,
        "60-80": -0.054759,
        "80+": -0.189892,
        "Missing": 0.223846
    },
    "percent_bc_gt_75": {
        "0": 0.25277,
        "1-33": 0.081136,
        "34-66": -0.034972,
        "67+": -0.191386,
        "Missing": 0.227168
    },
    "revol_util": {
        "<20": 0.349468,
        "20-40": 0.128666,
        "40-60": -0.03359,
        "60-80": -0.113119,
        "80+": -0.165093,
        "Missing": -0.046505
    },
    "acc_open_past_24mths": {
        "0-1": 0.374241,
        "2-3": 0.195587,
        "4-6": -0.046794,
        "7+": -0.342579,
        "Missing": 0.324925
    },
    "mo_sin_rcnt_tl": {
        "<=3": -0.192933,
        "4-6": -0.046111,
        "7-12": 0.074747,
        "13+": 0.291707,
        "Missing": 0.288314
    },
    "mths_since_recent_inq": {
        "<=3": -0.20405,
        "4-6": -0.027539,
        "7-12": 0.060127,
        "13+": 0.168196,
        "Missing": 0.340916
    }
}

# ==========================================================
# BIN FUNCTIONS WITH VALIDATION
# ==========================================================

def bin_emp_length(x):
    if is_missing(x):
        return "Missing"
    require_non_negative("emp_length", x)
    if x >= 10:
        return "10+"
    if 5 <= x <= 9:
        return "5-9"
    return "<5"


def bin_credit_age(x):
    if is_missing(x):
        raise ValueError("credit_age is mandatory.")
    require_non_negative("credit_age", x)
    years = x / 12
    if years >= 20:
        return "20y+"
    if years >= 10:
        return "10-20y"
    if years >= 5:
        return "5-10y"
    return "<5y"


def bin_annual_inc(x):
    if is_missing(x):
        return "Missing"
    require_non_negative("annual_inc", x)
    if x < 40000:
        return "<40k"
    if x < 60000:
        return "40-60k"
    if x < 80000:
        return "60-80k"
    if x < 120000:
        return "80-120k"
    return "120k+"


def bin_fico(x):
    if is_missing(x):
        raise ValueError("fico is mandatory.")
    if x < 300 or x > 900:
        raise ValueError("fico must be between 300 and 900.")
    if x < 660:
        return "<660"
    if x <= 679:
        return "660-679"
    if x <= 699:
        return "680-699"
    if x <= 719:
        return "700-719"
    if x <= 759:
        return "720-759"
    return "760+"


def bin_int_rate(x):
    if is_missing(x):
        raise ValueError("int_rate is mandatory.")
    require_non_negative("int_rate", x)
    if x <= 7:
        return "<=7%"
    if x <= 10:
        return "7-10%"
    if x <= 13:
        return "10-13%"
    if x <= 16:
        return "13-16%"
    if x <= 20:
        return "16-20%"
    return "20%+"


def bin_loan_amnt(x):
    if is_missing(x):
        raise ValueError("loan_amnt is mandatory.")
    require_non_negative("loan_amnt", x)
    if x <= 5000:
        return "<=5000"
    if x <= 10000:
        return "5000-10000"
    if x <= 15000:
        return "10000-15000"
    if x <= 20000:
        return "15000-20000"
    if x <= 30000:
        return "20000-30000"
    return "30000+"


def bin_dti(x):
    if is_missing(x):
        return "Missing"
    require_percentage("dti", x)
    if x < 10:
        return "<10"
    if x < 20:
        return "10-20"
    if x < 30:
        return "20-30"
    if x < 40:
        return "30-40"
    return "40+"


def bin_util(x, name):
    if is_missing(x):
        return "Missing"
    require_percentage(name, x)
    if x < 20:
        return "<20"
    if x < 40:
        return "20-40"
    if x < 60:
        return "40-60"
    if x < 80:
        return "60-80"
    return "80+"


def bin_percent_bc_gt_75(x):
    if is_missing(x):
        return "Missing"
    require_percentage("percent_bc_gt_75", x)
    if x == 0:
        return "0"
    if x <= 33:
        return "1-33"
    if x <= 66:
        return "34-66"
    return "67+"


def bin_acc_open(x):
    if is_missing(x):
        return "Missing"
    require_non_negative("acc_open_past_24mths", x)
    if x <= 1:
        return "0-1"
    if x <= 3:
        return "2-3"
    if x <= 6:
        return "4-6"
    return "7+"


def bin_mo_sin(x, name):
    if is_missing(x):
        return "Missing"
    require_non_negative(name, x)
    if x <= 3:
        return "<=3"
    if x <= 6:
        return "4-6"
    if x <= 12:
        return "7-12"
    return "13+"


# ==========================================================
# MAIN TRANSFORM FUNCTION
# ==========================================================

def transform_to_woe(raw):

    woe = {}

    woe["emp_length"] = WOE_DICT["emp_length"][bin_emp_length(raw["emp_length"])]
    woe["home_ownership"] = WOE_DICT["home_ownership"][raw["home_ownership"]]
    woe["purpose"] = WOE_DICT["purpose_group"].get(
        raw["purpose"], WOE_DICT["purpose_group"]["missing"]
    )
    woe["term"] = WOE_DICT["term"][f"{raw['term']} months"]
    woe["verification_status"] = WOE_DICT["verification_status"][raw["verification_status"]]
    woe["credit_age"] = WOE_DICT["credit_age"][bin_credit_age(raw["credit_age"])]
    woe["int_rate"] = WOE_DICT["int_rate"][bin_int_rate(raw["int_rate"])]
    woe["loan_amnt"] = WOE_DICT["loan_amnt"][bin_loan_amnt(raw["loan_amnt"])]
    woe["fico"] = WOE_DICT["fico"][bin_fico(raw["fico"])]
    woe["annual_inc"] = WOE_DICT["annual_inc"][bin_annual_inc(raw["annual_inc"])]
    woe["inq_last_6mths"] = WOE_DICT["inq_last_6mths"][bin_acc_open(raw["inq_last_6mths"])]
    woe["dti"] = WOE_DICT["dti"][bin_dti(raw["dti"])]
    woe["revol_util"] = WOE_DICT["revol_util"][bin_util(raw["revol_util"], "revol_util")]
    woe["bc_util"] = WOE_DICT["bc_util"][bin_util(raw["bc_util"], "bc_util")]
    woe["percent_bc_gt_75"] = WOE_DICT["percent_bc_gt_75"][bin_percent_bc_gt_75(raw["percent_bc_gt_75"])]
    woe["acc_open_past_24mths"] = WOE_DICT["acc_open_past_24mths"][bin_acc_open(raw["acc_open_past_24mths"])]
    woe["mo_sin_rcnt_tl"] = WOE_DICT["mo_sin_rcnt_tl"][bin_mo_sin(raw["mo_sin_rcnt_tl"], "mo_sin_rcnt_tl")]
    woe["mths_since_recent_inq"] = WOE_DICT["mths_since_recent_inq"][bin_mo_sin(raw["mths_since_recent_inq"], "mths_since_recent_inq")]

    return woe
