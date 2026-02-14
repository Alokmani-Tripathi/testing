# # LR_input_vector.py

# import pandas as pd
# import math
# from typing import Dict
# from raw_user_input import validate_raw_input


# # ==========================================================
# # LR FEATURE ORDER (STRICT — DO NOT CHANGE)
# # ==========================================================

# LR_FEATURE_ORDER = [
#     'emp_length',
#     'home_ownership',
#     'purpose',
#     'term',
#     'verification_status',
#     'credit_age',
#     'int_rate',
#     'loan_amnt',
#     'fico',
#     'annual_inc',
#     'inq_last_6mths',
#     'dti',
#     'revol_util',
#     'bc_util',
#     'percent_bc_gt_75',
#     'acc_open_past_24mths',
#     'mo_sin_rcnt_tl',
#     'mths_since_recent_inq'
# ]


# # ==========================================================
# # WOE DICTIONARY (COPIED — SELF CONTAINED)
# # ==========================================================

# WOE_DICT = {
#     "emp_length": {"10+": 0.075569, "5-9": 0.020044, "<5": -0.009668},
#     "home_ownership": {
#         "MORTGAGE": 0.181942,
#         "OTHER": 0.025399,
#         "OWN": -0.040206,
#         "RENT": -0.19211
#     },
#     "purpose_group": {
#         "wedding": 0.265251,
#         "vacation": 0.265251,
#         "car": 0.265251,
#         "credit_card": 0.176408,
#         "home_improvement": 0.176408,
#         "major_purchase": 0.176408,
#         "house": 0.176408,
#         "debt_consolidation": -0.082874,
#         "medical": -0.082874,
#         "moving": -0.082874,
#         "renewable_energy": -0.082874,
#         "small_business": -0.082874,
#         "other": -0.082874,
#         "educational": -0.082874
#     },
#     "term": {"36 months": 0.26918, "60 months": -0.654419},
#     "verification_status": {
#         "Not Verified": 0.367984,
#         "Source Verified": -0.060243,
#         "Verified": -0.227229
#     },
#     "credit_age": {
#         "20y+": 0.126171,
#         "10-20y": -0.015303,
#         "5-10y": -0.09759,
#         "<5y": -0.246351
#     },
#     "annual_inc": {
#         "<40k": -0.214757,
#         "40-60k": -0.098178,
#         "60-80k": 0.015539,
#         "80-120k": 0.168065,
#         "120k+": 0.323362
#     },
#     "fico": {
#         "<660": -0.384124,
#         "660-679": -0.254997,
#         "680-699": -0.023191,
#         "700-719": 0.251562,
#         "720-759": 0.577379,
#         "760+": 1.056444
#     },
#     "inq_last_6mths": {
#         "0-1": 0.05885,
#         "2": -0.234536,
#         "3+": -0.38363
#     },
#     "int_rate": {
#         "<=7%": 1.714661,
#         "7-10%": 0.85143,
#         "10-13%": 0.247831,
#         "13-16%": -0.172235,
#         "16-20%": -0.600758,
#         "20%+": -1.015004
#     },
#     "loan_amnt": {
#         "<=5000": 0.284335,
#         "5000-10000": 0.181317,
#         "10000-15000": -0.049287,
#         "15000-20000": -0.158532,
#         "20000-30000": -0.176376,
#         "30000+": -0.261182
#     },
#     "dti": {
#         "<10": 0.353121,
#         "10-20": 0.137611,
#         "20-30": -0.182373,
#         "30-40": -0.497065,
#         "40+": -0.566149
#     },
#     "revol_util": {
#         "<20": 0.349468,
#         "20-40": 0.128666,
#         "40-60": -0.03359,
#         "60-80": -0.113119,
#         "80+": -0.165093
#     },
#     "bc_util": {
#         "<20": 0.290122,
#         "20-40": 0.18103,
#         "40-60": 0.039957,
#         "60-80": -0.054759,
#         "80+": -0.189892
#     },
#     "percent_bc_gt_75": {
#         "0": 0.25277,
#         "1-33": 0.081136,
#         "34-66": -0.034972,
#         "67+": -0.191386
#     },
#     "acc_open_past_24mths": {
#         "0-1": 0.374241,
#         "2-3": 0.195587,
#         "4-6": -0.046794,
#         "7+": -0.342579
#     },
#     "mo_sin_rcnt_tl": {
#         "<=3": -0.192933,
#         "4-6": -0.046111,
#         "7-12": 0.074747,
#         "13+": 0.291707
#     },
#     "mths_since_recent_inq": {
#         "<=3": -0.20405,
#         "4-6": -0.027539,
#         "7-12": 0.060127,
#         "13+": 0.168196
#     }
# }


