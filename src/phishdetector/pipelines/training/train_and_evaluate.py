from phishdetector.entity.config_entity import (
    ModelTrainingConfig,
    ModelEvaluationConfig,
    TrainingPipelineConfig,
)
from phishdetector.entity.artifact_entity import (
    ModelTrainingArtifact,
    ModelEvaluationArtifact,
    TrainingPipelineArtifact,
)

from phishdetector.components.model_training import ModelTraining
from phishdetector.components.model_evaluation import ModelEvaluation
from phishdetector import logger


class TrainingPipeline:
    def __init__(self, config: TrainingPipelineConfig):
        self.config = config

    def _run_model_training(self) -> ModelTrainingArtifact:
        """Run the model training process."""
        model_training_config = ModelTrainingConfig(config=self.config)
        model_training = ModelTraining(config=model_training_config)
        return model_training.train_model()

    def _run_model_evaluation(self) -> ModelEvaluationArtifact:
        """Run the model evaluation process."""
        model_evaluation_config = ModelEvaluationConfig(config=self.config)
        model_evaluation = ModelEvaluation(config=model_evaluation_config)
        return model_evaluation.evaluate_model()

    def run(self) -> TrainingPipelineArtifact:
        logger.info("Starting the training pipeline...")
        try:
            # Step 1: Model Training
            model_training_artifact = self._run_model_training()
            logger.info(
                f"Model training completed. Artifact: {model_training_artifact}"
            )

            # Step 2: Model Evaluation
            model_evaluation_artifact = self._run_model_evaluation()
            logger.info(
                f"Model evaluation completed. Artifact: {model_evaluation_artifact}"
            )

            logger.info("Training pipeline completed successfully.")

            return TrainingPipelineArtifact(
                model_training_artifact=model_training_artifact,
                model_evaluation_artifact=model_evaluation_artifact,
            )
        except Exception as e:
            logger.error(f"An error occurred during the training pipeline: {e}")
            raise e
