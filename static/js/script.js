const API_BASE_URL = ''; // FastAPI serves from root

document.addEventListener('DOMContentLoaded', () => {
    checkLoginStatus();

    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }
});

function showLogin() {
    document.getElementById('login-section').style.display = 'block';
    document.getElementById('register-section').style.display = 'none';
}

function showRegister() {
    document.getElementById('login-section').style.display = 'none';
    document.getElementById('register-section').style.display = 'block';
}

async function handleLogin(event) {
    event.preventDefault();
    const username = event.target.username.value;
    const password = event.target.password.value;
    const errorP = document.getElementById('login-error');
    errorP.textContent = '';

    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    try {
        const response = await fetch(`${API_BASE_URL}/auth/token`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData,
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        localStorage.setItem('accessToken', data.access_token);
        await fetchUserDetails(); // Fetch user details and store role
        window.location.href = '/ui/products'; // Redirect to a protected page
    } catch (error) {
        console.error('Login failed:', error);
        errorP.textContent = `Login failed: ${error.message}`;
    }
}

async function handleRegister(event) {
    event.preventDefault();
    const username = event.target.username.value;
    const password = event.target.password.value;
    const role = event.target.role.value;
    const errorP = document.getElementById('register-error');
    const successP = document.getElementById('register-success');
    errorP.textContent = '';
    successP.textContent = '';

    try {
        const response = await fetch(`${API_BASE_URL}/auth/users/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password, role }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }
        const newUser = await response.json();
        successP.textContent = `User "${newUser.username}" registered successfully! You can now login.`;
        event.target.reset();
        showLogin(); // Show login form after successful registration
    } catch (error) {
        console.error('Registration failed:', error);
        errorP.textContent = `Registration failed: ${error.message}`;
    }
}


async function fetchUserDetails() {
    const token = localStorage.getItem('accessToken');
    if (!token) return;

    try {
        const response = await fetch(`${API_BASE_URL}/auth/users/me/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) {
            // If fetching user details fails (e.g. token expired), clear token and update UI
            if (response.status === 401) {
                logout();
            }
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const user = await response.json();
        localStorage.setItem('username', user.username);
        localStorage.setItem('userRole', user.role);
        updateAuthUI(user.username, user.role);
    } catch (error) {
        console.error('Error fetching user details:', error);
        // Don't clear token here necessarily unless it's a 401,
        // as it might be a temporary network issue.
        // The checkLoginStatus will handle UI updates if token is still there but invalid later.
    }
}

function updateAuthUI(username, role) {
    const authLinks = document.getElementById('auth-links');
    const userInfo = document.getElementById('user-info');
    const usernameDisplay = document.getElementById('username-display');
    const userRoleDisplay = document.getElementById('user-role-display');

    if (username && role) {
        if (authLinks) authLinks.style.display = 'none';
        if (userInfo) userInfo.style.display = 'inline'; // or 'block' depending on layout
        if (usernameDisplay) usernameDisplay.textContent = username;
        if (userRoleDisplay) userRoleDisplay.textContent = role;
    } else {
        if (authLinks) authLinks.style.display = 'inline';
        if (userInfo) userInfo.style.display = 'none';
    }
}

function checkLoginStatus() {
    const token = localStorage.getItem('accessToken');
    const username = localStorage.getItem('username');
    const role = localStorage.getItem('userRole');

    if (token && username && role) {
        updateAuthUI(username, role);
        // It's a good idea to verify the token with the backend here if the app is sensitive,
        // but for simplicity, we're relying on stored details.
        // fetchUserDetails(); // Optionally re-fetch to confirm token validity and get fresh details
    } else {
        updateAuthUI(null, null);
    }
}


function logout() {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('username');
    localStorage.removeItem('userRole');
    updateAuthUI(null, null);
    // Hide sections that require auth
    const addProductSection = document.getElementById('add-product-section');
    if (addProductSection) addProductSection.style.display = 'none';

    const productHistorySection = document.getElementById('product-history-section');
    if (productHistorySection) productHistorySection.style.display = 'none';

    const addEventSection = document.getElementById('add-event-section');
    if (addEventSection) addEventSection.style.display = 'none';

    // Redirect to home or login page
    if (window.location.pathname !== '/') {
        window.location.href = '/';
    } else {
        showLogin(); // If on homepage, just show login form
    }
}