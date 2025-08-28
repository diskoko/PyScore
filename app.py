from flask import Flask, render_template, request, jsonify, send_file
import os
import pandas as pd
from model import ScoreEstimator

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"

# ML Model instance
estimator = ScoreEstimator()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_csv():
    file = request.files.get("file")
    if not file or not file.filename.endswith(".csv"):
        return jsonify({"error": "Invalid file format"}), 400

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    df = pd.read_csv(filepath)
    estimator.load_data(df)
    
    return jsonify({
        "students": estimator.get_students(),
        "assessments": estimator.get_assessments()
    })

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    student = data.get("student")
    assessment = data.get("assessment")
    
    try:
        result = estimator.predict(student, assessment)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/export", methods=["GET"])
def export():
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], "predicted_markbook.csv")
    estimator.export_with_predictions(filepath)
    return send_file(filepath, as_attachment=True)
    
if __name__ == "__main__":
    app.run(debug=True)
