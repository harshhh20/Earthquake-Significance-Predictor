from flask import Flask, request, jsonify, render_template
from output import model, calculate_severity, get_safety_instructions
import pandas as pd

app = Flask(__name__)

# --------- ROUTES TO FRONTEND PAGES --------- #

@app.route('/')
def serve_home():
    return render_template('index.html')

@app.route('/predict')
def serve_predict():
    return render_template('predict.html')

@app.route('/analytics')
def serve_analytics():
    return render_template('analytics.html')

# --------- API ENDPOINT FOR PREDICTION --------- #

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        # Extract values from request
        magnitude = float(data.get('magnitude'))
        state = data.get('state')
        locality_type = data.get('locality_type')
        distance_km = float(data.get('distance_km'))

        # 1. Predict significance
        input_df = pd.DataFrame({
            'magnitudo': [magnitude],  # model expects this key
            'state': [state]
        })
        predicted_significance = model.predict(input_df)[0]

        # 2. Calculate severity
        severity = calculate_severity(predicted_significance, locality_type, distance_km)

        # 3. Get safety instructions
        instructions = get_safety_instructions(severity, locality_type)

        return jsonify({
            "predicted_significance": round(predicted_significance, 2),
            "severity_score": round(severity, 2),
            "instructions": instructions
        })

    except Exception as e:
        print(f"Error in prediction: {e}")  # Add logging for debugging
        return jsonify({"error": str(e)}), 400

# --------- RUN APP --------- #

if __name__ == '__main__':
    app.run(debug=True)
