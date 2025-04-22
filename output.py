import os
import joblib
import numpy as np
import pandas as pd

# Load the trained model
model_path = os.path.join(os.path.dirname(__file__), 'random_forest_regressor.pkl')
model = joblib.load(model_path)

def calculate_severity(significance, locality_type, distance_km):
    """
    Calculates severity on a scale of 0 to 100.
    Applies exponential decay based on distance and adds locality weight.
    """

    # Clamp distance between 0 and 50 km
    distance_km = max(0, min(distance_km, 50))

    # Normalize significance to max 100
    max_significance = 100
    base_severity = min(significance / max_significance, 1.0)

    # Exponential decay factor for distance
    decay = np.exp(-distance_km / 50)
    severity = base_severity * decay * 100

    # Adjust for locality
    if locality_type.lower() == 'urban':
        severity *= 1.15
    else:
        severity *= 0.9

    return min(severity, 100)


def get_safety_instructions(severity, locality_type):
    is_urban = locality_type.lower() == 'urban'

    if severity < 20:
        return (
            "🟢 Minor tremors in {} area.\n"
            "- Stay calm, avoid elevators.\n"
            "- Monitor local news or alerts."
        ).format("urban" if is_urban else "rural")

    elif severity < 40:
        return (
            "🟡 Light earthquake in {} area.\n"
            "- Secure fragile items.\n"
            "- Avoid standing near windows.\n"
            "- Be ready for aftershocks."
        ).format("urban" if is_urban else "rural")

    elif severity < 60:
        return (
            "🟠 Moderate earthquake in {} area.\n"
            "- Drop, Cover, and Hold On.\n"
            "- Avoid elevators.\n"
            "- Evacuate if necessary."
        ).format("urban" if is_urban else "rural")

    elif severity < 80:
        return (
            "🔴 Strong quake in a {} area!\n"
            "- Evacuate tall buildings.\n"
            "- Avoid glass and overhead objects.\n"
            "- Go to emergency shelters."
        ).format("urban" if is_urban else "rural")

    else:
        return (
            "🚨 Severe earthquake in {} area!\n"
            "- Immediate evacuation advised.\n"
            "- Avoid bridges and damaged structures.\n"
            "- Stay calm and wait for help."
        ).format("urban" if is_urban else "rural")


def predict_earthquake_response(magnitudo, state, locality_type, distance_km):
    # Step 1: Predict significance
    input_data = {
        'magnitudo': [magnitudo],
        'state': [state]
    }

    df = pd.DataFrame(input_data)
    predicted_significance = model.predict(df)[0]

    # Step 2: Calculate severity
    severity_score = calculate_severity(predicted_significance, locality_type, distance_km)

    # Step 3: Get safety instructions
    instructions = get_safety_instructions(severity_score, locality_type)

    # Output
    print(f"\n🌍 Predicted Significance: {predicted_significance:.2f}")
    print(f"🔥 Calculated Severity Score: {severity_score:.2f} / 100")
    print("📋 Safety Instructions:\n" + instructions)


# ---------- Example Usage ----------

if __name__ == "__main__":
    # Example input values
    magnitudo = 6.3
    state = "California"
    locality_type = "urban"
    distance_km = 25

    predict_earthquake_response(magnitudo, state, locality_type, distance_km)
