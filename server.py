import base64
import io

import joblib
import numpy as np
from flask import Flask, jsonify, request
from PIL import Image

app = Flask(__name__)

# Load your trained models
xgb_model = joblib.load('models/xgb_model.pkl')
svm_model = joblib.load('models/svm_model.pkl')
rf_model = joblib.load('models/rf_model.pkl')

def predict(image):
    # Example preprocessing
    img = Image.open(io.BytesIO(base64.b64decode(image.split(',')[1])))
    img = img.resize((64, 64))  # Resize image
    img_array = np.array(img).flatten().reshape(1, -1)  # Flatten and reshape

    # Use a voting ensemble for prediction
    predictions = {
        'xgboost': xgb_model.predict(img_array)[0],
        'svm': svm_model.predict(img_array)[0],
        'random_forest': rf_model.predict(img_array)[0]
    }
    # Majority voting or decision-making logic
    final_prediction = max(predictions, key=predictions.get)
    return final_prediction

@app.route('/predict', methods=['POST'])
def predict_route():
    data = request.json
    image = data.get('image')
    if not image:
        return jsonify({"error": "No image provided"}), 400

    prediction = predict(image)
    return jsonify({"prediction": prediction})

if __name__ == '__main__':
    app.run(debug=True)
