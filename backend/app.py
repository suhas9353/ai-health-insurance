from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import os

app = Flask(__name__)
CORS(app)

MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'ml', 'models')

health_model_path = os.path.join(MODEL_DIR, 'health_model.pkl')
ins_model_path = os.path.join(MODEL_DIR, 'ins_model.pkl')

health_model = joblib.load(health_model_path)
ins_model = joblib.load(ins_model_path)

@app.route('/predict_health', methods=['POST'])
def predict_health():
    data = request.get_json()
    try:
        Age = float(data.get('Age', 0))
        HeightCm = float(data.get('HeightCm', 0))
        WeightKg = float(data.get('WeightKg', 0))
        SystolicBP = float(data.get('SystolicBP', 0))
        DiastolicBP = float(data.get('DiastolicBP', 0))
        Smoking = int(data.get('Smoking', 0))
        BMI = WeightKg / ((HeightCm/100.0)**2) if HeightCm>0 else 0.0
        X = [[Age, BMI, SystolicBP, DiastolicBP, Smoking]]
        proba = None
        if hasattr(health_model, 'predict_proba'):
            proba = float(health_model.predict_proba(X)[0][1])
        pred = int(health_model.predict(X)[0])
        return jsonify({'prediction': pred, 'probability': proba})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/predict_insurance', methods=['POST'])
def predict_insurance():
    data = request.get_json()
    try:
        Age = float(data.get('Age', 0))
        BMI = float(data.get('BMI', 0))
        Smoking = int(data.get('Smoking', 0))
        PastClaims = int(data.get('PastClaims', 0))
        X = [[Age, BMI, Smoking, PastClaims]]
        premium = float(ins_model.predict(X)[0])
        return jsonify({'estimated_premium': premium})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/health_example', methods=['GET'])
def health_example():
    return jsonify({'note':'This endpoint exists. POST to /predict_health with JSON.'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
