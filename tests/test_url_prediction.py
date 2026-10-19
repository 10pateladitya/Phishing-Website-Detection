from src.phishdetector.feature_extraction.predictor import (
    URLPredictor
)


MODEL_PATH = "artifacts/models/model.pkl"

predictor = URLPredictor(MODEL_PATH)

url = "https://example.com"

result = predictor.predict(url)

print("\nPrediction:")
print(result)