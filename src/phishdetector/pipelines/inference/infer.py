from phishdetector.entity.config_entity import (
    InferencePipelineConfig,
    ModelPredictionConfig,
)
from phishdetector.entity.artifact_entity import (
    ModelPredictionArtifact,
    InferencePipelineArtifact,
)
from phishdetector.components.model_prediction import ModelPrediction
from phishdetector import logger

import pandas as pd


class InferencePipeline:
    def __init__(self, config: InferencePipelineConfig):
        """
        Initializes the InferencePipeline with the given configuration.

        Args:
            config (InferencePipelineConfig): An instance of InferencePipelineConfig that contains paths for inference.
        """
        self.config = config
        self.data = None

    def add_data(self, data: pd.DataFrame):
        self.data = data

    def _run_model_prediction(self) -> ModelPredictionArtifact:
        """
        Runs the model prediction step of the inference pipeline.

        Returns:
            ModelPredictionArtifact: An artifact containing the predictions made by the model.
        """
        model_prediction_config = ModelPredictionConfig(config=self.config)
        model_prediction = ModelPrediction(config=model_prediction_config)
        return model_prediction.predict(data=self.data)

    def run(self) -> InferencePipelineArtifact:

        logger.info("Starting the inference pipeline...")

        try:
            # Check if the input data is provided
            if self.data is None:
                logger.error(
                    "Input data is not provided. Please add data before running the prediction."
                )
                raise ValueError(
                    "Input data is not provided. Please add data before running the prediction."
                )

            # Run model prediction
            model_prediction_artifact = self._run_model_prediction()
            logger.info("Model prediction completed successfully.")

            return InferencePipelineArtifact(
                model_prediction_artifact=model_prediction_artifact
            )
        except Exception as e:
            logger.error(f"An error occurred during the inference pipeline: {e}")
            raise e
