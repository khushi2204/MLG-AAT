const uploadImage = document.getElementById("upload-image");
const predictionText = document.getElementById("prediction-text");
const predictionStatus = document.getElementById("prediction-status");
const alphabetSound = document.getElementById("alphabet-sound");

uploadImage.addEventListener("change", async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  // Show processing status
  predictionStatus.style.display = "block";
  predictionStatus.textContent = "Processing...";

  const reader = new FileReader();
  reader.onload = async () => {
    const base64Image = reader.result.split(",")[1]; // Remove the data:image part of the base64 string

    try {
      const response = await fetch("http://127.0.0.1:5000", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ image: base64Image }),
      });

      if (!response.ok) throw new Error("Failed to fetch prediction");

      const result = await response.json();
      predictionText.textContent = `The predicted sign is: ${result.alphabet}`;
      predictionStatus.style.display = "none";

      // Update and play the audio
      alphabetSound.style.display = "block";
      alphabetSound.src = `data:audio/mp3;base64,${result.sound}`;
      alphabetSound.play();
    } catch (error) {
      console.error("Error:", error);
      predictionText.textContent = "Error processing the image.";
      predictionStatus.style.display = "none";
    }
  };

  reader.readAsDataURL(file); // Read file as base64
});
