from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import pandas as pd
from flask_cors import CORS

# Load model and scaler
with open("model.pickle", "rb") as f:
    model = pickle.load(f)

with open("scaler.pickle", "rb") as f:
    scaler = pickle.load(f)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("app.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get form data
        age = float(request.form["age"])
        hypertension = int(request.form["hypertension"])
        heart_disease = int(request.form["heart_disease"])
        bmi = float(request.form["bmi"])
        HbA1c_level = float(request.form["HbA1c_level"])
        blood_glucose_level = float(request.form["blood_glucose_level"])
        gender = request.form["gender"]
        smoking_history = request.form["smoking_history"]

        # One-hot encoding
        gender_male = 1 if gender == "Male" else 0
        gender_other = 1 if gender == "Other" else 0
        smoking_smoker = 1 if smoking_history == "Smoker" else 0

        # Prepare input data
        feature_names = ['age', 'bmi', 'HbA1c_level', 'blood_glucose_level']
        input_data = {
            'age': [50],
            'bmi': [28.5],
            'HbA1c_level': [6.1],
            'blood_glucose_level': [140]
        }

        # Convert input data to DataFrame
        input_df = pd.DataFrame(input_data, columns=feature_names)

        # Transform data with scaler
        scaled_data = scaler.transform(input_df)
        age, bmi, HbA1c_level, blood_glucose_level = scaled_data[0]
        # input_data = np.array([
        #     [age, bmi, HbA1c_level, blood_glucose_level]
        # ])
        # scaled_data = scaler.transform(input_data)[0]
        #
        # age, bmi, HbA1c_level, blood_glucose_level = scaled_data

        # Combine scaled and categorical data
        final_input = np.concatenate((
            [age], [hypertension], [heart_disease], [bmi], [HbA1c_level], [blood_glucose_level], [gender_male], [gender_other], [smoking_smoker]
        ))

        # Make prediction
        prediction = model.predict([final_input])[0]
        result = "Yes" if prediction == 1 else "No"
        return jsonify({"diabetes": str(result)})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
