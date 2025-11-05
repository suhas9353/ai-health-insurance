// prediction.js
// Use local Flask backend or deployed API endpoint
// Example: 'http://127.0.0.1:5000' for local testing, or your Render/Railway URL for live use.
const API_BASE = 'https://ai-health-insurance.onrender.com';


// Utility function to update UI text
function show(id, text) {
  document.getElementById(id).innerText = text;
}

// Handle unified form submission
document.getElementById('userForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const payload = {
    Age: Number(document.getElementById('age').value),
    HeightCm: Number(document.getElementById('height').value),
    WeightKg: Number(document.getElementById('weight').value),
    SystolicBP: Number(document.getElementById('systolic').value),
    DiastolicBP: Number(document.getElementById('diastolic').value),
    Smoking: Number(document.getElementById('smoking').value),
    PastClaims: Number(document.getElementById('claims').value)
  };

  // Reset UI
  show('healthResult', '⏳ Predicting health risk...');
  show('insResult', '⏳ Estimating insurance premium...');

  try {
    // --- 1️⃣ HEALTH PREDICTION ---
    const healthRes = await fetch(`${API_BASE}/predict_health`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(payload)
    });
    const healthData = await healthRes.json();

    if (healthData.error) throw new Error(healthData.error);

    const riskLabel = healthData.prediction === 1 ? '⚠️ High Risk' : '✅ Low Risk';
    const prob = (healthData.probability * 100).toFixed(2);

    show('healthResult', `Prediction: ${riskLabel}\nProbability: ${prob}%`);

    // --- 2️⃣ INSURANCE PREDICTION ---
    const BMI = payload.WeightKg / ((payload.HeightCm / 100) ** 2);
    const insRes = await fetch(`${API_BASE}/predict_insurance`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        Age: payload.Age,
        BMI: BMI,
        Smoking: payload.Smoking,
        PastClaims: payload.PastClaims
      })
    });
    const insData = await insRes.json();

    if (insData.error) throw new Error(insData.error);

    const premium = insData.estimated_premium.toFixed(2);
    show('insResult', `💰 Estimated Premium: ₹${premium}`);

  } catch (err) {
    show('healthResult', `❌ Error: ${err.message}`);
    show('insResult', `❌ Unable to get predictions`);
  }
});
