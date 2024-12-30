import base64
import io
import logging
import os

import joblib
import numpy as np
from flask import Flask, jsonify, request
from flask_cors import CORS
from gtts import gTTS
from PIL import Image

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app, resources={r"/predict": {"origins": "*"}})

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Custom preprocessing to match the training
def preprocess_image(img):
    """
    Resize and preprocess the image to match the model input requirements.
    """
    img = img.resize((28, 28)).convert('L')  # Resize to 28x28 and convert to grayscale
    img_array = np.array(img).flatten()  # Flatten to 1D array
    return img_array / 255.0  # Normalize pixel values to [0, 1]

def predict(image, model_choice):
    try:
        # Dynamically load the model based on the choice
        model_path = f'models/{model_choice}_model.pkl'
        model = joblib.load(model_path)

        # Decode the base64 image
        img = Image.open(io.BytesIO(base64.b64decode(image.split(',')[1])))
        img_array = preprocess_image(img).reshape(1, -1)  # Reshape to (1, num_features)

        # Predict using the selected model
        prediction = model.predict(img_array)

        # Map prediction to alphabet
        label_mapping = {
            0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H',
            8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O',
            15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V',
            22: 'W', 23: 'X', 24: 'Y', 25: 'Z'
        }
        predicted_label = label_mapping.get(prediction[0], "Unknown")

        # Generate sound for prediction
        tts = gTTS(text=f"The predicted hand sign is {predicted_label}", lang='en')
        audio_filename = f"{predicted_label}.mp3"
        tts.save(audio_filename)

        # Read the audio file as base64
        with open(audio_filename, "rb") as audio_file:
            sound_base64 = base64.b64encode(audio_file.read()).decode('utf-8')

        # Remove the temporary file
        os.remove(audio_filename)

        return predicted_label, sound_base64
    except Exception as e:
        logger.error(f"Error in prediction: {e}", exc_info=True)
        return str(e), None

@app.route('/predict', methods=['POST'])
def predict_route():
    try:
        data = request.json
        image = data.get('image')
        model_choice = data.get('model')

        # Validate the input data
        if not image:
            logger.error("No image provided")
            return jsonify({"error": "No image provided"}), 400
        if model_choice not in ['svm', 'random_search']:
            logger.error("Invalid model choice")
            return jsonify({"error": "Invalid model choice"}), 400

        # Make the prediction using the selected model
        prediction, sound = predict(image, model_choice)

        if sound is None:
            logger.error(f"Prediction failed: {prediction}")
            return jsonify({"error": f"Prediction failed: {prediction}"}), 500

        # Return the response with prediction, sound, and model used
        response = {
            "alphabet": prediction,
            "sound": sound,
            "model_used": model_choice.upper()
        }
        logger.info(f"Prediction successful: {response}")
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error in /predict route: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

# Make sure this block is correct
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)