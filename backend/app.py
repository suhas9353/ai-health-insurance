from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib, os

app = Flask(__name__)
CORS(app)

# === Model Path Setup ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, '..', 'ml', 'models')

health_model_path = os.path.join(MODEL_DIR, 'health_model.pkl')
ins_model_path = os.path.join(MODEL_DIR, 'ins_model.pkl')

# Load models safely
try:
    health_model = joblib.load(health_model_path)
    ins_model = joblib.load(ins_model_path)
except Exception as e:
    print("⚠️ Model load warning:", e)
    health_model = None
    ins_model = None


@app.route('/')
def home():
    return "✅ Flask backend running. Try /predict_health or /predict_insurance"


# === Example Endpoint ===
@app.route('/health_example', methods=['GET'])
def health_example():
    return jsonify({'note': 'Use POST /predict_health with JSON body to get results.'})


# === Detailed Health Prediction ===
@app.route('/predict_health', methods=['POST'])
def predict_health():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON received'}), 400

    try:
        # Extract input data
        Age = float(data.get('Age', 0))
        Gender = int(data.get('Gender', 0))  # 0=Male, 1=Female
        HeightCm = float(data.get('HeightCm', 0))
        WeightKg = float(data.get('WeightKg', 0))
        SystolicBP = float(data.get('SystolicBP', 0))
        DiastolicBP = float(data.get('DiastolicBP', 0))
        Smoking = int(data.get('Smoking', 0))
        Alcohol = int(data.get('Alcohol', 0))
        Exercise = int(data.get('Exercise', 0))
        Diet = int(data.get('Diet', 0))
        Stress = int(data.get('Stress', 0))

        # Calculate BMI
        BMI = WeightKg / ((HeightCm / 100) ** 2) if HeightCm > 0 else 0

        # === Intelligent Health Risk Scoring ===
        score = (
            0.03 * Age +
            0.4 * Smoking +
            0.3 * Alcohol +
            0.2 * Stress -
            0.25 * Exercise -
            0.2 * Diet +
            (BMI - 25) * 0.1 +
            max(0, SystolicBP - 120) * 0.01 +
            max(0, DiastolicBP - 80) * 0.01
        )

        # Normalize risk (0–1)
        probability = max(0, min(1, score / 10))

        # Categorize
        if probability < 0.3:
            risk = "Low Risk"
            advice = "You're maintaining good health! Keep exercising regularly."
            tips = "✅ Stay hydrated, eat balanced meals, and get 7–8 hours of sleep."
        elif probability < 0.7:
            risk = "Moderate Risk"
            advice = "Some indicators suggest potential health concerns."
            tips = "⚠️ Increase daily activity, avoid junk food, and manage stress."
        else:
            risk = "High Risk"
            advice = "Please consult a healthcare professional soon."
            tips = "❌ Quit smoking/alcohol, adopt a low-sodium diet, and reduce stress."

        return jsonify({
            "BMI": round(BMI, 2),
            "probability": round(float(probability), 2),
            "risk_category": risk,
            "recommendation": advice,
            "tips": tips
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# === Enhanced Insurance Premium Prediction ===
@app.route('/predict_insurance', methods=['POST'])
def predict_insurance():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON received'}), 400

    try:
        Age = float(data.get('Age', 0))
        BMI = float(data.get('WeightKg', 0)) / ((float(data.get('HeightCm', 1)) / 100) ** 2)
        Smoking = int(data.get('Smoking', 0))
        Alcohol = int(data.get('Alcohol', 0))
        Stress = int(data.get('Stress', 0))
        Exercise = int(data.get('Exercise', 0))
        Diet = int(data.get('Diet', 0))
        PastClaims = int(data.get('PastClaims', 0))

        # === Smarter Premium Estimation Formula ===
        base = 4000
        risk_factor = Smoking * 1200 + Alcohol * 800 + Stress * 700
        lifestyle_adjustment = (2 - Diet) * 300 + (7 - Exercise) * 150
        claim_factor = PastClaims * 500
        age_factor = Age * 25 + (BMI - 25) * 50

        premium = base + risk_factor + lifestyle_adjustment + claim_factor + age_factor
        lower = round(premium * 0.9, 2)
        upper = round(premium * 1.1, 2)

        if premium < 7000:
            tier = "Basic Plan"
            note = "💡 Suitable for low-risk, healthy individuals."
        elif premium < 12000:
            tier = "Balanced Plan"
            note = "⚖️ Medium coverage with affordable pricing."
        else:
            tier = "Comprehensive Plan"
            note = "🏥 High coverage recommended for high-risk profiles."

        return jsonify({
            "estimated_premium": round(float(premium), 2),
            "confidence_range": [lower, upper],
            "premium_tier": tier,
            "note": note
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# === Run App ===
if __name__ == '__main__':
    app.run(debug=True)
