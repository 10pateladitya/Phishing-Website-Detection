import joblib
import pandas as pd

from .extractor import PhishingFeatureExtractor
from .feature_schema import FEATURE_COLUMNS


class URLPredictor:

    def __init__(self, model_path):
        self.model = joblib.load(model_path)
        self.extractor = PhishingFeatureExtractor()

    def predict(self, url: str):

        features = self.extractor.extract(url)

        df = pd.DataFrame(
            [features],
            columns=FEATURE_COLUMNS
        )

        prediction = self.model.predict(df)[0]

        return {
            "url": url,
            "prediction": int(prediction),
            "result": (
                "phishing"
                if prediction == 1
                else "legitimate"
            ),
            "features": features
        }