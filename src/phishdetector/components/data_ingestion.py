from phishdetector.entity.artifact_entity import DataIngestionArtifact
from phishdetector.entity.config_entity import DataIngestionConfig
from phishdetector import logger

import pandas as pd
from sklearn.model_selection import train_test_split


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        """Initializes the DataIngestion component with the provided configuration.

        Args:
            config (DataIngestionConfig): An instance of DataIngestionConfig that contains paths for data ingestion.
        """
        self.config = config

    def split_data(self, df: pd.DataFrame):
        try:
            train_df, test_df = train_test_split(
                df,
                test_size=0.2,
                random_state=42,
                stratify=df["Result"] if "Result" in df.columns else None,
            )

            logger.info(
                f"Data split into train and test sets with sizes: {len(train_df)} and {len(test_df)} respectively."
            )

            logger.info("Exporting train and test datasets to CSV files.")
            train_df.to_csv(self.config.ingested_train_filepath, index=False)
            test_df.to_csv(self.config.ingested_test_filepath, index=False)
            return
        except Exception as e:
            logger.error(f"Error during data splitting")
            raise Exception(f"Error during data splitting: {e}")

    def ingest_data(self) -> DataIngestionArtifact:
        """Ingests data from the source, splits it into train and test sets, and saves them to specified file paths.

        Raises:
            Exception: If there is an error during the data ingestion process.

        Returns:
            DataIngestionArtifact: An artifact containing the file paths of the train and test datasets.
        """
        logger.info("Starting data ingestion process...")
        try:
            raw_df = pd.read_csv(self.config.data_source_filepath)
            self.split_data(raw_df)
            logger.info("Data ingestion completed successfully.")

            return DataIngestionArtifact(
                ingested_train_filepath=self.config.ingested_train_filepath,
                ingested_test_filepath=self.config.ingested_test_filepath,
            )

        except Exception as e:
            raise Exception(f"Error in ingesting data: {e}")
