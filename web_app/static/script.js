let videoStream;
let currentMode = 'none'; // 'image' or 'camera'
let uploadedFile = null;

const videoElement = document.getElementById('videoElement');
const imagePreview = document.getElementById('imagePreview');
const placeholder = document.getElementById('placeholder-text');
const canvas = document.getElementById('canvas');
const cameraBtn = document.getElementById('cameraBtn');


// 1. Handle Image Upload
document.getElementById('imageInput').addEventListener('change', function (e) {
    if (e.target.files && e.target.files[0]) {
        uploadedFile = e.target.files[0];

        // Stop camera if running
        stopCamera();

        // Show Image
        const reader = new FileReader();
        reader.onload = function (e) {
            imagePreview.src = e.target.result;
            imagePreview.hidden = false;
            placeholder.hidden = true;
            videoElement.hidden = true;
            currentMode = 'image';
        }
        reader.readAsDataURL(uploadedFile);
    }
});

// 2. Handle Camera Toggle
function toggleCamera() {
    if (currentMode === 'camera') {
        capturePhoto(); // If camera is on, clicking button captures photo
    } else {
        startCamera();
    }
}

function startCamera() {
    navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
        .then(stream => {
            videoStream = stream;
            videoElement.srcObject = stream;

            // STRICTLY SHOW/HIDE ELEMENTS
            videoElement.hidden = false;    // Show video
            imagePreview.hidden = true;     // Hide image
            placeholder.hidden = true;      // Hide text

            // Update Button UI
            cameraBtn.innerHTML = '<i class="fas fa-camera"></i> Capture';
            cameraBtn.style.background = "#ffdd00";
            cameraBtn.style.color = "#000";

            currentMode = 'camera';
        })
        .catch(err => {
            alert("Camera access denied. Please allow permissions.");
            console.error(err);
        });
}

function stopCamera() {
    if (videoStream) {
        videoStream.getTracks().forEach(track => track.stop());
        videoStream = null;
    }
    videoElement.hidden = true;
    cameraBtn.innerHTML = '<i class="fas fa-camera"></i> Camera';
    cameraBtn.style.background = "";
    cameraBtn.style.color = "";

    resetPlaceholder();   // 👈 ADD THIS LINE
}


function capturePhoto() {
    // Draw video frame to canvas
    canvas.width = videoElement.videoWidth;
    canvas.height = videoElement.videoHeight;
    canvas.getContext('2d').drawImage(videoElement, 0, 0);

    // Convert to image blob
    canvas.toBlob(blob => {
        uploadedFile = new File([blob], "capture.jpg", { type: "image/jpeg" });
        imagePreview.src = URL.createObjectURL(blob);
        imagePreview.hidden = false;
        videoElement.hidden = true;
        stopCamera();
        currentMode = 'image';
    });
}



// 3. Classification Logic
// function classifyWaste() {
//     if (!uploadedFile && currentMode !== 'image') {
//         alert("Please upload an image or capture a photo first!");
//         return;
//     }

//     const resultCard = document.getElementById('resultCard');
//     const resultText = document.getElementById('wasteType');
//     const progressFill = document.getElementById('progressFill');
//     const confValue = document.getElementById('confValue');
//     const hint = document.getElementById('disposalHint');
//     // NEW: Get the preview container
//     const previewContainer = document.getElementById('previewContainer');

//     // Hide previous results during new scan
//     resultCard.hidden = true;

//     // --- START SCANNING ---
//     // Add the class that triggers the CSS animation
//     previewContainer.classList.add('scanning');
//     cameraBtn.disabled = true; // Disable buttons during scan
//     document.querySelector('.button-group label').style.pointerEvents = 'none';


//     // --- MOCK PREDICTION (Wait 2.5s for animation) ---
//     setTimeout(() => {
//         // --- STOP SCANNING ---
//         // Remove the class to stop animation
//         previewContainer.classList.remove('scanning');
//         cameraBtn.disabled = false; // Re-enable buttons
//         document.querySelector('.button-group label').style.pointerEvents = 'auto';

//         // Show Loading state
//         resultCard.hidden = false;
//         resultText.innerText = "Analyzing...";
//         progressFill.style.width = "0%";

//         const formData = new FormData();
//         formData.append("image", uploadedFile);

//         fetch("/predict", {
//             method: "POST",
//             body: formData
//         })
//             .then(res => res.json())
//             .then(data => {

//                 previewContainer.classList.remove('scanning');

//                 resultCard.hidden = false;

//                 const confidence = data.confidence.toFixed(1);

