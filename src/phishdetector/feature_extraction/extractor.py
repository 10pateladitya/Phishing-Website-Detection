from .feature_schema import FEATURE_COLUMNS
from .url_features import extract_url_features


class PhishingFeatureExtractor:

    def extract(self, url: str) -> dict:
        """
        Extract all features required by the model.
        """

        url_features = extract_url_features(url)

        features = {}

        # Start with all required columns.
        for column in FEATURE_COLUMNS:
            features[column] = -1

        # Replace the features we can calculate.
        features.update(url_features)

        return features