// Get the file input element
const fileInput = document.querySelector('input[type="file"]');

// Get the preview container element
const previewContainer = document.querySelector('.profile-picture-preview');

// Get the preview image element
const previewImage = previewContainer.querySelector('img');

// Set the default preview image source
previewImage.setAttribute('src', '{% static "img/placeholder.jpg" %}');

// Listen for a file selection
fileInput.addEventListener('change', function() {
  // Get the selected file
  const file = this.files[0];
  if (file) {
    // Create a new FileReader object
    const reader = new FileReader();
    // Set the preview image source when the file has loaded
    reader.addEventListener('load', function() {
      previewImage.setAttribute('src', this.result);
      previewImage.removeAttribute('src', '{% static "img/placeholder.jpg" %}');
    });
    // Read the selected file as a URL
    reader.readAsDataURL(file);
  } else {
    // Set the default preview image source if no file is selected
    previewImage.setAttribute('src', '{% static "img/placeholder.jpg" %}');
  }
});

// Listen for form submission
const form = document.querySelector('form');
form.addEventListener('submit', function() {
  // Set the preview image source to the uploaded image
  previewImage.setAttribute('src', URL.createObjectURL(fileInput.files[0]));
  previewImage.removeAttribute('src', '{% static "img/placeholder.jpg" %}');
});
