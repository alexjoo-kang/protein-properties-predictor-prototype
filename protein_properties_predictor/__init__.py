"""
Protein Properties Predictor Package

This package provides:
1. **Chemical property analysis** of a given amino acid sequence (e.g., molecular weight, hydrophobicity, isoelectric point, etc.).
2. **Structural classification** of a protein sequence based on extracted features.
3. **Validation of the structural classification** using a deep learning model.

Modules:
- `sequence_validator.py` → Ensures input sequences are valid.
- `fasta_parser.py` → Reads and extracts sequences from FASTA files.
- `feature_extractor.py` → Extracts physicochemical properties and predicts structure.
- `sequence_search.py` → Runs BLASTp similarity searches.
- `ml_model.py` → Validates structural classification using deep learning.
- `cli.py` → Command-line interface for running sequence analysis.

Author: Joohyoung Kang
Version: 1.0.0
"""

# Define package version
__version__ = "1.0.0"
__author__ = "Joohyoung Kang"

# Import essential functions to make them available at the package level
from .sequence_validator import validate_amino_acid_sequence
from .fasta_parser import parse_fasta
from .feature_extractor import extract_features
from .sequence_search import blastp_search
from .ml_model import ProteinStructureClassifier  