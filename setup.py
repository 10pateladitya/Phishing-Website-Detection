from setuptools import setup, find_packages
import os


def get_requirements(filepath: str) -> list[str]:
    """
    Returns a list of requirements from the given file.
    """
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r") as file:
        requirements = file.read().splitlines()
    if "-e ." in requirements:
        requirements.remove("-e .")
    return requirements


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


__version__ = "0.1.0"

AUTHOR_NAME = "Sujeet Gund"
AUTHOR_USERNAME = "sujeetgund"
AUTHOR_EMAIL = "sujeetgund@gmail.com"

REPO_NAME = "phishing-website-detection"
SRC_REPO_NAME = "phishdetector"


setup(
    name=SRC_REPO_NAME,
    version=__version__,
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,
    description="A Python package for detecting phishing websites using machine learning.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{AUTHOR_USERNAME}/{REPO_NAME}",
    project_urls={
        "Issues": f"https://github.com/{AUTHOR_USERNAME}/{REPO_NAME}/issues",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
    ],
    install_requires=get_requirements("requirements.txt"),
)
