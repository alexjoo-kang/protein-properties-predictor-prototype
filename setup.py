from setuptools import setup, find_packages

setup(
    name="ProteinPropertiesPredictor",
    version="1.0.0",
    author="Joohyoung Kang",
    author_email="alexkang1014@naver.com",
    description="A package for extracting physicochemical properties from amino acid sequences and predicting structural classification.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/alexjoo-kang/ProteinPropertiesPredictor",
    packages=find_packages(),
    install_requires=[
        "biopython",         # For handling biological sequences
        "numpy",             # For numerical operations
        "pandas",            # For data handling
        "scikit-learn",      # For machine learning preprocessing
        "tensorflow-macos",  # For deep learning model
        "requests",          # For making HTTP requests (e.g., BLASTp)
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Environment :: MacOS X",
    ],
    python_requires=">=3.10",
    platforms=["macOS-arm64"],
    entry_points={
        "console_scripts": [
            "proteinpropertiespredictor=protein_properties_predictor.cli:main",  # CLI-based execution only
        ],
    },
)
