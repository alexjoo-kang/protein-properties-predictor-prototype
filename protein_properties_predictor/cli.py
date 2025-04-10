import os
import sys
from .sequence_validator import validate_amino_acid_sequence
from .fasta_parser import parse_fasta
from .feature_extractor import extract_features
from .sequence_search import blastp_search
from .ml_model import ProteinStructureClassifier, generate_training_data

# File to store results
RESULTS_FILE = "results.txt"
MAX_INPUTS = 5  # 🔒 Limit total inputs to 5 (manual + FASTA)

def ensure_model_trained():
    """Ensures a trained model exists; trains a new one if missing."""
    if not os.path.exists("protein_structure_model.keras") or not os.path.exists("scaler.pkl"):
        print("⚠️ No pre-trained model found. Training a new model...")

        # Generate training data and train model
        X_train, y_train = generate_training_data(samples_per_class=30, sequence_length=30)
        classifier = ProteinStructureClassifier()
        classifier.train(X_train, y_train, epochs=300)

def analyze_sequence(sequence):
    """Analyzes the input sequence and prints full results."""
    try:
        ensure_model_trained()
        validated_seq = validate_amino_acid_sequence(sequence)

        # Try to extract features using Biopython
        try:
            features = extract_features(validated_seq)
            biopython_available = True
        except Exception as e:
            features = None
            biopython_available = False
            print("⚠️ Biopython failed to extract features. Skipping physicochemical property analysis.")

        # Try BLASTp
        try:
            print("🔍 Running BLASTp search...")
            blast_results = blastp_search(validated_seq)
        except Exception:
            blast_results = "Unable to retrieve BLASTp results (this may be due to an internet connectivity issue)."

        # Predict structure using the model
        classifier = ProteinStructureClassifier()
        model_prediction = classifier.predict(validated_seq)

        # Output message
        if biopython_available:
            result_output = f"""
✨ Protein Properties Predictor Results ✨

🧬 Given Sequence: {validated_seq}

🏷️ Extracted Features:
Molecular Weight: {features["molecular_weight"]:.2f}
Hydrophobicity: {features["hydrophobicity"]:.3f}
Isoelectric Point: {features["isoelectric_point"]:.2f}
Aromaticity: {features["aromaticity"]:.3f}
Instability Index: {features["instability_index"]:.3f}
Charge at pH 7: {features["charge_at_pH7"]:.3f}
Helix Fraction: {features["helix_fraction"]:.3f}
Sheet Fraction: {features["sheet_fraction"]:.3f}
Coil Fraction: {features["coil_fraction"]:.3f}
Structural Classification: {features["structure_class"]}

🔬 BLASTp Results:
{blast_results}

🧠 Deep Learning Model Prediction:
{model_prediction}

✅ Classification Match: {'Yes' if model_prediction == features["structure_class"] else 'No'}
"""
        else:
            result_output = f"""
✨ Protein Properties Predictor Results ✨

🧬 Given Sequence: {validated_seq}

⚠️ Biopython is not available, so physicochemical properties could not be extracted.

🔬 BLASTp Results:
{blast_results}

🧠 Deep Learning Model Prediction:
{model_prediction}

⚠️ Classification Match cannot be computed because physicochemical properties were not extracted.
"""

        print(result_output)

        with open(RESULTS_FILE, "a") as f:
            f.write(result_output + "\n\n")
        print(f"📄 Results saved to {RESULTS_FILE}\n")

    except Exception as e:
        print(f"❌ Error processing sequence: {sequence} | {e}")

def main():
    """Interactive CLI for analyzing protein sequences."""
    print("\n🔬 Protein Properties Predictor Interactive Mode")
    print("📌 For responsible BLASTp usage, total input sequences (manual + FASTA) are limited to 5.")
    print("🌐 Note: Internet connection is only required for BLASTp search.")
    print("📊 Physicochemical properties and structure prediction will still work offline unless Biopython fails.\n")

    sequences = []

    # Manual sequence input
    while len(sequences) < MAX_INPUTS:
        user_input = input(f"\n🧬 Enter an amino acid sequence ({len(sequences) + 1}/{MAX_INPUTS}) "
                           "or press Enter to provide a FASTA file: ").strip()
        if not user_input:
            break
        sequences.append(user_input)

    # FASTA input
    if len(sequences) < MAX_INPUTS:
        fasta_file = input("📂 Enter FASTA file path (or press Enter to skip): ").strip()
        if fasta_file:
            try:
                parsed_sequence = parse_fasta(fasta_file)
                if isinstance(parsed_sequence, list):
                    if len(parsed_sequence) + len(sequences) > MAX_INPUTS:
                        print(f"❌ Too many sequences. Only {MAX_INPUTS - len(sequences)} more allowed.")
                        parsed_sequence = parsed_sequence[:MAX_INPUTS - len(sequences)]
                    sequences.extend(parsed_sequence)
                else:
                    sequences.append(parsed_sequence)
            except Exception as e:
                print(f"❌ Error reading FASTA file: {e}")

    # Final validation
    if not sequences:
        print("⚠️ No input sequences provided. Exiting.")
        return

    if len(sequences) > MAX_INPUTS:
        print(f"❌ Too many total inputs. Maximum allowed is {MAX_INPUTS}.")
        return

    # Analyze each sequence
    for seq in sequences:
        analyze_sequence(seq)

# Optional cleanup section (commented by default)
def cleanup_model_files():
    """
    Deletes saved model and scaler files after CLI execution.

    💡 If you want to retrain the model every time, 
    uncomment the call to this function below in the __main__ block.
    """
    if os.path.exists("protein_structure_model.keras"):
        os.remove("protein_structure_model.keras")
        print("🗑️ Removed old model file after CLI execution.")
    if os.path.exists("scaler.pkl"):
        os.remove("scaler.pkl")
        print("🗑️ Removed old scaler file after CLI execution.")

if __name__ == "__main__":
    main()

    # 👇 Optional cleanup: Uncomment if you want to force retraining each time
    # cleanup_model_files()