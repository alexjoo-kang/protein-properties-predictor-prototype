# protein-properties-predictor-prototype

## 🤝 Acknowledgment

This project was created with significant assistance from ChatGPT (OpenAI), which helped in:

    Designing the code architecture

    Writing and debugging Python scripts

    Structuring the machine learning pipeline

    Generating documentation, including this README

    Clarifying biological and computational concepts throughout the development process

I'm grateful for how this AI tool accelerated learning and supported the creative development of this tutorial project.

## 🔍 About Structural Classification

⚠️ Important Note on Structural Categories and Thresholds

This tool currently classifies protein structures into five broad categories based on user-defined thresholds for α-helix (H) and β-sheet (S) content:

    Dominantly α-helical Proteins (H ≥ 0.5, S < 0.3) → Mostly α-helices

    Dominantly β-sheet Proteins (S ≥ 0.5, H < 0.3) → Mostly β-sheets

    α/β Proteins (0.3 ≤ H ≤ 0.5 and 0.3 ≤ S ≤ 0.5) → Intermixed α-helices & β-sheets

    α+β Proteins (H > 0.3 and S > 0.3, but not in α/β range) → Segregated α and β regions

    Unstructured / Coil-Dominant Proteins (H < 0.3 and S < 0.3) → Mostly random coils

These thresholds and class names were chosen for tutorial and demonstration purposes and are not based on standardized structural classification schemes (thus named -prototype).

🔧 If you are using this tool for real biological analysis, we recommend:

    Referencing authoritative structural classification databases or literature.

    Modifying the thresholds and class labels accordingly in the source code (feature_extractor.py, ml_model.py).

    Optionally retraining the deep learning model to reflect updated class definitions.


## 🧬 Overview

**protein-properties-predicor-prototype** is a Python tool that extracts physicochemical properties from amino acid sequences and predicts their structural class using a deep learning model.

This package was built to provide structural classification **even when key tools like Biopython are not available**. It works best when online (to access BLASTp), but can still function in offline environments.  
> 🔁 If Biopython fails, BLASTp will still work (as long as internet is available) because BLASTp is handled independently.

---

⚠️ Platform Note: This package is currently supported only on Apple Silicon (M1/M2) Macs due to its use of tensorflow-macos.

## 🚀 Features

- ✅ **Physicochemical Property Extraction**
  - Molecular weight
  - Hydrophobicity
  - Isoelectric point
  - Aromaticity
  - Instability index
  - Charge at pH 7
  - Helix, sheet, and coil fractions
- 🔬 **BLASTp Similarity Search**
  - Finds similar proteins using BLASTp (requires internet)
- 🧠 **Deep Learning Structural Prediction**
  - Predicts one of five broad protein structure types using only the sequence:
    - Dominantly α-helical
    - Dominantly β-sheet
    - α/β
    - α+β
    - Unstructured / Coil-Dominant

---

## 🧠 How the Deep Learning Model Works (Beginner-Friendly)

The program includes a simple yet powerful deep learning model that can **predict the rough 3D structure** of a protein from its sequence — **without needing BLAST or external data**.

### ❓ What Is Deep Learning?

Deep learning is a type of machine learning that uses "neural networks" — layers of virtual "neurons" that learn patterns in data. Think of it like how your brain learns to recognize patterns in faces or voices. The model learns from lots of example data and applies that knowledge to make predictions on new inputs.

### 🔡 Input: What Goes Into the Model?

Each amino acid sequence is turned into a **20-number vector** that counts how often each of the 20 standard amino acids appears (called amino acid composition).

So, the input to the model looks like this:

```
[Frequency of A, Frequency of C, Frequency of D, ..., Frequency of Y]
```

These values are then **normalized** so that the model can learn more effectively.

---

### 🧱 Model Architecture (Simple Neural Network)

The deep learning model is made up of multiple layers of "neurons" — each layer transforms the input a little bit more to get closer to the final answer.

Here’s the layout:

1. **Input Layer (20 values)** — One for each amino acid type
2. **Hidden Layer 1**: 128 neurons + ReLU activation
3. **Dropout Layer**: Randomly turns off some neurons to prevent overfitting
4. **Hidden Layer 2**: 64 neurons + ReLU
5. **Dropout Layer**
6. **Hidden Layer 3**: 32 neurons + ReLU
7. **Hidden Layer 4**: 16 neurons + ReLU
8. **Output Layer**: 5 neurons (one for each structural class) + Softmax activation  
   → This outputs the **probability of each structure type**, and the one with the highest score is the predicted class.

---

### 🧪 How It Was Trained

- Each class ("α-helical", "β-sheet", etc.) is trained with **30 sample sequences**
- The training data is generated synthetically using known relationships between sequence and structure
- The model was trained for **300 cycles (epochs)** using the **Adam optimizer**, which helps it gradually improve
- After training, the model is saved and used directly for predictions

---

### 🎯 Why Use a Deep Learning Model?

- You can still get predictions **without internet** or external databases
- It works even if **Biopython is unavailable**
- Fast and light — doesn't require a GPU or large computing resources

---

## 📥 Installation Guide

### Step 1: Clone This Repository

