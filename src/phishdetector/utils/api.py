from phishdetector.utils import load_model, read_yaml
from phishdetector import logger
import pandas as pd
from pathlib import Path

model = load_model(model_path=Path("artifacts/models/model.pkl"))

schema_path = Path("data/schema.yaml")
if not schema_path.exists():
    logger.error(f"Schema file not found at {schema_path}")
    raise FileNotFoundError(f"Schema file not found at {schema_path}")

schema = read_yaml(schema_path)


def get_schema() -> dict:
    try:
        return schema
    except Exception as e:
        logger.error(f"Error fetching schema: {e}")
        raise ValueError("Failed to load schema") from e


def predict_phishing(df: pd.DataFrame) -> list[int]:

    if df.empty:
        raise ValueError(
            "Input DataFrame is empty. Please provide valid data for prediction."
        )
    if "result" in df.columns:
        logger.warning("Dropping 'result' column from input DataFrame")
        df = df.drop(columns=["result"])

    prediction = model.predict(df)
    return prediction
