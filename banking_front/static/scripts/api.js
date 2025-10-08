// --- API Base URLs ---
const DJANGO_API_BASE_URL = 'http://127.0.0.1:8000';
const FASTAPI_API_BASE_URL = 'http://127.0.0.1:8001'; // <-- New base URL for microservice

// --- Django Endpoints ---
const LOGIN_URL = `${DJANGO_API_BASE_URL}/api/token/`;
const REGISTER_URL = `${DJANGO_API_BASE_URL}/api/auth/register/`;
const PROFILE_URL = `${DJANGO_API_BASE_URL}/api/auth/me/`;
const ACCOUNTS_URL = `${DJANGO_API_BASE_URL}/api/account/`;

// --- FastAPI Endpoints ---
const TRANSACTIONS_URL = `${FASTAPI_API_BASE_URL}/transactions/`; // <-- New endpoint


// --- Authentication API Functions (Django) ---
async function apiLogin(email, password) {
    const response = await fetch(LOGIN_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });
    const data = await response.json();
    if (!response.ok) {
        throw new Error(data.detail || 'Login failed.');
    }
    return data;
}

async function apiRegister(payload) {
    const response = await fetch(REGISTER_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });
    const data = await response.json();
    if (!response.ok) {
        const errorMessages = Object.entries(data).map(([key, value]) => `${key}: ${value.join(', ')}`).join('\n');
        throw new Error(errorMessages || 'Registration failed.');
    }
    return data;
}

// --- User & Account API Functions (Django) ---
async function apiFetchProfile(token) {
    const response = await fetch(PROFILE_URL, {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    if (!response.ok) throw new Error('Session expired.');
    return await response.json();
}

async function apiFetchAccounts(token) {
    const response = await fetch(ACCOUNTS_URL, {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    if (!response.ok) throw new Error('Failed to fetch accounts.');
    return await response.json();
}


// --- Transaction API Functions (FastAPI) ---

async function apiFetchTransactionsForAccount(accountId, token) {
    const response = await fetch(`${TRANSACTIONS_URL}${accountId}`, {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    if (!response.ok) throw new Error('Failed to fetch transactions.');
    return await response.json();
}

async function apiCreateTransaction(payload, token) {
    const response = await fetch(TRANSACTIONS_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(payload)
    });
    const data = await response.json();
    if (!response.ok) {
        throw new Error(data.detail || 'Transaction failed.');
    }
    return data;
}
