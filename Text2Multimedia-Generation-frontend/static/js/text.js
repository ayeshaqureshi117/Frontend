// Add functions to show and hide loading icon
function showLoading() {
    document.querySelector('.loading').style.display = 'block';
}

function hideLoading() {
    document.querySelector('.loading').style.display = 'none';
}

document.getElementById('textForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission
    var form = event.target;
    var formData = new FormData(form);

    // Show loading spinner
    showLoading();

    // Send form data to Flask route via AJAX
    fetch('/text', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        var videoPath = data.video_path;
        console.log(videoPath);
        displayVideo(videoPath);
        // Hide loading spinner
        hideLoading();
    })
    .catch(error => {
        console.error('Error:', error);
        // Hide loading spinner on error
        hideLoading();
    });

    // Log a message to indicate that the function has been run
    console.log('Form submit event listener has been run.');
});

function displayVideo(videoPath) {
    var videoContainer = document.querySelector('.video-container');
    var video = document.getElementById('output-video');
    var downloadLink = document.getElementById('download-link');

    // Set video source
    video.src = videoPath;

    // Show the video container
    videoContainer.style.display = 'flex';

    // Set download link href
    downloadLink.href = videoPath;
}


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

// Check if user is logged in when the page loads
checkLoginStatus();

// Function to check login status
function checkLoginStatus() {
    fetch('/check_login_status')
    .then(response => response.json())
    .then(data => {
        if (!data.logged_in) {
            // If user is not logged in, redirect to login page
            window.location.href = '/login';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    });
}