# # ==========================================================
# # BIN FUNCTIONS
# # ==========================================================

# def build_lr_input_vector(raw: Dict) -> pd.DataFrame:

#     raw = validate_raw_input(raw)
#     woe = {}

#     # emp_length
#     if raw["emp_length"] >= 10:
#         bin_key = "10+"
#     elif raw["emp_length"] >= 5:
#         bin_key = "5-9"
#     else:
#         bin_key = "<5"
#     woe["emp_length"] = WOE_DICT["emp_length"][bin_key]

#     # home
#     woe["home_ownership"] = WOE_DICT["home_ownership"][raw["home_ownership"]]

#     # purpose
#     woe["purpose"] = WOE_DICT["purpose_group"].get(raw["purpose"], -0.082874)

#     # term
#     woe["term"] = WOE_DICT["term"][f"{raw['term']} months"]

#     # verification
#     woe["verification_status"] = WOE_DICT["verification_status"][raw["verification_status"]]

#     # credit age
#     years = raw["credit_age"] / 12
#     if years >= 20:
#         bin_key = "20y+"
#     elif years >= 10:
#         bin_key = "10-20y"
#     elif years >= 5:
#         bin_key = "5-10y"
#     else:
#         bin_key = "<5y"
#     woe["credit_age"] = WOE_DICT["credit_age"][bin_key]

#     # int rate
#     ir = raw["int_rate"]
#     if ir <= 7:
#         bin_key = "<=7%"
#     elif ir <= 10:
#         bin_key = "7-10%"
#     elif ir <= 13:
#         bin_key = "10-13%"
#     elif ir <= 16:
#         bin_key = "13-16%"
#     elif ir <= 20:
#         bin_key = "16-20%"
#     else:
#         bin_key = "20%+"
#     woe["int_rate"] = WOE_DICT["int_rate"][bin_key]

#     # loan amount
#     la = raw["loan_amnt"]
#     if la <= 5000:
#         bin_key = "<=5000"
#     elif la <= 10000:
#         bin_key = "5000-10000"
#     elif la <= 15000:
#         bin_key = "10000-15000"
#     elif la <= 20000:
#         bin_key = "15000-20000"
#     elif la <= 30000:
#         bin_key = "20000-30000"
#     else:
#         bin_key = "30000+"
#     woe["loan_amnt"] = WOE_DICT["loan_amnt"][bin_key]

#     # fico
#     fico = raw["fico"]
#     if fico < 660:
#         bin_key = "<660"
#     elif fico <= 679:
#         bin_key = "660-679"
#     elif fico <= 699:
#         bin_key = "680-699"
#     elif fico <= 719:
#         bin_key = "700-719"
#     elif fico <= 759:
#         bin_key = "720-759"
#     else:
#         bin_key = "760+"
#     woe["fico"] = WOE_DICT["fico"][bin_key]

#     # annual income
#     inc = raw["annual_inc"]
#     if inc < 40000:
#         bin_key = "<40k"
#     elif inc < 60000:
#         bin_key = "40-60k"
#     elif inc < 80000:
#         bin_key = "60-80k"
#     elif inc < 120000:
#         bin_key = "80-120k"
#     else:
#         bin_key = "120k+"
#     woe["annual_inc"] = WOE_DICT["annual_inc"][bin_key]

