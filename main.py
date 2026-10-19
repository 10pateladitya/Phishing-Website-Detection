from phishdetector.pipelines.preprocessing import PreprocessingPipeline
from phishdetector.pipelines.training import TrainingPipeline
from phishdetector.pipelines.inference import InferencePipeline
from phishdetector.entity.config_entity import (
    PreprocessingPipelineConfig,
    TrainingPipelineConfig,
    InferencePipelineConfig,
)
from phishdetector.entity.artifact_entity import (
    PreprocessingPipelineArtifact,
    TrainingPipelineArtifact,
    ModelPredictionArtifact,
)
from phishdetector import logger

import pandas as pd


def run_preprocessing(
    config: PreprocessingPipelineConfig,
) -> PreprocessingPipelineArtifact:
    """
    Run the preprocessing pipeline with the given configuration.

    Args:
        config (PreprocessingPipelineConfig): Configuration for the preprocessing pipeline.

    Returns:
        PreprocessingPipelineArtifact: The artifact containing results of the preprocessing steps.
    """
    preprocessing = PreprocessingPipeline(config=config)
    return preprocessing.run()


def run_training(config: TrainingPipelineConfig) -> TrainingPipelineArtifact:
    """
    Run the training pipeline with the given configuration.

    Args:
        config (TrainingPipelineConfig): Configuration for the training pipeline.

    Returns:
        TrainingPipelineArtifact: The artifact containing results of the training steps.
    """
    training = TrainingPipeline(config=config)
    return training.run()


def run_inference(
    config: InferencePipelineConfig, data: pd.DataFrame
) -> ModelPredictionArtifact:
    """
    Run the inference pipeline with the given configuration.

    Args:
        config (InferencePipelineConfig): Configuration for the inference pipeline.
        data (pd.DataFrame): The input data for making predictions. It should be preprocessed and ready for the model.

    Returns:
        ModelPredictionArtifact: The artifact containing predictions made by the model.
    """
    inference = InferencePipeline(config=config)
    inference.add_data(data=data)
    return inference.run()


def main():
    # run_preprocessing(config=PreprocessingPipelineConfig())
    # run_training(config=TrainingPipelineConfig())

    # Example data for inference
    sample_data = pd.read_csv(
        "./artifacts/feature_store/validated/validated_test.csv"
    ).sample(3)
    
    # Original results
    logger.info(f"Original results: {sample_data['result'].to_list()}")
    predictions = run_inference(config=InferencePipelineConfig(), data=sample_data.drop("result", axis=1))
    print(predictions)


if __name__ == "__main__":
    main()
