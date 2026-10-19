from pathlib import Path

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier


class PhishDetectorConfig:
    """Base configuration for the PhishDetector project."""

    def __init__(self):
        """Initializes the PhishDetectorConfig with paths for the main configuration."""
        self.artifacts_dir = Path("artifacts")
        self.feature_store_dir = self.artifacts_dir / "feature_store"
        self.model_dir = self.artifacts_dir / "models"
        self.reports_dir = self.artifacts_dir / "reports"
        self.data_source = Path("data") / "phishingData.csv"
        self.data_schema = Path("data") / "schema.yaml"
        self._create_base_dirs()

    def _create_base_dirs(self):
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)
        self.feature_store_dir.mkdir(parents=True, exist_ok=True)
        self.model_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)


class PreprocessingPipelineConfig(PhishDetectorConfig):
    def __init__(self):
        """Initializes the PreprocessingPipelineConfig with paths for preprocessing pipeline."""
        super().__init__()
        self.preprocessing_report_filepath = (
            self.reports_dir / "preprocessing_report.json"
        )
        self._create_preprocessing_dirs()

    def _create_preprocessing_dirs(self):
        self.preprocessing_report_filepath.parent.mkdir(parents=True, exist_ok=True)


class DataIngestionConfig:
    def __init__(self, config: PreprocessingPipelineConfig):
        """
        Initializes the DataIngestionConfig with paths for data ingestion.

        Args:
            config (PreprocessingPipelineConfig): An instance of PreprocessingPipelineConfig that contains base directories for artifacts and feature store.
        """
        self.config = config
        self.data_source_filepath = config.data_source
        self.ingestion_report_filepath = (
            config.reports_dir / "data_ingestion_report.json"
        )
        self.ingested_train_filepath = (
            config.feature_store_dir / "ingested" / "train.csv"
        )
        self.ingested_test_filepath = config.feature_store_dir / "ingested" / "test.csv"
        self._create_ingested_dirs()

    def _create_ingested_dirs(self):
        (self.ingested_train_filepath.parent).mkdir(parents=True, exist_ok=True)
        (self.ingested_test_filepath.parent).mkdir(parents=True, exist_ok=True)


class DataValidationConfig:
    def __init__(self, config: PreprocessingPipelineConfig):
        """
        Initializes the DataValidationConfig with paths for data validation.

        Args:
            config (PreprocessingPipelineConfig): An instance of PreprocessingPipelineConfig that contains base directories for artifacts and feature store.
        """
        self.config = config
        self.data_schema_filepath = config.data_schema
        self.validation_report_filepath = (
            config.reports_dir / "data_validation_report.yaml"
        )
        self.validated_train_filepath = (
            config.feature_store_dir / "validated" / "validated_train.csv"
        )
        self.validated_test_filepath = (
            config.feature_store_dir / "validated" / "validated_test.csv"
        )
        self._create_validated_dirs()

    def _create_validated_dirs(self):
        (self.validated_train_filepath.parent).mkdir(parents=True, exist_ok=True)
        (self.validated_test_filepath.parent).mkdir(parents=True, exist_ok=True)


class TrainingPipelineConfig(PhishDetectorConfig):
    """Configuration for training pipeline in the PhishDetector project."""

    def __init__(self):
        """Initializes the TrainingPipelineConfig with paths for training pipeline."""
        super().__init__()
        self.training_data_filepath = (
            self.feature_store_dir / "validated" / "validated_train.csv"
        )
        self.testing_data_filepath = (
            self.feature_store_dir / "validated" / "validated_test.csv"
        )
        self.trained_model_filepath = self.model_dir / "model.pkl"
        self.training_report_filepath = self.reports_dir / "training_report.yaml"
        self.evaluation_report_filepath = self.reports_dir / "evaluation_report.yaml"
        self.target_column = "result"
        self._create_training_dirs()

    def _create_training_dirs(self):
        self.trained_model_filepath.parent.mkdir(parents=True, exist_ok=True)
        self.training_report_filepath.parent.mkdir(parents=True, exist_ok=True)
        self.evaluation_report_filepath.parent.mkdir(parents=True, exist_ok=True)


