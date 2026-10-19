from phishdetector.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
)
from phishdetector.entity.config_entity import DataValidationConfig
from phishdetector import logger
from phishdetector.utils import read_yaml, write_yaml

import pandas as pd


class DataValidation:
    def __init__(
        self, config: DataValidationConfig, ingestion_artifact: DataIngestionArtifact
    ):
        self.config = config
        self.ingestion_artifact = ingestion_artifact
        self.validation_report = {
            "schema_version": 1.0,
            "validation_date": pd.Timestamp.now().isoformat(),
            "validation_status": "Pending",
            "summary": {
                "total_columns_checked": 0,
                "columns_passed": 0,
                "columns_failed": 0,
            },
            "details": {},
            "errors": [],
        }

    def transform_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transforms column names to lowercase and replaces spaces with underscores.

        Args:
            df (pd.DataFrame): The DataFrame whose column names need to be transformed.

        Returns:
            pd.DataFrame: DataFrame with transformed column names.
        """
        logger.info("Transforming column names...")
        df.columns = [col.lower().replace(" ", "_") for col in df.columns]
        return df

    def validate_schema(self, df: pd.DataFrame) -> bool:
        """
        Validates the schema of the DataFrame against expected criteria.
        - Checks if all expected columns are present.
        - Checks if the column types match expected types.
        - Checks if the columns have only allowed unique values.

        Args:
            df (pd.DataFrame): The DataFrame to validate.

        Returns:
            bool: True if the schema is valid, False otherwise.
        """
        logger.info("Validating schema...")
        try:
            schema = read_yaml(self.config.data_schema_filepath)
            expected_columns = schema.get("columns", {})
            if not expected_columns:
                logger.error("No expected columns found in schema.")
                raise ValueError("Schema validation failed: No expected columns found.")

            # Check schema for each column
            for column_name, column_data in expected_columns.items():
                # Individual column check status
                check_passed = True

                # Check if the column is missing
                if column_name not in df.columns:
                    message = f"Missing expected column: {column_name}"
                    logger.error(message)
                    check_passed = False
                    self.validation_report["errors"].append(message)
                    return False

                # Check if the column type matches expected type
                if column_data.get("data_type") and not pd.api.types.is_dtype_equal(
                    df[column_name].dtype, column_data["data_type"]
                ):
                    message = f"Column '{column_name}' has type {df[column_name].dtype}, expected {column_data['data_type']}"
                    logger.error(message)
                    check_passed = False
                    self.validation_report["errors"].append(message)
                    return False

                # Check if the column has only allowed values
                actual_unique_values = set(df[column_name].unique())
                allowed_unique_values = set(
                    column_data.get("allowed_unique_values", [])
                )
                if not actual_unique_values.issubset(allowed_unique_values):
                    message = (
                        f"Column '{column_name}' has unexpected values: "
                        f"{actual_unique_values}, "
                        f"expected: {allowed_unique_values}"
                    )
                    logger.error(message)
                    check_passed = False
                    self.validation_report["errors"].append(message)
                    return False

                # Update validation report
                self.validation_report["summary"]["total_columns_checked"] += 1

                # Store the validation status for the column
                if column_name not in self.validation_report["details"]:
                    self.validation_report["details"][column_name] = {}

                if check_passed:
                    self.validation_report["summary"]["columns_passed"] += 1
                    self.validation_report["details"][column_name]["status"] = "Passed"
                else:
                    self.validation_report["summary"]["columns_failed"] += 1
                    self.validation_report["details"][column_name]["status"] = "Failed"

            # Finalize validation report and write to file
            self.validation_report["validation_status"] = "Passed"
            write_yaml(
                filepath=self.config.validation_report_filepath,
                content=self.validation_report,
            )
            return True
        except Exception as e:
            logger.error(f"Error validating schema: {e}")
            raise e

    def validate_data(self) -> DataValidationArtifact:
        """Validates the ingested train and test datasets.

        Raises:
            Exception: If any validation step fails, an exception is raised.

        Returns:
            DataValidationArtifact: An artifact containing paths to the validated datasets and the validation report.
        """
        logger.info("Starting data validation process...")
        try:
            # Load the ingested train and test datasets
            train_df = pd.read_csv(self.ingestion_artifact.ingested_train_filepath)
            test_df = pd.read_csv(self.ingestion_artifact.ingested_test_filepath)

            # Validate train dataset
            train_df = self.transform_column_names(train_df)
            train_valid = self.validate_schema(train_df)
            logger.info(f"Train dataset validation status: {train_valid}")

            # Validate test dataset
            test_df = self.transform_column_names(test_df)
            test_valid = self.validate_schema(test_df)
            logger.info(f"Test dataset validation status: {test_valid}")

            # Save validated datasets
            train_df.to_csv(self.config.validated_train_filepath, index=False)
            test_df.to_csv(self.config.validated_test_filepath, index=False)

            logger.info("Data validation completed successfully.")
            return DataValidationArtifact(
                validated_train_filepath=self.config.validated_train_filepath,
                validated_test_filepath=self.config.validated_test_filepath,
                validation_report_filepath=self.config.validation_report_filepath,
            )
        except Exception as e:
            logger.error(f"Data validation failed: {e}")
            raise e
