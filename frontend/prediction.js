const API_BASE = 'https://ai-health-insurance.onrender.com'; // your Render backend

document.getElementById('userForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const payload = {
    Age: Number(document.getElementById('age').value),
    Gender: Number(document.getElementById('gender').value),
    HeightCm: Number(document.getElementById('height').value),
    WeightKg: Number(document.getElementById('weight').value),
    SystolicBP: Number(document.getElementById('systolic').value),
    DiastolicBP: Number(document.getElementById('diastolic').value),
    Smoking: Number(document.getElementById('smoking').value),
    Alcohol: Number(document.getElementById('alcohol').value),
    Exercise: Number(document.getElementById('exercise').value),
    Diet: Number(document.getElementById('diet').value),
    Stress: Number(document.getElementById('stress').value),
    PastClaims: Number(document.getElementById('claims').value)
  };

  document.getElementById('healthResult').innerText = "⏳ Calculating health risk...";
  document.getElementById('insResult').innerText = "⏳ Estimating premium...";

  try {
    const res = await fetch(`${API_BASE}/predict_health`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(payload)
    });
    const health = await res.json();

    document.getElementById('healthResult').innerText = `
🧠 Health Risk Analysis:
Risk: ${health.risk_category}
Probability: ${(health.probability * 100).toFixed(1)}%
Recommendation: ${health.recommendation}
Lifestyle Tips: ${health.tips}
    `;

    const ins = await fetch(`${API_BASE}/predict_insurance`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(payload)
    });
    const insurance = await ins.json();

    document.getElementById('insResult').innerText = `
💰 Insurance Premium Estimate:
Estimated Premium: ₹${insurance.estimated_premium}
Range: ₹${insurance.confidence_range[0]} - ₹${insurance.confidence_range[1]}
Plan Tier: ${insurance.premium_tier}
Note: ${insurance.note}
    `;
  } catch (err) {
    document.getElementById('healthResult').innerText = "❌ Error: " + err.message;
  }
});
