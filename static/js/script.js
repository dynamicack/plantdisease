// Wait for the DOM content to fully load
document.addEventListener('DOMContentLoaded', function () {

    // Smooth scroll to sections when clicking links with hash in href (for navigation)
    const navLinks = document.querySelectorAll('a[href^="#"]');
    navLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();

            const targetId = link.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Image preview functionality when selecting a file for prediction
    const fileInput = document.querySelector('input[type="file"]');
    const previewImage = document.getElementById('imagePreview');

    if (fileInput) {
        fileInput.addEventListener('change', function (e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function () {
                    previewImage.src = reader.result;
                    previewImage.style.display = 'block';
                };
                reader.readAsDataURL(file);
            } else {
                previewImage.style.display = 'none';
            }
        });
    }

    // Display loading spinner when submitting form (For predictions, etc.)
    const form = document.querySelector('form');
    const spinner = document.getElementById('loadingSpinner');
    
    if (form && spinner) {
        form.addEventListener('submit', function () {
            spinner.style.display = 'block'; // Show loading spinner
        });
    }

    // Handle showing and hiding treatment recommendations on hover
    const treatmentItems = document.querySelectorAll('.treatment-item');
    treatmentItems.forEach(item => {
        item.addEventListener('mouseenter', function () {
            item.classList.add('highlight');
        });

        item.addEventListener('mouseleave', function () {
            item.classList.remove('highlight');
        });
    });

});

// Optional: Scroll to top function for better navigation experience
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Optional: Show confirmation message on successful form submission
function showConfirmationMessage(message) {
    const confirmationElement = document.createElement('div');
    confirmationElement.classList.add('confirmation');
    confirmationElement.innerText = message;
    document.body.appendChild(confirmationElement);

    setTimeout(function () {
        confirmationElement.remove();
    }, 3000); // Remove after 3 seconds
}
