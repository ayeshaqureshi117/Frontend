// Fetch the login/logout link element
const loginLogoutLink = document.getElementById('loginLogoutLink');

// Event listener for click on login/logout link
loginLogoutLink.addEventListener('click', function(event) {
    // If the link text is 'Sign In', do nothing (link will take user to login page)
    if (loginLogoutLink.innerText === 'Sign In') {
        return;
    }

    // If the link text is 'Signout', perform logout action
    event.preventDefault(); // Prevent default link behavior
    logoutUser(); // Call logout function
});

// Function to logout user
function logoutUser() {
    fetch('/logout') // Call logout route
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url; // Redirect to homepage after logout
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    });
}
