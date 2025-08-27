Score Estimator Flask app

Structure:
- app.py: Flask entry point
- model.py: ML logic (OOP)
- forms.py: optional Flask-WTF forms
- static/: css/js/manifest/sw
- templates/: index.html
- uploads/: uploaded CSVs

How to run (PowerShell):

python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
$env:FLASK_APP = 'app.py'
# run Flask
flask run

API endpoints:
- POST /api/upload (form-data file=...)
- POST /api/estimate (json {student, task})
- GET  /api/export
