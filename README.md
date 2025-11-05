AI Health & Insurance Prediction - Full Project (static frontend + backend + ML)
==========================================================================

What is included
-----------------
- frontend/  -> Static website ready to host on Netlify (index.html, styles.css, prediction.js)
- backend/   -> Flask app that serves prediction endpoints (app.py) + requirements.txt
- ml/        -> Synthetic sample datasets (CSV), training script (train_model.py), and pre-trained models (models/health_model.pkl, models/ins_model.pkl)
- README.md  -> This file
- LICENSE    -> MIT (you can change)

Quickstart (local)
------------------
1. Frontend only (Netlify):
   - Upload the frontend/ folder to Netlify (drag & drop) OR push to a GitHub repo and connect Netlify.
   - Before use, edit frontend/prediction.js and set API_BASE to the URL of your deployed backend.
   - Also replace FORM_ID in frontend/index.html iframe with your Google Form's id if you want to embed it.

2. Backend (Flask):
   - Install Python 3.9+ and create a virtualenv.
   - From backend/ directory, install requirements:
       pip install -r requirements.txt
   - Run the app (development):
       python app.py
   - For production, deploy to Cloud Run / Railway / Heroku. Make sure ML models are present at ../ml/models/*.pkl relative to backend/app.py
   - If deploying to a separate service, update frontend/prediction.js API_BASE to the deployed URL.

3. Training custom models:
   - Edit ml/health_sample.csv or replace with your Google Sheets-exported CSV.
   - Run the training script to retrain and overwrite models:
       python ml/train_model.py

Notes & next steps
------------------
- The included datasets are synthetic for demo/testing. Replace with real datasets (Kaggle/UCI) or your collected Google Sheets data for production.
- Add authentication, input validation, and HTTPS for production use.
- For real-time scoring, create a Google Apps Script trigger on form submit to POST the new row to your backend.
- Add a privacy policy and consent checkbox to your form if collecting PII or health data.

Have fun! Customize and test carefully before any real-world use.