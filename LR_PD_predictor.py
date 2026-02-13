# LR_PD_predictor.py

import joblib
import pandas as pd


class LRPDPredictor:

    def __init__(self, model_path="LR_model.joblib"):
        """
        Load the LR model artifact.
        """
        artifact = joblib.load(model_path)

        self.model = artifact["model"]
        self.expected_features = artifact["features"]
        self.expected_dtypes = artifact["feature_dtypes"]
        self.classes = artifact["classes"]
        self.model_version = artifact.get("model_version", "unknown")

        # Validate that class 1 exists
        if 1 not in self.classes:
            raise ValueError("Model does not contain class '1' for default.")

        # Find index of class 1 (default class)
        self.default_class_index = list(self.classes).index(1)

    def _validate_input(self, df: pd.DataFrame):
        """
        Strict validation of feature order, names and datatypes.
        """

        # Check missing features
        missing_features = set(self.expected_features) - set(df.columns)
        if missing_features:
            raise ValueError(f"Missing features: {missing_features}")

        # Check extra features
        extra_features = set(df.columns) - set(self.expected_features)
        if extra_features:
            raise ValueError(f"Unexpected extra features: {extra_features}")

        # Enforce feature order
        df = df[self.expected_features]

        # Enforce dtype casting strictly
        try:
            df = df.astype(self.expected_dtypes)
        except Exception as e:
            raise ValueError(f"Datatype mismatch: {str(e)}")

        return df

    def predict_pd_percent(self, woe_input_df: pd.DataFrame) -> float:
        """
        Predict Probability of Default (PD) in percentage.
        Input must be WOE transformed and aligned.
        """

        if not isinstance(woe_input_df, pd.DataFrame):
            raise ValueError("Input must be a pandas DataFrame.")

        if len(woe_input_df) != 1:
            raise ValueError("Input must contain exactly one row.")

        # Strict validation
        validated_df = self._validate_input(woe_input_df)

        # Predict probabilities
        proba = self.model.predict_proba(validated_df)

        # Extract probability of default class (1)
        pd_probability = proba[0][self.default_class_index]

        # Convert to percentage
        pd_percent = round(pd_probability * 100, 4)

        return pd_percent
