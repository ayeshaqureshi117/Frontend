document.addEventListener('DOMContentLoaded', function () {
    // Event listener for form submission
    document.getElementById('signupForm').addEventListener('submit', function (event) {
        event.preventDefault();
        validateForm();
    });

    // Event listener for show/hide password checkbox
    document.getElementById('showPassword').addEventListener('change', function () {
        const passwordInput = document.getElementById('password');
        if (this.checked) {
            passwordInput.type = 'text';
        } else {
            passwordInput.type = 'password';
        }
    });

    // Event listener for show/hide confirm password checkbox
    document.getElementById('showConfirmPassword').addEventListener('change', function () {
        const confirmPasswordInput = document.getElementById('confirmPassword');
        if (this.checked) {
            confirmPasswordInput.type = 'text';
        } else {
            confirmPasswordInput.type = 'password';
        }
    });
});

function validateForm() {
    const formData = {
        firstName: document.getElementById('firstName').value,
        lastName: document.getElementById('lastName').value,
        username: document.getElementById('username').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value,
        confirmPassword: document.getElementById('confirmPassword').value
    };

    // Check if all fields are filled
    for (const key in formData) {
        if (!formData[key]) {
            alert('Please fill in all fields');
            return;
        }
    }

    // Check if Name contains only letters
    const nameRegex = /^[A-Za-z]+$/;
    if (!nameRegex.test(formData.firstName) || !nameRegex.test(formData.lastName)) {
        alert('Name should only contain letters');
        return;
    }

    // Check if username is valid
    const usernameRegex = /^(?=.*[a-zA-Z])[a-zA-Z0-9_]+$/;
    if (!usernameRegex.test(formData.username)) {
        alert('Username should not contain only numbers or special characters!');
        return;
    }

    // Email format validation using regular expression
    const emailRegex = /^\S+@\S+\.\S+$/;
    if (!emailRegex.test(formData.email)) {
        alert('Invalid email address');
        return;
    }

    // Password length check
    if (formData.password.length < 8) {
        alert('Password should be at least 8 characters long');
        return;
    }

    // Check if password contains both letters and numbers
    const passwordRegex = /^(?=.*[a-zA-Z])(?=.*\d).+$/;
    if (!passwordRegex.test(formData.password)) {
        alert('Password should contain both letters and numbers');
        return;
    }

    // Check if passwords match
    if (formData.password !== formData.confirmPassword) {
        alert('Password and Confirm Password don\'t match. Try again!');
        return;
    }

    // If all validations pass, submit the form
    submitForm(formData);
}

function submitForm(formData) {
        fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Display success message
                alert(data.message);
                // Redirect to the login page
                window.location.href = data.redirect;
            } else {
                // Display error message
                alert(data.error);
            }
        })
        .catch(error => {
            alert('Some error occurred. Please try again.');
            console.error(error);
        });
    }