```bash
git clone https://github.com/alexjoo-kang/protein-properties-predictor-prototype.git
cd protein-properties-predictor-prototype
```

---

### Step 2: Create Conda Environment (✅ Preferred Method)

```bash
conda env create -f protein_env.yml
conda activate protein_env
```

This ensures all required dependencies (like `tensorflow-macos`, `biopython`, `pandas`, etc.) are installed correctly on **macOS**.

---

### Step 3: Install the Package Locally

After activating the environment, install the package in **editable mode**:

```bash
pip install -e .
```

This enables:
- CLI usage with the command `proteinpropertiespredictor`
- Real-time updates as you modify the source code

---

### 💡 Alternative (Without Conda)

You can install dependencies manually using `pip` with:

```bash
pip install -e .
```

But using the Conda environment (`protein_env.yml`) is recommended for compatibility and ease of setup.

---

## 🧪 Usage

Run the CLI tool after installation:

```bash
proteinpropertiespredictor
```

You’ll see an interactive prompt:

```
🔬 Protein Properties Predictor Interactive Mode
📌 For responsible BLASTp usage, total input sequences (manual + FASTA) are limited to 5.
🌐 Note: Internet connection is only required for BLASTp search.
📊 Physicochemical properties and structure prediction will still work offline unless Biopython fails.

🧬 Enter an amino acid sequence (1/5) or press Enter to provide a FASTA file:
```

### ▶️ Example Test Sequence

You can paste the following test sequence when prompted:

```
MTEYKLVVVGAGGVGKSALTIQLIQNHFVDEYDPTIEDSYRKQ
```

Or press **Enter** to skip manual input and upload a FASTA file instead.

---

## 📦 Training Info

The deep learning model is **not pre-trained by default** — instead, it will automatically train itself the first time you run the program.  
During this first run, the following files will be generated and saved for reuse:

- `training_data.csv` — training dataset
- `scaler.pkl` — Feature normalizer (StandardScaler)
- `protein_structure_model.keras` — Trained deep learning model

Once these files are created, the tool will use them for all future predictions to speed up execution.

> 🔁 **Want to retrain the model from scratch?**  
> Simply uncomment the "cleanup section" in `cli.py` to remove the saved files and regenerate everything.



---

## 🧾 Example Output Scenarios

### ✅ 1. Everything Works (Online + Biopython)

```
✨ Protein Properties Predictor Results ✨

🧬 Given Sequence: MTEYKLVVVGAGGVGKSALTIQLIQNHFVDEYDPTIEDSYRKQ

🏷️ Extracted Features:
Molecular Weight: 4814.38
Hydrophobicity: -0.256
Isoelectric Point: 4.95
Aromaticity: 0.093
Instability Index: 26.916
Charge at pH 7: -2.407
Helix Fraction: 0.279
Sheet Fraction: 0.256
Coil Fraction: 0.419
Structural Classification: Unstructured / Coil-Dominant

🔬 BLASTp Results:
[('emb|CAA51689.1|', '223'), ('gb|KAL1765642.1|', '226'), ('prf||1905199A', '224'), ('gb|ACI62841.1|', '224'), ('ref|XP_016396535.1|', '224')]

🧠 Deep Learning Model Prediction:
Unstructured / Coil-Dominant

✅ Classification Match: Yes

📄 Results saved to results.txt
```

---

### 🌐 2. Offline Mode (BLASTp Fails, Biopython Works)

```
🔍 Running BLASTp search...
⚠️ Unable to retrieve BLASTp results (this may be due to an internet connectivity issue).

✨ Protein Properties Predictor Results ✨

🧬 Given Sequence: MTEYKLVVVGAGGVGKSALTIQLIQNHFVDEYDPTIEDSYRKQ

🏷️ Extracted Features:
Molecular Weight: 4814.38
Hydrophobicity: -0.256
Isoelectric Point: 4.95
Aromaticity: 0.093
Instability Index: 26.916
Charge at pH 7: -2.407
Helix Fraction: 0.279
Sheet Fraction: 0.256
Coil Fraction: 0.419
Structural Classification: Unstructured / Coil-Dominant

🔬 BLASTp Results:
Unable to retrieve BLASTp results (this may be due to an internet connectivity issue).

🧠 Deep Learning Model Prediction:
Unstructured / Coil-Dominant

✅ Classification Match: Yes
```

---

### ⚠️ 3. Biopython Not Available (BLASTp Still Works)

```
⚠️ Biopython is not available. Skipping physicochemical feature extraction and classification match.

🔬 BLASTp Results:
[('emb|CAA51689.1|', '223'), ('gb|KAL1765642.1|', '226'), ('prf||1905199A', '224'), ('gb|ACI62841.1|', '224'), ('ref|XP_016396535.1|', '224')]

🧠 Deep Learning Model Prediction:
Unstructured / Coil-Dominant

⚠️ Classification Match cannot be computed because physicochemical properties were not extracted.
```

---

## 🤝 Contributing

Contributions are welcome!  
Feel free to fork the repo, submit issues, or create pull requests.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👤 Author

**Joohyoung Kang**  
📧 alexkang1014@naver.com  
🐙 [GitHub](https://github.com/alexjoo-kang)
