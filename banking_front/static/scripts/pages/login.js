document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    // Check if the user just registered successfully
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('registered') === 'true') {
        showMessage('Registration successful! Please log in.');
    }

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            hideMessage();
            const email = document.getElementById('login-email').value;
            const password = document.getElementById('login-password').value;

            try {
                const data = await apiLogin(email, password);
                localStorage.setItem('accessToken', data.access);
                window.location.href = 'dashboard.html';
            } catch (error) {
                showMessage(error.message, true);
            }
        });
    }
});

