from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from phishdetector.utils.api import predict_phishing, get_schema
from phishdetector import logger
import pandas as pd

router = APIRouter()


@router.get("/schema", description="Get schema for prediction input")
def schema_route():
    """
    Endpoint to get the schema of the prediction input.
    """
    try:
        logger.info("Fetching schema for prediction input")
        schema = get_schema()
        logger.info("Schema fetched successfully")
        return JSONResponse(content=schema, status_code=200)
    except Exception as e:
        logger.error(f"Error fetching schema: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error") from e


@router.post("/predict", description="Predict phishing URLs")
def predict_route(data: UploadFile = File(...)):
    """
    Endpoint to predict phishing URLs.
    """
    try:
        logger.info("Received data for prediction")

        # Check if the uploaded file is a CSV
        if data.content_type != "text/csv":
            raise HTTPException(
                status_code=400, detail="Uploaded file must be a CSV file."
            )

        df = pd.read_csv(data.file)
        predictions = predict_phishing(df=df)
        logger.info("Prediction successful")
        return JSONResponse(
            content={"predictions": predictions.tolist()}, status_code=200
        )
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error") from e
