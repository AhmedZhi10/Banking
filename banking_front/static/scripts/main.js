// This file contains shared functions for manipulating the DOM.

/**
 * Displays a message in the message area.
 * @param {string} message - The message to display.
 * @param {boolean} isError - If true, styles the message as an error.
 */
function showMessage(message, isError = false) {
    const messageArea = document.getElementById('message-area');
    if (!messageArea) return;
    
    messageArea.textContent = message;
    messageArea.classList.remove('hidden', 'bg-red-500', 'bg-green-500');
    messageArea.classList.add(isError ? 'bg-red-500' : 'bg-green-500');
}

/**
 * Hides the message area.
 */
function hideMessage() {
    const messageArea = document.getElementById('message-area');
    if (messageArea) {
        messageArea.classList.add('hidden');
    }
}

/**
 * Logs out the user by clearing storage and redirecting.
 */
function handleLogout() {
    localStorage.removeItem('accessToken');
    window.location.href = 'login.html';
}

