import base64
import io

import joblib
import numpy as np
from flask import Flask, jsonify, request
from flask_cors import CORS  # Import CORS
from gtts import gTTS
from PIL import Image

app = Flask(__name__)

# Enable CORS for all routes
CORS(app, resources={r"/predict": {"origins": "http://127.0.0.1:5501"}})

# Load the model
svm_model = joblib.load('models/svm_model.pkl')

def predict(image):
    img = Image.open(io.BytesIO(base64.b64decode(image.split(',')[1])))
    img = img.resize((28, 28))
    img_array = np.array(img).flatten().reshape(1, -1)
    img_array = img_array / 255.0
    
    prediction = svm_model.predict(img_array)
    
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
    tts.save("output.mp3")

    # Read the audio file as base64
    with open("output.mp3", "rb") as audio_file:
        sound_base64 = base64.b64encode(audio_file.read()).decode('utf-8')

    return predicted_label, sound_base64

@app.route('/predict', methods=['POST'])
def predict_route():
    data = request.json
    image = data.get('image')
    if not image:
        return jsonify({"error": "No image provided"}), 400

    prediction, sound = predict(image)
    return jsonify({"alphabet": prediction, "sound": sound})
@app.route('/predict', methods=['OPTIONS'])
def predict_options():
    return jsonify({"message": "Preflight request allowed"}), 200


if __name__ == '__main__':
    app.run(debug=True)
