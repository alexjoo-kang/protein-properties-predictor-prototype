import os
import joblib
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import StandardScaler, LabelEncoder
from .feature_extractor import extract_features
from .sequence_validator import validate_amino_acid_sequence
import numpy as np
import random
import pandas as pd

# Define standard amino acids
AMINO_ACIDS = "ACDEFGHIKLMNPQRSTVWY"

# Define structural classes
STRUCTURE_CLASSES = ["Dominantly α-helical", "Dominantly β-sheet", "α/β", "α+β", "Unstructured / Coil-Dominant"]

# Function to generate random sequences of length 30
def generate_random_sequence(length=30):
    """Generates a random amino acid sequence."""
    return ''.join(random.choices(AMINO_ACIDS, k=length))

# Function to generate BALANCED training data
def generate_training_data(samples_per_class=20, sequence_length=30, save_csv=True):
    """Generates a dataset of amino acid sequences and their predicted structural classes."""
    print("🔄 Generating training data...")

    X_train, y_train = [], []
    
    for structure_class in STRUCTURE_CLASSES:
        count = 0
        print(f"🛠️ Generating data for class: {structure_class} ({samples_per_class} samples)...")
        
        while count < samples_per_class:
            sequence = generate_random_sequence(sequence_length)
            features = extract_features(sequence)
            assigned_class = features["structure_class"]
            
            if assigned_class == structure_class:
                feature_vector = np.array([sequence.count(aa) / len(sequence) for aa in AMINO_ACIDS], dtype=np.float32)  # ✅ Ensure float dtype
                X_train.append(feature_vector)
                y_train.append(assigned_class)
                count += 1

    X_train = np.array(X_train, dtype=np.float32)  # ✅ Ensure float dtype
    y_train = np.array(y_train)

    if save_csv:
        df = pd.DataFrame(X_train, columns=[aa for aa in AMINO_ACIDS])
        df["Structure_Class"] = y_train
        df.to_csv("training_data.csv", index=False)
        print(f"✅ Training data saved to 'training_data.csv'")

    return X_train, y_train

# Class for deep learning model
class ProteinStructureClassifier:
    def __init__(self):
        """Initializes the deep learning model for sequence-based protein structure classification."""
        print("🚀 Initializing model...")

        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.label_encoder.fit(STRUCTURE_CLASSES)

        # Check if a trained model and scaler exist
        if os.path.exists("protein_structure_model.keras") and os.path.exists("scaler.pkl"):
            print("🔄 Loading pre-trained model and scaler...")
            self.model = tf.keras.models.load_model("protein_structure_model.keras")  # ✅ Updated to .keras format
            self.scaler = joblib.load("scaler.pkl")
            print("✅ Model and scaler loaded successfully.")
        else:
            print("🚀 No pre-trained model found. Creating a new model...")
            
            self.model = Sequential([
                Dense(128, activation='relu', input_shape=(20,)),  
                Dropout(0.3),
                Dense(64, activation='relu'),
                Dropout(0.3),
                Dense(32, activation='relu'),
                Dense(16, activation='relu'),
                Dense(5, activation='softmax')  
            ])
            self.model.compile(optimizer=Adam(learning_rate=0.0003), 
                               loss='sparse_categorical_crossentropy', 
                               metrics=['accuracy'])

    def train(self, X_train, y_train, epochs=300, batch_size=16):
        """Trains the deep learning model with given training data."""
        print("📊 Training the model...")
        self.scaler.fit(X_train)
        X_scaled = self.scaler.transform(X_train)

        y_encoded = self.label_encoder.transform(y_train)
        self.model.fit(X_scaled, y_encoded, epochs=epochs, batch_size=batch_size)

        # Save trained model & scaler after training
        self.model.save("protein_structure_model.keras")  # ✅ Updated to .keras format
        joblib.dump(self.scaler, "scaler.pkl")
        print("✅ Model and scaler saved.")

    def predict(self, sequence):
        """Predicts the structural class of a given amino acid sequence of any length."""
        validated_seq = validate_amino_acid_sequence(sequence)

        # Ensure valid input transformation
        feature_vector = np.array([validated_seq.count(aa) / len(validated_seq) for aa in AMINO_ACIDS], dtype=np.float32)  # ✅ Convert to float

        try:
            X_scaled = self.scaler.transform([feature_vector])
        except AttributeError:
            raise ValueError("Scaler has not been fitted yet. Train the model first.")
        
        prediction = self.model.predict(X_scaled)
        predicted_class = self.label_encoder.inverse_transform([prediction.argmax()])[0]
        return predicted_class
