from phishdetector.entity.config_entity import ModelTrainingConfig
from phishdetector.entity.artifact_entity import ModelTrainingArtifact
from phishdetector.utils.core import extract_clf_name
from phishdetector.utils import write_yaml
from phishdetector import logger


from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

import pandas as pd
import pickle


class ModelTraining:
    def __init__(self, config: ModelTrainingConfig):
        self.config = config
        self.pipeline = Pipeline(
            [("scaler", StandardScaler()), ("clf", LogisticRegression())]
        )

    def _save_report(self, results_df: pd.DataFrame):
        results_df["param_clf"] = results_df["param_clf"].astype(str)
        # TODO: do it for params column also
        results_df["clf_name"] = results_df["param_clf"].apply(extract_clf_name)

        best_models = results_df.loc[
            results_df.groupby("clf_name")["mean_test_score"].idxmax()
        ].sort_values(by="mean_test_score", ascending=False)

        report = best_models[
            [
                "clf_name",
                "mean_test_score",
                "std_test_score",
                "mean_fit_time",
                "param_clf",
            ]
        ].to_dict(orient="records")

        write_yaml(filepath=self.config.training_report_filepath, content=report)
        return

    def _save_model(self, model):
        with open(self.config.trained_model_filepath, "wb") as f:
            pickle.dump(model, f)
        logger.info(f"Model saved to {self.config.trained_model_filepath}")

    def train_model(self) -> ModelTrainingArtifact:
        logger.info("Starting model training process...")
        try:
            # Load the training data
            train_df = pd.read_csv(self.config.training_data_filepath)

            # Check if target column exists
            if self.config.target_column not in train_df.columns:
                raise ValueError(
                    f"Target column '{self.config.target_column}' not found in training data."
                )

            # Extract features and target variable
            X = train_df.drop(columns=self.config.target_column)
            y = train_df[self.config.target_column]

            # Grid search for hyperparameter tuning
            grid_search = GridSearchCV(
                estimator=self.pipeline,
                param_grid=self.config.param_grid,
                scoring="accuracy",
                cv=5,
                verbose=0,
                n_jobs=-1,
            )

            logger.info("Starting grid search for hyperparameter tuning...")
            grid_search.fit(X, y)

            logger.info(
                f"Best parameters found: {grid_search.best_params_} | Best score: {grid_search.best_score_}"
            )

            # Save the training report
            logger.info("Saving training report...")
            results_df = pd.DataFrame(grid_search.cv_results_)
            self._save_report(results_df)

            # Save the best model
            logger.info("Saving the best model...")
            best_model = grid_search.best_estimator_
            self._save_model(best_model)

            logger.info("Model training completed successfully.")

            return ModelTrainingArtifact(
                trained_model_filepath=self.config.trained_model_filepath,
                training_report_filepath=self.config.training_report_filepath,
            )
        except Exception as e:
            logger.error(f"Error during model training: {e}")
            raise e