class ModelTrainingConfig:
    """Configuration for model training in the PhishDetector project."""

    def __init__(self, config: TrainingPipelineConfig):
        """
        Initializes the ModelTrainingConfig with paths for model training.

        Args:
            config (TrainingPipelineConfig): An instance of TrainingPipelineConfig that contains base directories for models and reports.
        """
        self.config = config
        self.target_column = config.target_column
        self.training_data_filepath = config.training_data_filepath
        self.trained_model_filepath = config.trained_model_filepath
        self.training_report_filepath = config.training_report_filepath
        self.param_grid = [
            # Random Forest (no scaling)
            {
                "scaler": [None],
                "clf": [RandomForestClassifier(random_state=42)],
                "clf__n_estimators": [100, 200],
                "clf__max_depth": [None, 10, 20],
                "clf__min_samples_split": [2, 5],
                "clf__min_samples_leaf": [1, 2],
                "clf__max_features": ["sqrt", "log2"],
            },
            # Logistic Regression (scaling required)
            {
                "scaler": [StandardScaler()],
                "clf": [LogisticRegression(max_iter=1000, random_state=42)],
                "clf__C": [0.1, 1, 10],
                "clf__penalty": ["l2"],
                "clf__solver": ["liblinear", "saga"],
            },
            # Ridge Classifier (no scaling needed, but can help)
            {
                "scaler": [None, StandardScaler()],
                "clf": [RidgeClassifier(random_state=42)],
                "clf__alpha": [0.1, 1, 10],
            },
            # SVM (scaling required)
            {
                "scaler": [StandardScaler()],
                "clf": [SVC(probability=True, random_state=42)],
                "clf__C": [0.1, 1, 10],
                "clf__kernel": ["linear", "rbf"],
                "clf__gamma": ["scale", "auto"],
            },
            # KNN (scaling required)
            {
                "scaler": [StandardScaler()],
                "clf": [KNeighborsClassifier()],
                "clf__n_neighbors": [3, 5, 7],
                "clf__weights": ["uniform", "distance"],
                "clf__p": [1, 2],  # 1=Manhattan, 2=Euclidean
            },
        ]


class ModelEvaluationConfig:
    def __init__(self, config: TrainingPipelineConfig):
        """
        Initializes the ModelEvaluationConfig with paths for model evaluation.

        Args:
            config (TrainingPipelineConfig): An instance of TrainingPipelineConfig that contains base directories for models and reports.
        """
        self.config = config
        self.target_column = config.target_column
        self.evaluation_report_filepath = config.evaluation_report_filepath
        self.trained_model_filepath = config.trained_model_filepath
        self.testing_data_filepath = config.testing_data_filepath
        self._create_evaluation_dirs()

    def _create_evaluation_dirs(self):
        self.evaluation_report_filepath.parent.mkdir(parents=True, exist_ok=True)
        self.trained_model_filepath.parent.mkdir(parents=True, exist_ok=True)
        self.testing_data_filepath.parent.mkdir(parents=True, exist_ok=True)


class InferencePipelineConfig(PhishDetectorConfig):
    """Configuration for inference pipeline in the PhishDetector project."""

    def __init__(self):
        """Initializes the InferencePipelineConfig with paths for inference pipeline."""
        super().__init__()
        self.trained_model_filepath = self.model_dir / "model.pkl"


class ModelPredictionConfig:
    """Configuration for model prediction in the PhishDetector project."""

    def __init__(self, config: InferencePipelineConfig):
        """
        Initializes the ModelPredictionConfig with paths for model prediction.

        Args:
            config (InferencePipelineConfig): An instance of InferencePipelineConfig that contains base directories for models.
        """
        self.config = config
        self.trained_model_filepath = config.trained_model_filepath
        self.input_data_filepath = Path("data") / "input_data.csv"
        self.prediction_report_filepath = config.reports_dir / "prediction_report.json"
        self._create_prediction_dirs()

    def _create_prediction_dirs(self):
        self.prediction_report_filepath.parent.mkdir(parents=True, exist_ok=True)
        self.input_data_filepath.parent.mkdir(parents=True, exist_ok=True)
