"""
Sequence Validator

This module provides functions to validate amino acid sequences.
- Ensures sequences contain only standard amino acids.
- Converts sequences to uppercase for consistency.
- Can be extended to support non-standard amino acids in the future.
"""

# Define standard 20 amino acids
STANDARD_AMINO_ACIDS = set("ACDEFGHIKLMNPQRSTVWY")

def validate_amino_acid_sequence(seq):
    """
    Validates an amino acid sequence by checking if it contains only standard amino acids.

    :param seq: (str) The amino acid sequence to validate.
    :return: (str) Cleaned sequence if valid.
    :raises ValueError: If the sequence contains invalid characters.
    """
    # Remove whitespace and convert to uppercase
    cleaned_seq = seq.strip().upper()

    # Check if sequence contains only standard amino acids
    invalid_chars = set(cleaned_seq) - STANDARD_AMINO_ACIDS
    if invalid_chars:
        raise ValueError(f"Invalid characters found in sequence: {invalid_chars}")

    return cleaned_seq

def is_valid_sequence(seq):
    """
    Checks whether a sequence is valid without raising an error.

    :param seq: (str) The amino acid sequence.
    :return: (bool) True if valid, False if invalid.
    """
    cleaned_seq = seq.strip().upper()
    return set(cleaned_seq).issubset(STANDARD_AMINO_ACIDS)

if __name__ == "__main__":
    # Test cases
    test_sequences = [
        "MTEYKLVVVGAGGVGKSALTIQLIQNHFVDEYDPTIEDSYRKQ",  # Valid sequence
        "MKTPR-XXX",  # Invalid sequence (contains "- and X")
        "ABCDEFG"  # Invalid sequence (contains non-standard amino acids)
    ]

    for seq in test_sequences:
        try:
            print(f"Validating: {seq}")
            valid_seq = validate_amino_acid_sequence(seq)
            print(f"✅ Valid sequence: {valid_seq}\n")
        except ValueError as e:
            print(f"❌ {e}\n")
