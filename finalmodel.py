import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
import pickle

# Step 1: Load the Pretrained Model, Scaler, and LabelEncoder
try:
    with open("earthquake_significance_model.pkl", "rb") as file:
        model = pickle.load(file)

    with open("label_encoder.pkl", "rb") as file:
        label_encoder = pickle.load(file)

    with open("scaler.pkl", "rb") as file:
        scaler = pickle.load(file)

    print("Model, Label Encoder, and Scaler loaded successfully!")

except FileNotFoundError:
    print("Model files not found! Please train the model first.")

# Step 2: User Input for Predictions
def predict_significance(state, magnitudo):
    try:
        # Encode the state
        state_encoded = label_encoder.transform([state])[0]
    except ValueError:
        # Handle the case where the state is not in the encoder's vocabulary
        return f"State '{state}' is not recognized. Please enter a valid state from the dataset."

    # Scale the magnitudo
    magnitudo_scaled = scaler.transform([[magnitudo]])[0][0]

    # Make prediction using the loaded model
    predicted_significance = model.predict([[state_encoded, magnitudo_scaled]])[0]
    return predicted_significance

# Get user input for state and magnitudo
state_input = input("Enter the state: ")
magnitudo_input = float(input("Enter the magnitudo: "))

# Predict significance for the given state and magnitudo
predicted_significance = predict_significance(state_input, magnitudo_input)

# Output the prediction or error message
if isinstance(predicted_significance, str):
    print(predicted_significance)  # Error message if state is unknown
else:
    print(f"Predicted significance for state '{state_input}' and magnitudo '{magnitudo_input}': {predicted_significance:.2f}")
