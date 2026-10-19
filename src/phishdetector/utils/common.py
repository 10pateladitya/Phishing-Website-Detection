import yaml
import json
from pathlib import Path
from phishdetector import logger


def read_yaml(filepath: Path):
    """
    Reads a YAML file and returns its content.

    Args:
        filepath (Path): Path to the YAML file.

    Raises:
        FileNotFoundError: If the file does not exist.
        yaml.YAMLError: If the file is not a valid YAML file.

    Returns:
        Any: Parsed content of the YAML file.
    """
    try:
        with open(filepath, "r") as file:
            content = yaml.safe_load(file)
        return content
    except FileNotFoundError as e:
        logger.error(f"The file {filepath} was not found.")
        raise e
    except yaml.YAMLError as e:
        logger.error(f"Failed to parse YAML file {filepath}.")
        raise e


def write_yaml(filepath: Path, content: dict):
    """
    Writes content to a YAML file.

    Args:
        filepath (Path): Path to the YAML file where content will be written.
        content (dict): Content to write to the YAML file.

    Raises:
        Exception: If there is an error writing to the file.
    """
    try:
        with open(filepath, "w") as file:
            yaml.safe_dump(content, file)
        logger.info(f"Successfully wrote to {filepath}.")
    except Exception as e:
        logger.error(f"Failed to write to YAML file {filepath}.")
        raise e


def read_json(filepath: Path):
    """
    Reads a JSON file and returns its content.

    Args:
        filepath (Path): Path to the JSON file.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file is not a valid JSON file.

    Returns:
        Any: Parsed content of the JSON file.
    """
    try:
        with open(filepath, "r") as file:
            content = json.load(file)
        return content
    except FileNotFoundError as e:
        logger.error(f"The file {filepath} was not found.")
        raise e
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON file {filepath}.")
        raise e


def write_json(filepath: Path, content: dict):
    """
    Writes content to a JSON file.

    Args:
        filepath (Path): Path to the JSON file where content will be written.
        content (dict): Content to write to the JSON file.

    Raises:
        Exception: If there is an error writing to the file.
    """
    try:
        with open(filepath, "w") as file:
            json.dump(content, file, indent=4)
        logger.info(f"Successfully wrote to {filepath}.")
    except Exception as e:
        logger.error(f"Failed to write to JSON file {filepath}.")
        raise e