//                 if (data.label === "DRY") {
//                     resultText.innerText = "Dry Waste ♻️";
//                     resultText.style.color = "#80ffdb";
//                     progressFill.style.background = "#80ffdb";
//                     hint.innerText = "Disposal: Blue Bin (Paper, Plastic, Metal)";
//                 } else {
//                     resultText.innerText = "Wet Waste 🍌";
//                     resultText.style.color = "#ffdd00";
//                     progressFill.style.background = "#ffdd00";
//                     hint.innerText = "Disposal: Green Bin (Organic, Food)";
//                 }

//                 progressFill.style.width = confidence + "%";
//                 confValue.innerText = confidence + "%";
//             });


//         if (isDry) {
//             resultText.innerText = "Dry Waste ♻️";
//             resultText.style.color = "#80ffdb";
//             progressFill.style.background = "#80ffdb";
//             hint.innerText = "Disposal: Blue Bin (Paper, Plastic, Metal)";
//         } else {
//             resultText.innerText = "Wet Waste 🍌";
//             resultText.style.color = "#ffdd00";
//             progressFill.style.background = "#ffdd00";
//             hint.innerText = "Disposal: Green Bin (Organic, Food, Peels)";
//         }

//         // Small delay for the progress bar animation to kick in visually
//         setTimeout(() => {
//             progressFill.style.width = confidence + "%";
//             confValue.innerText = confidence + "%";
//         }, 100);

//     }, 2500); // Wait 2.5 seconds for the scan animation
//     resetPlaceholder();

// }

function classifyWaste() {

    if (!uploadedFile) {
        alert("Please upload an image or capture a photo first!");
        return;
    }

    const resultCard = document.getElementById('resultCard');
    const previewContainer = document.getElementById('previewContainer');
    const loader = document.getElementById('loader');
    const resultText = document.getElementById('wasteType');
    const hint = document.getElementById('disposalHint');
    const progressFill = document.getElementById('progressFill');
    const confValue = document.getElementById('confValue');

    // Reset UI
    resultCard.hidden = false;
    loader.hidden = false;
    resultText.innerHTML = "Analyzing...";
    hint.innerText = "";
    progressFill.style.width = "0%";
    confValue.innerText = "";

    // Start scanning animation
    previewContainer.classList.add('scanning');

    // Disable buttons
    document.querySelectorAll("button").forEach(b => b.disabled = true);

    const formData = new FormData();
    formData.append("image", uploadedFile);

    fetch("/predict", {
        method: "POST",
        body: formData
    })
        .then(res => {
            if (!res.ok) throw new Error("Server error");
            return res.json();
        })
        .then(data => {

            // Stop scanning animation
            previewContainer.classList.remove('scanning');
            loader.hidden = true;

            // Enable buttons
            document.querySelectorAll(".btn").forEach(b => b.disabled = false);

            if (data.error) {
                alert("Backend error: " + data.error);
                return;
            }

            // 🔥 Update annotated result image
            if (data.result_image) {
                imagePreview.src = data.result_image + "?t=" + Date.now();
                imagePreview.hidden = false;
                placeholder.hidden = true;
            }

            const detections = data.objects || data.detections;

            if (!detections || detections.length === 0) {
                resultText.innerText = "No objects detected";
                hint.innerText = "Try another image";
                return;
            }

            let dryCount = 0;
            let wetCount = 0;

            detections.forEach(d => {
                if (d.waste_type === "DRY") dryCount++;
                else wetCount++;
            });

            // Update UI summary
            resultText.innerText =
                detections.length === 1
                    ? "1 Object Detected"
                    : `${detections.length} Objects Detected`;
            resultText.style.color = "#ffffff";

            hint.innerText = `Dry: ${dryCount} | Wet: ${wetCount}`;

            // Optional: Confidence bar = average confidence
            let avgConfidence = (
                detections.reduce((sum, d) => sum + d.confidence, 0)
                / detections.length
            ).toFixed(1);

            progressFill.style.width = avgConfidence + "%";
            confValue.innerText = avgConfidence + "%";

            // Color logic
            if (avgConfidence > 85)
                progressFill.style.background = "#00ff88";
            else if (avgConfidence > 60)
                progressFill.style.background = "#ffdd00";
            else
                progressFill.style.background = "#ff6b6b";


            // 4️⃣ 🔌 IoT Simulation Code HERE
            document.getElementById("segregateBtn").hidden = false;

        })
        .catch(err => {

            previewContainer.classList.remove('scanning');
            loader.hidden = true;
            document.querySelectorAll(".btn").forEach(b => b.disabled = false);

            alert("Prediction failed. Check backend.");
            console.error(err);
        });
}

function resetPlaceholder() {
    if (!uploadedFile) {
        imagePreview.hidden = true;
        placeholder.hidden = false;
    }
}

function startSegregation() {
    window.location.href = "/simulation";
}