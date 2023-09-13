document.addEventListener("DOMContentLoaded", function () {
    const analyzeButton = document.getElementById("analyze-button");
    const resultsElement = document.getElementById("results");

    analyzeButton.addEventListener("click", function () {
        const form = document.getElementById("upload-form");
        const formData = new FormData(form);
        fetch("/upload", {
            method: "POST",
            body: formData,
        })
            .then((response) => response.json())
            .then((data) => {
                // Clear any previous results
                resultsElement.innerHTML = "";

                // Display each analysis result
                for (const key in data) {
                    const result = data[key];
                    const resultDiv = document.createElement("div");
                    resultDiv.textContent = `${key}: ${result}`;
                    resultsElement.appendChild(resultDiv);
                }
            })
            .catch((error) => {
                console.error("Error:", error);
            });
    });
});




   

