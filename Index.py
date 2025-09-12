from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pickle

# Step 1: Initialize Flask
app = Flask(__name__)
CORS(app)

# Step 2: Load the trained model
try:
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    print("✅ Model loaded successfully, TYPE: ", type(model))
except Exception as e:
    print("❌ Error loading model:", e)
    model = None

# Step 3: Simple route
@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500

    try:
        data = request.get_json()

        # Extract features in the right order
        features = np.array([[
            data["study_time_weekly"],
            data["absences"],
            data["parental_support"],
            data["tutoring"],
            data["parental_education"],
            data["extracurricular_activities"]
        ]])

        # Make prediction
        prediction = model.predict(features)[0]

        return jsonify({
            "input": data,
            "prediction": str(prediction)  # convert NumPy type to string
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/", methods=["GET"])
def home():
    # return render_template("index.html")
    return jsonify({"message": "Student Performance Prediction API is running 🚀"})


# Step 4: Run app
if __name__ == "__main__":
    app.run(debug=True)
