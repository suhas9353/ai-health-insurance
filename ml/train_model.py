# Simple training script for synthetic data. Produces two models:
# - health_model.pkl : classifier (RandomForest)
# - ins_model.pkl : regressor (RandomForestRegressor)
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
import os

ml_dir = os.path.dirname(__file__)
health = pd.read_csv(os.path.join(ml_dir, 'health_sample.csv'))
ins = pd.read_csv(os.path.join(ml_dir, 'insurance_sample.csv'))

# Health model
Xh = health[['Age','BMI','SystolicBP','DiastolicBP','Smoking']]
yh = health['Target']
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(Xh, yh)
joblib.dump(clf, os.path.join(ml_dir, 'models', 'health_model.pkl'))

# Insurance model
Xi = ins[['Age','BMI','Smoking','PastClaims']]
yi = ins['Premium']
reg = RandomForestRegressor(n_estimators=100, random_state=42)
reg.fit(Xi, yi)
joblib.dump(reg, os.path.join(ml_dir, 'models', 'ins_model.pkl'))

print('Training complete. Models saved to models/ directory.')
