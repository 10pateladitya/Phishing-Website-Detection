from phishdetector.entity.config_entity import ModelPredictionConfig
from phishdetector.entity.artifact_entity import ModelPredictionArtifact
from phishdetector.utils import load_model
from phishdetector import logger


import pandas as pd


class ModelPrediction:
    def __init__(self, config: ModelPredictionConfig):
        self.config = config
        self.model = load_model(self.config.trained_model_filepath)

    def predict(self, data: pd.DataFrame) -> ModelPredictionArtifact:
        """Make predictions using the trained model.
        This method takes a DataFrame as input, validates it, and uses the loaded model to make predictions.

        Args:
            data (pd.DataFrame): The input data for making predictions. It should be preprocessed and ready for the model.

        Raises:
            Exception: If there is an error during the prediction process, it will be logged and raised.

        Returns:
            ModelPredictionArtifact: An artifact containing the predictions made by the model.
        """
        try:
            # validate data

            # Make predictions
            predictions = self.model.predict(data)

            return ModelPredictionArtifact(predictions=predictions)
        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            raise e
