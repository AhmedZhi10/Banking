document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('register-form');

    if (registerForm) {
        registerForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            hideMessage();
            const payload = {
                email: document.getElementById('register-email').value,
                password: document.getElementById('register-password').value,
                first_name: document.getElementById('register-first-name').value,
                last_name: document.getElementById('register-last-name').value,
                national_id: document.getElementById('register-national-id').value,
            };

            try {
                await apiRegister(payload);
                // Redirect to login page with a success message indicator
                window.location.href = 'login.html?registered=true';
            } catch (error) {
                showMessage(error.message, true);
            }
        });
    }
});

