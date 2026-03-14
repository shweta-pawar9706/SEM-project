// Show file name when user selects a file
document.getElementById("resume-input").addEventListener("change", function () {
    const file = this.files[0];
    if (file) {
        document.getElementById("file-name").textContent = "Selected: " + file.name;
        document.getElementById("analyze-btn").disabled = false;
    }
});


// Upload resume to Flask backend
async function uploadResume() {
    const fileInput = document.getElementById("resume-input");
    const file = fileInput.files[0];

    if (!file) {
        showError("Please select a file first.");
        return;
    }

    // Show loading spinner
    document.getElementById("loading").classList.remove("d-none");
    document.getElementById("analyze-btn").disabled = true;
    document.getElementById("error-msg").classList.add("d-none");

    // Prepare form data
    const formData = new FormData();
    formData.append("resume", file);

    try {
        // Send to Flask backend
        const response = await fetch("http://127.0.0.1:5000/upload", {
            method: "POST",
            body: formData
        });

        const result = await response.json();

        if (response.ok) {
            // Save parsed data to localStorage for use on other pages
            localStorage.setItem("resumeData", JSON.stringify(result.data));

            // Redirect to dashboard
            window.location.href = "dashboard.html";
        } else {
            showError(result.error || "Something went wrong.");
        }

    } catch (error) {
        showError("Cannot connect to server. Make sure Flask is running.");
    } finally {
        document.getElementById("loading").classList.add("d-none");
        document.getElementById("analyze-btn").disabled = false;
    }
}


// Show error message
function showError(message) {
    const errorDiv = document.getElementById("error-msg");
    errorDiv.textContent = message;
    errorDiv.classList.remove("d-none");
}