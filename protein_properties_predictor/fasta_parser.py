
"""
FASTA File Parser

This module provides functions to:
- Read and parse protein sequences from a FASTA file.
- Extract only the amino acid sequence, ignoring headers.
- Validate sequences using `sequence_validator.py`.
"""

from .sequence_validator import validate_amino_acid_sequence

def parse_fasta(file_path):
    """
    Parses a FASTA file and extracts the amino acid sequence.

    :param file_path: (str) Path to the FASTA file.
    :return: (str) Cleaned amino acid sequence.
    :raises FileNotFoundError: If the file does not exist.
    :raises ValueError: If the sequence contains invalid characters.
    """
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Remove header lines (lines starting with ">")
        sequence_lines = [line.strip() for line in lines if not line.startswith(">")]

        # Join all lines to form a continuous sequence
        raw_sequence = "".join(sequence_lines)

        # Validate sequence using sequence_validator
        cleaned_sequence = validate_amino_acid_sequence(raw_sequence)

        return cleaned_sequence

    except FileNotFoundError:
        raise FileNotFoundError(f"Error: The file '{file_path}' was not found.")
    
    except Exception as e:
        raise ValueError(f"Error while parsing FASTA file: {str(e)}")

if __name__ == "__main__":
    # Test case: Parse a sample FASTA file
    test_fasta_path = "/path/to/test.fasta"

    try:
        print(f"Parsing file: {test_fasta_path}")
        sequence = parse_fasta(test_fasta_path)
        print(f"✅ Extracted Sequence: {sequence}\n")
    except Exception as e:
        print(f"❌ {e}\n")
