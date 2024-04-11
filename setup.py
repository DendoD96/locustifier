from setuptools import setup, find_packages
import sample  # Import your library module to access __version__

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="locustifier",
    version=sample.__version__,
    author="Daniele Rossi",
    author_email="daniele.rossi18@studio.unibo.it",
    description="Locustifier is designed to streamline the process of generating Locustfiles from JSON or Yaml specifications.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/DendoD96/locustifier",
    packages=find_packages(),
    license="GPL-3.0-only",
    python_requires=">=3.11",
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL-3.0-only",
    ],
)
