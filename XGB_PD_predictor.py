# XGB_PD_predictor.py

import joblib
import pandas as pd
import numpy as np


class XGBPDPredictor:

    def __init__(self, model_path: str):
        """
        Loads trained XGB model artifact.
        """
        artifact = joblib.load(model_path)

        if "model" not in artifact:
            raise ValueError("Invalid model artifact: missing 'model' key.")

        if "features" not in artifact:
            raise ValueError("Invalid model artifact: missing 'features' key.")

        if "feature_dtypes" not in artifact:
            raise ValueError("Invalid model artifact: missing 'feature_dtypes' key.")

        self.model = artifact["model"]
        self.expected_features = artifact["features"]
        self.expected_dtypes = artifact["feature_dtypes"]
        self.model_version = artifact.get("model_version", "unknown")

    # =====================================================
    # INTERNAL VALIDATION
    # =====================================================

    def _validate_input_dataframe(self, df: pd.DataFrame):

        if not isinstance(df, pd.DataFrame):
            raise ValueError("Input must be a pandas DataFrame.")

        if df.shape[0] != 1:
            raise ValueError("Input DataFrame must contain exactly 1 row.")

        # Check feature names match exactly
        input_features = list(df.columns)

        if input_features != self.expected_features:
            raise ValueError(
                f"Feature order mismatch.\n"
                f"Expected: {self.expected_features}\n"
                f"Received: {input_features}"
            )

        # Check missing values
        if df.isnull().any().any():
            raise ValueError("Input contains missing values.")

        # Enforce dtype casting
        for col, dtype in self.expected_dtypes.items():
            try:
                df[col] = df[col].astype(dtype)
            except Exception:
                raise ValueError(f"Failed dtype casting for feature: {col}")

        return df

    # =====================================================
    # PREDICT PD %
    # =====================================================

    def predict_pd_percent(self, df: pd.DataFrame) -> float:
        """
        Returns PD in percentage format (e.g., 7.23)
        """

        df = self._validate_input_dataframe(df)

        try:
            proba = self.model.predict_proba(df)[:, 1]
        except Exception as e:
            raise ValueError(f"Model prediction failed: {str(e)}")

        pd_value = float(proba[0]) * 100

        return round(pd_value, 4)

    # =====================================================
    # OPTIONAL RAW PROBABILITY (0–1)
    # =====================================================

    def predict_pd_raw(self, df: pd.DataFrame) -> float:
        df = self._validate_input_dataframe(df)
        proba = self.model.predict_proba(df)[:, 1]
        return float(proba[0])
