import os
import pandas as pd
from model import ScoreEstimator

# Prepare sample CSV in uploads
os.makedirs('uploads', exist_ok=True)
sample_path = os.path.join('uploads', 'sample_markbook.csv')
if not os.path.exists(sample_path):
    sample = """Student,Math Test 1,Math Test 2,Math Quiz 1,Math Quiz 2,Math Assignment
Alex Johnson,85,82,90,87,
Sarah Smith,78,80,85,83,88
Mike Brown,92,89,95,91,94
Emma Wilson,,85,88,90,92
"""
    with open(sample_path, 'w', encoding='utf-8') as f:
        f.write(sample)

se = ScoreEstimator()
df = pd.read_csv(sample_path)
se.load_data(df)

student = 'Emma Wilson'
target = 'Math Test 1'

print('Running linear regression prediction...')
res_lin = se.predict(student, target, model_type='linear')
print(res_lin)

print('Running decision tree regression prediction...')
res_tree = se.predict(student, target, model_type='tree')
print(res_tree)

# export with predictions
out = os.path.join('uploads','predicted_markbook.csv')
se.export_with_predictions(out)
print('Wrote', out)
