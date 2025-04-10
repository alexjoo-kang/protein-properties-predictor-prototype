"""
Feature Extractor for Protein Structural Classification

This module extracts key physicochemical properties from an amino acid sequence. 
The extracted features can be used for general protein analysis and machine learning models. 

Additionally, this module classifies the sequence into one of the five structural categories 
based on secondary structure content:

- Dominantly α-helical Proteins (H ≥ 0.5, S < 0.3) → Mostly α-helices
- Dominantly β-sheet Proteins (S ≥ 0.5, H < 0.3) → Mostly β-sheets
- α/β Proteins (0.3 ≤ H ≤ 0.5 and 0.3 ≤ S ≤ 0.5) → Intermixed α-helices & β-sheets
- α+β Proteins (H > 0.3 and S > 0.3, but not in α/β range) → Segregated α and β regions
- Unstructured / Coil-Dominant Proteins (H < 0.3 and S < 0.3) → Mostly random coils

These structural classifications are based on secondary structure predictions and 
are useful for bioinformatics and structural biology research.

Dependencies:
- Biopython (install using `pip install biopython`)
"""

from Bio.SeqUtils.ProtParam import ProteinAnalysis
from .sequence_validator import validate_amino_acid_sequence

def extract_features(sequence):
    """
    Extracts physicochemical properties from an amino acid sequence and classifies its structure.

    The extracted properties include:
    - Molecular weight
    - Hydrophobicity (GRAVY score)
    - Isoelectric point (pI)
    - Aromaticity (fraction of aromatic amino acids)
    - Instability index (predicts protein stability)
    - Net charge at pH 7.0
    - Helix fraction (α-helices)
    - Sheet fraction (β-sheets)
    - Coil fraction (random coils)
    - Sequence length

    These properties can be used for general protein analysis, machine learning models, 
    and protein structure classification.

    :param sequence: (str) Amino acid sequence.
    :return: (dict) Dictionary containing extracted features and structural classification.
    :raises ValueError: If the sequence is invalid.
    """
    # Validate the sequence
    validated_seq = validate_amino_acid_sequence(sequence)

    # Analyze sequence properties
    analyzed_seq = ProteinAnalysis(validated_seq)

    # Extract secondary structure fractions
    helix_fraction, sheet_fraction, coil_fraction = analyzed_seq.secondary_structure_fraction()

    # Determine structural classification
    if helix_fraction >= 0.5 and sheet_fraction < 0.3:
        structure_class = "Dominantly α-helical"
    elif sheet_fraction >= 0.5 and helix_fraction < 0.3:
        structure_class = "Dominantly β-sheet"
    elif 0.3 <= helix_fraction <= 0.5 and 0.3 <= sheet_fraction <= 0.5:
        structure_class = "α/β"
    elif helix_fraction > 0.3 and sheet_fraction > 0.3:
        structure_class = "α+β"
    else:
        structure_class = "Unstructured / Coil-Dominant"

    # Store extracted features in a dictionary
    features = {
        "molecular_weight": analyzed_seq.molecular_weight(),
        "hydrophobicity": analyzed_seq.gravy(),
        "isoelectric_point": analyzed_seq.isoelectric_point(),
        "aromaticity": analyzed_seq.aromaticity(),
        "instability_index": analyzed_seq.instability_index(),
        "charge_at_pH7": analyzed_seq.charge_at_pH(7.0),
        "helix_fraction": helix_fraction,
        "sheet_fraction": sheet_fraction,
        "coil_fraction": coil_fraction,
        "sequence_length": len(validated_seq),
        "structure_class": structure_class,  # Structural classification
    }

    return features

if __name__ == "__main__":
    # Test case: Extract features from a sample sequence
    test_sequence = "MTEYKLVVVGAGGVGKSALTIQLIQNHFVDEYDPTIEDSYRKQ"

    try:
        print(f"Extracting features for: {test_sequence}")
        features = extract_features(test_sequence)
        print(f"✅ Extracted Features: {features}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")
