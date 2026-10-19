from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel

from phishdetector.feature_extraction.predictor import URLPredictor


router = APIRouter()


class URLPredictionRequest(BaseModel):
    url: str


PROJECT_ROOT = Path(__file__).resolve().parents[3]

MODEL_PATH = PROJECT_ROOT / "artifacts" / "models" / "model.pkl"

predictor = URLPredictor(str(MODEL_PATH))


@router.post("/predict-url")
def predict_url(request: URLPredictionRequest):
    result = predictor.predict(request.url)
    return result