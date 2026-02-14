# # pd_to_decision_engine.py

# import numpy as np
# import pandas as pd


# class PDDecisionEngine:
#     """
#     Enterprise-grade PD → Score → Rating → Decision engine.
#     Generic input: PD in percentage form (e.g., 2.45 for 2.45%)
#     """

#     # ==========================================================
#     # 1️⃣ SCALING CONFIG (Option A - Institutional Standard)
#     # ==========================================================

#     BASE_SCORE = 650
#     BASE_ODDS = 20        # 20:1 good:bad at base score
#     PDO = 50              # 50 points doubles the odds

#     FACTOR = PDO / np.log(2)
#     OFFSET = BASE_SCORE - FACTOR * np.log(BASE_ODDS)

#     # ==========================================================
#     # 2️⃣ RATING BAND STRUCTURE (AAA → CCC)
#     # ==========================================================

#     BAND_STRUCTURE = [
#         ("AAA", 800, np.inf),
#         ("AA", 750, 800),
#         ("A", 700, 750),
#         ("BBB", 650, 700),
#         ("BB", 600, 650),
#         ("B", 550, 600),
#         ("CCC", -np.inf, 550),
#     ]

#     # ==========================================================
#     # 3️⃣ DECISION POLICY (Bank Style)
#     # ==========================================================

#     DECISION_MAP = {
#         "AAA": "Auto Approve",
#         "AA": "Auto Approve",
#         "A": "Approve",
#         "BBB": "Approve with Risk-Based Pricing",
#         "BB": "Manual Review",
#         "B": "Secured / Collateral Required",
#         "CCC": "Decline"
#     }

#     # ==========================================================
#     # 4️⃣ VALIDATION
#     # ==========================================================

#     @staticmethod
#     def _validate_pd(pd_percent: float):

#         if pd_percent is None:
#             raise ValueError("PD cannot be None.")

#         if not isinstance(pd_percent, (int, float)):
#             raise ValueError("PD must be numeric.")

#         if pd_percent <= 0 or pd_percent >= 100:
#             raise ValueError("PD must be between 0 and 100 (exclusive).")

#     # ==========================================================
#     # 5️⃣ PD → SCORE TRANSFORMATION
#     # ==========================================================

#     def _pd_to_score(self, pd_percent: float) -> float:

#         pd_decimal = pd_percent / 100

#         odds = (1 - pd_decimal) / pd_decimal

#         score = self.OFFSET + self.FACTOR * np.log(odds)

#         return round(score, 0)

#     # ==========================================================
#     # 6️⃣ SCORE → RATING BAND
#     # ==========================================================

#     def _score_to_band(self, score: float) -> str:

#         for band, lower, upper in self.BAND_STRUCTURE:
#             if lower <= score < upper:
#                 return band

#         raise ValueError("Score band mapping failed.")

#     # ==========================================================
#     # 7️⃣ MAIN PUBLIC METHOD
#     # ==========================================================

#     def evaluate(self, pd_percent: float) -> pd.DataFrame:
#         """
#         Main evaluation method.
#         Returns structured DataFrame output.
#         """

#         self._validate_pd(pd_percent)

#         score = self._pd_to_score(pd_percent)
#         rating = self._score_to_band(score)
#         decision = self.DECISION_MAP[rating]

#         result = pd.DataFrame([{
#             "PD (%)": round(pd_percent, 4),
#             "Score": score,
#             "Rating Band": rating,
#             "Decision": decision
#         }])

#         return result










# pd_to_decision_engine.py

import numpy as np
import pandas as pd


class PDDecisionEngine:
    """
    Enterprise-grade PD → Score → Rating → Decision engine.
    Generic input: PD in percentage form (e.g., 2.45 for 2.45%)
    Supports multi-model usage (LR / XGB / future models)
    """

    # ==========================================================
    # 1️⃣ SCALING CONFIG (Institutional Standard)
    # ==========================================================

    BASE_SCORE = 650
    BASE_ODDS = 20        # 20:1 good:bad at base score
    PDO = 50              # 50 points doubles the odds

    FACTOR = PDO / np.log(2)
    OFFSET = BASE_SCORE - FACTOR * np.log(BASE_ODDS)

    # ==========================================================
    # 2️⃣ RATING BAND STRUCTURE
    # ==========================================================

    BAND_STRUCTURE = [
        ("AAA", 800, np.inf),
        ("AA", 750, 800),
        ("A", 700, 750),
        ("BBB", 650, 700),
        ("BB", 600, 650),
        ("B", 550, 600),
        ("CCC", -np.inf, 550),
    ]

    # ==========================================================
    # 3️⃣ DECISION POLICY
    # ==========================================================

    DECISION_MAP = {
        "AAA": "Auto Approve",
        "AA": "Auto Approve",
        "A": "Approve",
        "BBB": "Approve with Risk-Based Pricing",
        "BB": "Manual Review",
        "B": "Secured / Collateral Required",
        "CCC": "Decline"
    }

    # ==========================================================
    # 4️⃣ VALIDATION
    # ==========================================================

    @staticmethod
    def _validate_pd(pd_percent: float):

        if pd_percent is None:
            raise ValueError("PD cannot be None.")

        if not isinstance(pd_percent, (int, float)):
            raise ValueError("PD must be numeric.")

        if pd_percent <= 0 or pd_percent >= 100:
            raise ValueError("PD must be between 0 and 100 (exclusive).")

    # ==========================================================
    # 5️⃣ PD → SCORE
    # ==========================================================

    def _pd_to_score(self, pd_percent: float) -> float:

        pd_decimal = pd_percent / 100
        odds = (1 - pd_decimal) / pd_decimal
        score = self.OFFSET + self.FACTOR * np.log(odds)

        return round(score, 0)

    # ==========================================================
    # 6️⃣ SCORE → RATING BAND
    # ==========================================================

    def _score_to_band(self, score: float) -> str:

        for band, lower, upper in self.BAND_STRUCTURE:
            if lower <= score < upper:
                return band

        raise ValueError("Score band mapping failed.")

    # ==========================================================
    # 7️⃣ MAIN PUBLIC METHOD (UPDATED FOR STREAMLIT)
    # ==========================================================

    # def evaluate(self, pd_percent: float, model_name: str = None) -> dict:
    #     """
    #     Main evaluation method.
    #     Returns dictionary output (better for UI rendering).
    #     """

    #     self._validate_pd(pd_percent)

    #     score = self._pd_to_score(pd_percent)
    #     rating = self._score_to_band(score)
    #     decision = self.DECISION_MAP[rating]

    #     return {
    #         "Model": model_name,
    #         "PD (%)": round(pd_percent, 4),
    #         "Score": int(score),
    #         "Rating Band": rating,
    #         "Decision": decision
    #     }


    def evaluate(self, pd_percent: float, model_name: str = None) -> dict:

    self._validate_pd(pd_percent)

    score = self._pd_to_score(pd_percent)
    rating = self._score_to_band(score)
    decision = self.DECISION_MAP[rating]

    return {
        "model": model_name,
        "pd_percent": round(pd_percent, 4),
        "credit_score": int(score),
        "rating_band": rating,
        "decision": decision
    }

    # ==========================================================
    # 8️⃣ OPTIONAL: DATAFRAME FORMAT (If Needed)
    # ==========================================================

    def evaluate_df(self, pd_percent: float, model_name: str = None) -> pd.DataFrame:
        """
        Returns structured DataFrame output (optional usage).
        """

        result_dict = self.evaluate(pd_percent, model_name)

        return pd.DataFrame([result_dict])
