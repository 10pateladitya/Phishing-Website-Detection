from phishdetector.entity.config_entity import (
    PreprocessingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
)
from phishdetector.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    PreprocessingPipelineArtifact,
)
from phishdetector.components.data_ingestion import DataIngestion
from phishdetector.components.data_validation import DataValidation
from phishdetector import logger


class PreprocessingPipeline:
    def __init__(self, config: PreprocessingPipelineConfig):
        self.config = config

    def _run_data_ingestion(self) -> DataIngestionArtifact:
        """Run the data ingestion process."""
        data_ingestion_config = DataIngestionConfig(config=self.config)
        data_ingestion = DataIngestion(config=data_ingestion_config)
        return data_ingestion.ingest_data()

    def _run_data_validation(
        self, ingestion_artifact: DataIngestionArtifact
    ) -> DataValidationArtifact:
        """Run the data validation process."""
        data_validation_config = DataValidationConfig(config=self.config)
        data_validation = DataValidation(
            config=data_validation_config,
            ingestion_artifact=ingestion_artifact,
        )
        return data_validation.validate_data()

    def run(self) -> PreprocessingPipelineArtifact:
        """Run the entire preprocessing pipeline."""
        try:
            logger.info("Starting the preprocessing pipeline...")

            # Step 1: Data Ingestion
            ingestion_artifact = self._run_data_ingestion()
            logger.info(f"Data ingestion completed. Artifact: {ingestion_artifact}")

            # Step 2: Data Validation
            validation_artifact = self._run_data_validation(ingestion_artifact)
            logger.info(f"Data validation completed. Artifact: {validation_artifact}")

            logger.info("Preprocessing pipeline completed successfully.")
            return PreprocessingPipelineArtifact(
                data_ingestion_artifact=ingestion_artifact,
                data_validation_artifact=validation_artifact,
                preprocessing_report_filepath=self.config.preprocessing_report_filepath,
            )

        except Exception as e:
            logger.error(f"An error occurred during the preprocessing pipeline: {e}")
            raise e
