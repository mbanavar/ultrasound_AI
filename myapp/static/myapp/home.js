document.addEventListener("DOMContentLoaded", function () {
    const galleryImages = document.querySelectorAll(".gallery-container img");
    const displayImage = document.getElementById("displayed-image");
    const deleteForm = document.getElementById("delete-form");
    const processForm = document.getElementById("process-form");

    galleryImages.forEach(img => {
        img.addEventListener("click", function () {
            // Update the displayed image
            displayImage.src = this.src;

            // Set the selected image ID in the delete form's action URL
            const imageId = this.getAttribute("data-id");  // Get the image ID
            deleteForm.action = `delete/${imageId}/`;
            processForm.action = `process/${imageId}/`;// Update the form action URL
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const sliders = document.querySelectorAll('.slider-container input[type="range"]');
    sliders.forEach(slider => {
        const numberInput = slider.nextElementSibling;  // The number input is right after the slider
        numberInput.value = slider.value;  // Initialize the number input with the slider's value

        // Update the slider when the number input changes
        numberInput.addEventListener('input', function () {
            slider.value = numberInput.value;  // Sync the slider with the number input value
        });

        // Update the number input when the slider changes
        slider.addEventListener('input', function () {
            numberInput.value = slider.value;  // Sync the number input with the slider value
        });
    });
});

document.getElementById("id_image").addEventListener("change", function() {
    var fileName = this.files[0] ? this.files[0].name : "No file selected";
    document.getElementById("selected-file-name").textContent = fileName;
});