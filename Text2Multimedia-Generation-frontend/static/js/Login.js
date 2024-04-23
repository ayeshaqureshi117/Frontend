document.addEventListener('DOMContentLoaded', function () {
    // Event listener for form submission
    document.getElementById('loginForm').addEventListener('submit', function (event) {
        event.preventDefault();
        loginUser();
    });
});

function loginUser() {
    const formData = {
        email: document.getElementById('email').value,
        password: document.getElementById('password').value
    };

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Redirect to dashboard page
            window.location.href = data.redirect;
        } else {
            // Display error message
            alert(data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    });
}