#     # inquiries
#     inq = raw["inq_last_6mths"]
#     if inq <= 1:
#         bin_key = "0-1"
#     elif inq == 2:
#         bin_key = "2"
#     else:
#         bin_key = "3+"
#     woe["inq_last_6mths"] = WOE_DICT["inq_last_6mths"][bin_key]

#     # dti
#     dti = raw["dti"]
#     if dti < 10:
#         bin_key = "<10"
#     elif dti < 20:
#         bin_key = "10-20"
#     elif dti < 30:
#         bin_key = "20-30"
#     elif dti < 40:
#         bin_key = "30-40"
#     else:
#         bin_key = "40+"
#     woe["dti"] = WOE_DICT["dti"][bin_key]

#     # revol_util
#     ru = raw["revol_util"]
#     if ru < 20:
#         bin_key = "<20"
#     elif ru < 40:
#         bin_key = "20-40"
#     elif ru < 60:
#         bin_key = "40-60"
#     elif ru < 80:
#         bin_key = "60-80"
#     else:
#         bin_key = "80+"
#     woe["revol_util"] = WOE_DICT["revol_util"][bin_key]

#     # bc_util
#     bu = raw["bc_util"]
#     if bu < 20:
#         bin_key = "<20"
#     elif bu < 40:
#         bin_key = "20-40"
#     elif bu < 60:
#         bin_key = "40-60"
#     elif bu < 80:
#         bin_key = "60-80"
#     else:
#         bin_key = "80+"
#     woe["bc_util"] = WOE_DICT["bc_util"][bin_key]

#     # percent_bc_gt_75
#     p = raw["percent_bc_gt_75"]
#     if p == 0:
#         bin_key = "0"
#     elif p <= 33:
#         bin_key = "1-33"
#     elif p <= 66:
#         bin_key = "34-66"
#     else:
#         bin_key = "67+"
#     woe["percent_bc_gt_75"] = WOE_DICT["percent_bc_gt_75"][bin_key]

#     # acc open
#     acc = raw["acc_open_past_24mths"]
#     if acc <= 1:
#         bin_key = "0-1"
#     elif acc <= 3:
#         bin_key = "2-3"
#     elif acc <= 6:
#         bin_key = "4-6"
#     else:
#         bin_key = "7+"
#     woe["acc_open_past_24mths"] = WOE_DICT["acc_open_past_24mths"][bin_key]

#     # mo_sin_rcnt_tl
#     ms = raw["mo_sin_rcnt_tl"]
#     if ms <= 3:
#         bin_key = "<=3"
#     elif ms <= 6:
#         bin_key = "4-6"
#     elif ms <= 12:
#         bin_key = "7-12"
#     else:
#         bin_key = "13+"
#     woe["mo_sin_rcnt_tl"] = WOE_DICT["mo_sin_rcnt_tl"][bin_key]

#     # mths_since_recent_inq
#     mi = raw["mths_since_recent_inq"]
#     if mi <= 3:
#         bin_key = "<=3"
#     elif mi <= 6:
#         bin_key = "4-6"
#     elif mi <= 12:
#         bin_key = "7-12"
#     else:
#         bin_key = "13+"
#     woe["mths_since_recent_inq"] = WOE_DICT["mths_since_recent_inq"][bin_key]

#     df = pd.DataFrame([woe])[LR_FEATURE_ORDER]
#     df = df.astype("float64")

#     return df


















# LR_input_vector.py

import pandas as pd
from typing import Dict
from raw_user_input import validate_raw_input


