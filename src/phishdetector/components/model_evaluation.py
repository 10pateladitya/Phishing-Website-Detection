from phishdetector.entity.config_entity import ModelEvaluationConfig
from phishdetector.entity.artifact_entity import ModelEvaluationArtifact
from phishdetector import logger
from phishdetector.utils import write_yaml, load_model

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)

import pandas as pd


class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        """
        Initializes the ModelEvaluation with configuration for model evaluation.

        Args:
            config (ModelEvaluationConfig): An instance of ModelEvaluationConfig that contains paths for model evaluation artifacts.
        """
        self.config = config

    def _get_metrics(self, y_true: pd.Series, y_pred: pd.Series) -> dict:
        """
        Helper method to calculate evaluation metrics.

        Args:
            y_true (pd.Series): True labels.
            y_pred (pd.Series): Predicted labels.

        Returns:
            dict: A dictionary containing evaluation metrics.
        """
        return {
            "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(y_true, y_pred, zero_division=0),
            "recall": recall_score(y_true, y_pred, zero_division=0),
            "f1_score": f1_score(y_true, y_pred, zero_division=0),
            "confusion_matrix": confusion_matrix(y_true, y_pred).tolist(),
        }

    def evaluate_model(self) -> ModelEvaluationArtifact:
        logger.info("Starting model evaluation...")

        try:
            # Load the trained model
            logger.info(
                f"Loading trained model from {self.config.trained_model_filepath}"
            )
            model = load_model(model_path=self.config.trained_model_filepath)

            # Load the testing data
            logger.info(
                f"Loading testing data from {self.config.testing_data_filepath}"
            )
            testing_data = pd.read_csv(self.config.testing_data_filepath)

            # Separate features and target variable
            X_test = testing_data.drop(columns=[self.config.target_column])
            y_test = testing_data[self.config.target_column]

            logger.info("Evaluating model performance...")

            # Make predictions
            logger.info("Making predictions on the test set...")
            y_pred = model.predict(X_test)

            # Calculate evaluation metrics
            logger.info("Calculating evaluation metrics...")
            evaluation_report = self._get_metrics(y_true=y_test, y_pred=y_pred)

            # Save the evaluation report
            logger.info(
                f"Saving evaluation report to {self.config.evaluation_report_filepath}"
            )
            write_yaml(
                filepath=self.config.evaluation_report_filepath,
                content=evaluation_report,
            )

            logger.info("Model evaluation completed successfully.")
            return ModelEvaluationArtifact(
                evaluation_report_filepath=self.config.evaluation_report_filepath
            )
        except Exception as e:
            logger.error(f"Error during model evaluation: {e}")
            raise e
