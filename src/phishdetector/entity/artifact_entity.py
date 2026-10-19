from dataclasses import dataclass
from pathlib import Path


@dataclass
class DataIngestionArtifact:
    """Artifact for data ingestion containing paths for the data source, ingestion report, and ingested datasets."""

    ingested_train_filepath: Path
    ingested_test_filepath: Path


@dataclass
class DataValidationArtifact:
    """Artifact for data validation containing paths for validation report and validated datasets."""

    validation_report_filepath: Path
    validated_train_filepath: Path
    validated_test_filepath: Path


@dataclass
class PreprocessingPipelineArtifact:
    """Artifact for the preprocessing pipeline containing results of data ingestion and validation steps."""

    data_ingestion_artifact: DataIngestionArtifact
    data_validation_artifact: DataValidationArtifact

    def __post_init__(self):
        if not isinstance(self.data_ingestion_artifact, DataIngestionArtifact):
            raise TypeError(
                "data_ingestion_artifact must be of type DataIngestionArtifact"
            )
        if not isinstance(self.data_validation_artifact, DataValidationArtifact):
            raise TypeError(
                "data_validation_artifact must be of type DataValidationArtifact"
            )


@dataclass
class ModelTrainingArtifact:
    """Artifact for model training containing paths for the trained model and training report."""

    trained_model_filepath: Path
    training_report_filepath: Path


@dataclass
class ModelEvaluationArtifact:
    """Artifact for model evaluation containing paths for the evaluation report and metrics."""

    evaluation_report_filepath: Path


@dataclass
class TrainingPipelineArtifact:
    """Artifact for the training pipeline containing results of preprocessing, model training, and evaluation steps."""

    model_training_artifact: ModelTrainingArtifact
    model_evaluation_artifact: ModelEvaluationArtifact

    def __post_init__(self):
        if not isinstance(self.model_training_artifact, ModelTrainingArtifact):
            raise TypeError(
                "model_training_artifact must be of type ModelTrainingArtifact"
            )
        if not isinstance(self.model_evaluation_artifact, ModelEvaluationArtifact):
            raise TypeError(
                "model_evaluation_artifact must be of type ModelEvaluationArtifact"
            )


@dataclass
class ModelPredictionArtifact:
    predictions: list[int]


@dataclass
class InferencePipelineArtifact:
    """Artifact for the inference pipeline containing results of model predictions."""

    model_prediction_artifact: ModelPredictionArtifact

    def __post_init__(self):
        if not isinstance(self.model_prediction_artifact, ModelPredictionArtifact):
            raise TypeError(
                "model_prediction_artifact must be of type ModelPredictionArtifact"
            )