class LRInputVector:

    # ==========================================================
    # STRICT FEATURE ORDER (DO NOT CHANGE)
    # ==========================================================

    FEATURE_ORDER = [
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

    # ==========================================================
    # WOE DICTIONARY (SELF-CONTAINED)
    # ==========================================================

    WOE_DICT = {
        "emp_length": {"10+": 0.075569, "5-9": 0.020044, "<5": -0.009668},
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
            "educational": -0.082874
        },
        "term": {"36 months": 0.26918, "60 months": -0.654419},
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
            "120k+": 0.323362
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
            "40+": -0.566149
        },
        "revol_util": {
            "<20": 0.349468,
            "20-40": 0.128666,
            "40-60": -0.03359,
            "60-80": -0.113119,
            "80+": -0.165093
        },
        "bc_util": {
            "<20": 0.290122,
            "20-40": 0.18103,
            "40-60": 0.039957,
            "60-80": -0.054759,
            "80+": -0.189892
        },
        "percent_bc_gt_75": {
            "0": 0.25277,
            "1-33": 0.081136,
            "34-66": -0.034972,
            "67+": -0.191386
        },
        "acc_open_past_24mths": {
            "0-1": 0.374241,
            "2-3": 0.195587,
            "4-6": -0.046794,
            "7+": -0.342579
        },
        "mo_sin_rcnt_tl": {
            "<=3": -0.192933,
            "4-6": -0.046111,
            "7-12": 0.074747,
            "13+": 0.291707
        },
        "mths_since_recent_inq": {
            "<=3": -0.20405,
            "4-6": -0.027539,
            "7-12": 0.060127,
            "13+": 0.168196
        }
    }

    # ==========================================================
    # MAIN BUILD METHOD
    # ==========================================================

    def build(self, raw: Dict) -> pd.DataFrame:

        raw = validate_raw_input(raw)
        woe = {}

        # --- All binning logic remains exactly same ---
        # (keeping your exact logic, unchanged)

        # emp_length
        if raw["emp_length"] >= 10:
            bin_key = "10+"
        elif raw["emp_length"] >= 5:
            bin_key = "5-9"
        else:
            bin_key = "<5"
        woe["emp_length"] = self.WOE_DICT["emp_length"][bin_key]

        # home_ownership
        woe["home_ownership"] = self.WOE_DICT["home_ownership"][raw["home_ownership"]]

        # purpose
        woe["purpose"] = self.WOE_DICT["purpose_group"].get(raw["purpose"], -0.082874)

        # term
        #woe["term"] = self.WOE_DICT["term"][f"{raw['term']} months"]

        term_value = int(raw["term"])

        if term_value not in (36, 60):
           raise ValueError("term must be 36 or 60.")

        #woe["term"] = WOE_DICT["term"][f"{term_value} months"]
        woe["term"] = self.WOE_DICT["term"][f"{term_value} months"]


        # verification_status
        woe["verification_status"] = self.WOE_DICT["verification_status"][raw["verification_status"]]

        # credit_age
        years = raw["credit_age"] / 12
        if years >= 20:
            bin_key = "20y+"
        elif years >= 10:
            bin_key = "10-20y"
        elif years >= 5:
            bin_key = "5-10y"
        else:
            bin_key = "<5y"
        woe["credit_age"] = self.WOE_DICT["credit_age"][bin_key]

        # int_rate
        ir = raw["int_rate"]
        if ir <= 7:
            bin_key = "<=7%"
        elif ir <= 10:
            bin_key = "7-10%"
        elif ir <= 13:
            bin_key = "10-13%"
        elif ir <= 16:
            bin_key = "13-16%"
        elif ir <= 20:
            bin_key = "16-20%"
        else:
            bin_key = "20%+"
        woe["int_rate"] = self.WOE_DICT["int_rate"][bin_key]

        # loan_amnt
        la = raw["loan_amnt"]
        if la <= 5000:
            bin_key = "<=5000"
        elif la <= 10000:
            bin_key = "5000-10000"
        elif la <= 15000:
            bin_key = "10000-15000"
        elif la <= 20000:
            bin_key = "15000-20000"
        elif la <= 30000:
            bin_key = "20000-30000"
        else:
            bin_key = "30000+"
        woe["loan_amnt"] = self.WOE_DICT["loan_amnt"][bin_key]

        # fico
        fico = raw["fico"]
        if fico < 660:
            bin_key = "<660"
        elif fico <= 679:
            bin_key = "660-679"
        elif fico <= 699:
            bin_key = "680-699"
        elif fico <= 719:
            bin_key = "700-719"
        elif fico <= 759:
            bin_key = "720-759"
        else:
            bin_key = "760+"
        woe["fico"] = self.WOE_DICT["fico"][bin_key]

        # annual_inc
        inc = raw["annual_inc"]
        if inc < 40000:
            bin_key = "<40k"
        elif inc < 60000:
            bin_key = "40-60k"
        elif inc < 80000:
            bin_key = "60-80k"
        elif inc < 120000:
            bin_key = "80-120k"
        else:
            bin_key = "120k+"
        woe["annual_inc"] = self.WOE_DICT["annual_inc"][bin_key]

        # inquiries
        inq = raw["inq_last_6mths"]
        if inq <= 1:
            bin_key = "0-1"
        elif inq == 2:
            bin_key = "2"
        else:
            bin_key = "3+"
        woe["inq_last_6mths"] = self.WOE_DICT["inq_last_6mths"][bin_key]

        # dti
        dti = raw["dti"]
        if dti < 10:
            bin_key = "<10"
        elif dti < 20:
            bin_key = "10-20"
        elif dti < 30:
            bin_key = "20-30"
        elif dti < 40:
            bin_key = "30-40"
        else:
            bin_key = "40+"
        woe["dti"] = self.WOE_DICT["dti"][bin_key]

        # revol_util
        ru = raw["revol_util"]
        if ru < 20:
            bin_key = "<20"
        elif ru < 40:
            bin_key = "20-40"
        elif ru < 60:
            bin_key = "40-60"
        elif ru < 80:
            bin_key = "60-80"
        else:
            bin_key = "80+"
        woe["revol_util"] = self.WOE_DICT["revol_util"][bin_key]

        # bc_util
        bu = raw["bc_util"]
        if bu < 20:
            bin_key = "<20"
        elif bu < 40:
            bin_key = "20-40"
        elif bu < 60:
            bin_key = "40-60"
        elif bu < 80:
            bin_key = "60-80"
        else:
            bin_key = "80+"
        woe["bc_util"] = self.WOE_DICT["bc_util"][bin_key]

        # percent_bc_gt_75
        p = raw["percent_bc_gt_75"]
        if p == 0:
            bin_key = "0"
        elif p <= 33:
            bin_key = "1-33"
        elif p <= 66:
            bin_key = "34-66"
        else:
            bin_key = "67+"
        woe["percent_bc_gt_75"] = self.WOE_DICT["percent_bc_gt_75"][bin_key]

        # acc_open_past_24mths
        acc = raw["acc_open_past_24mths"]
        if acc <= 1:
            bin_key = "0-1"
        elif acc <= 3:
            bin_key = "2-3"
        elif acc <= 6:
            bin_key = "4-6"
        else:
            bin_key = "7+"
        woe["acc_open_past_24mths"] = self.WOE_DICT["acc_open_past_24mths"][bin_key]

        # mo_sin_rcnt_tl
        ms = raw["mo_sin_rcnt_tl"]
        if ms <= 3:
            bin_key = "<=3"
        elif ms <= 6:
            bin_key = "4-6"
        elif ms <= 12:
            bin_key = "7-12"
        else:
            bin_key = "13+"
        woe["mo_sin_rcnt_tl"] = self.WOE_DICT["mo_sin_rcnt_tl"][bin_key]

        # mths_since_recent_inq
        mi = raw["mths_since_recent_inq"]
        if mi <= 3:
            bin_key = "<=3"
        elif mi <= 6:
            bin_key = "4-6"
        elif mi <= 12:
            bin_key = "7-12"
        else:
            bin_key = "13+"
        woe["mths_since_recent_inq"] = self.WOE_DICT["mths_since_recent_inq"][bin_key]

        df = pd.DataFrame([woe])[self.FEATURE_ORDER]
        df = df.astype("float64")

        return df
