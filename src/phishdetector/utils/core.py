import pickle
from pathlib import Path
from phishdetector import logger


def load_model(model_path: Path):
    """
    Loads a model from the specified path.

    Args:
        model_path (Path): The path to the model file.

    Returns:
        The loaded model.
    """
    if not model_path.exists():
        logger.error(f"Model file not found at {model_path}")
        raise FileNotFoundError(f"Model file not found at {model_path}")

    with open(model_path, "rb") as file:
        model = pickle.load(file)

    return model


def save_model(model, model_path: Path):
    """
    Saves a model to the specified path.

    Args:
        model: The model to save.
        model_path (Path): The path where the model will be saved.
    """
    if not model_path.parent.exists():
        model_path.parent.mkdir(parents=True, exist_ok=True)

    with open(model_path, "wb") as file:
        pickle.dump(model, file)

    logger.info(f"Model saved at {model_path}")


def extract_clf_name(clf_str):
    if not isinstance(clf_str, str):
        clf_str = str(clf_str)
    if "RandomForestClassifier" in clf_str:
        return "RandomForest"
    elif "KNeighborsClassifier" in clf_str:
        return "KNeighbors"
    elif "SVC" in clf_str:
        return "SVC"
    elif "RidgeClassifier" in clf_str:
        return "Ridge"
    elif "LogisticRegression" in clf_str:
        return "Logistic"
    else:
        return "Unknown"
