document
  .getElementById("upload-image")
  .addEventListener("change", async (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = async (e) => {
        const imageData = e.target.result;

        // Call the API or model to predict
        const prediction = await predictSignLanguage(imageData);
        document.getElementById("prediction-text").textContent = prediction;
      };
      reader.readAsDataURL(file);
    }
  });

// Example function to call your ML model or API
async function predictSignLanguage(imageData) {
  try {
    const response = await fetch("http://localhost:5000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ image: imageData }),
    });
    const data = await response.json();
    return data.prediction; // Assuming API returns { prediction: "Detected Sign" }
  } catch (error) {
    console.error("Error predicting:", error);
    return "Error in prediction";
  }
}
