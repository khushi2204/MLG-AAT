import { useState } from "react"; // Assuming you add CSS in this file

export default function FileUpload() {
  const [prediction, setPrediction] = useState(null);
  const [status, setStatus] = useState("");
  const [audioSrc, setAudioSrc] = useState("");
  const [predictionModel, setPredictionModel] = useState("svm");

  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = async (e) => {
      const base64Image = e.target.result;
      setStatus("Processing...");

      try {
        console.log(predictionModel);
        const response = await fetch(
          "https://mlg-aat-production.up.railway.app/predict",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              image: base64Image,
              model: predictionModel,
            }),
          }
        );

        const data = await response.json();
        if (data.error) {
          setStatus("Error: " + data.error);
        } else {
          setPrediction(`Predicted Alphabet: ${data.alphabet}`);
          setAudioSrc(`data:audio/mp3;base64,${data.sound}`);
          setStatus("");
        }
      } catch (error) {
        setStatus("Error occurred during prediction");
        console.error("Error:", error);
      }
    };

    reader.readAsDataURL(file);
  };

  const handleModelChange = (event) => {
    setPredictionModel(event.target.value);
  };

  return (
    <div className="file-upload-container">
      <header className="file-upload-header">
        <h1>Sign Language Alphabet Predictor</h1>
        <p>
          Empower communication through technology! Upload an image of a hand
          gesture, and let our AI model predict the corresponding alphabet.
        </p>
      </header>
      <div className="upload-section">
        <h2>Upload an Image</h2>
        <label htmlFor="upload-image" className="animated-label">
          Select an image:
        </label>
        <input
          type="file"
          id="upload-image"
          accept="image/*"
          onChange={handleFileChange}
        />
        <div className="model-selector">
          <label htmlFor="model-choice">Choose a model:</label>
          <select
            id="model-choice"
            onChange={handleModelChange}
            value={predictionModel}
          >
            <option value="svm">SVM</option>
            <option value="svm">Logistic Regression</option>
            <option value="svm">Random Forest</option>
          </select>
        </div>
        <div id="result" className="result-section">
          <h3>Prediction:</h3>
          <p id="prediction-text">{prediction || "No prediction yet."}</p>
          <p id="prediction-status">{status}</p>
        </div>
        {audioSrc && (
          <audio
            id="alphabet-sound"
            controls
            src={audioSrc}
            className="audio-control"
          />
        )}
      </div>
    </div>
  );
}
