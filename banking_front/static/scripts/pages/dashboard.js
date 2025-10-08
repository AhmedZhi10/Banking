// --- DOM Element Selection ---
const profileNameEl = document.getElementById('profile-name');
const profileEmailEl = document.getElementById('profile-email');
const profileNationalIdEl = document.getElementById('profile-national-id');
const accountsListEl = document.getElementById('accounts-list');
const logoutBtn = document.getElementById('logout-btn');

// Modal Elements
const transactionsModal = document.getElementById('transactions-modal');
const closeModalBtn = document.getElementById('close-modal-btn');
const modalAccountNumberEl = document.getElementById('modal-account-number');
const transactionsHistoryListEl = document.getElementById('transactions-history-list');
const newTransactionForm = document.getElementById('new-transaction-form');
const transactionAccountIdInput = document.getElementById('transaction-account-id');
const transactionMessageArea = document.getElementById('transaction-message-area');


// --- Main Functions ---

function handleLogout() {
    localStorage.removeItem('accessToken');
    window.location.href = 'login.html';
}

function renderProfile(user) {
    profileNameEl.textContent = `${user.first_name || ''} ${user.last_name || ''}`;
    profileEmailEl.textContent = user.email;
    profileNationalIdEl.textContent = user.national_id;
}

function renderAccounts(accounts) {
    accountsListEl.innerHTML = '';
    if (accounts.length === 0) {
        accountsListEl.innerHTML = '<p class="text-gray-500 text-center col-span-full">You have no bank accounts yet.</p>';
        return;
    }

    accounts.forEach(acc => {
        const accountCard = `
            <div class="p-6 border rounded-lg bg-white shadow-sm flex flex-col justify-between">
                <div>
                    <div class="flex justify-between items-center">
                        <p class="font-bold text-lg text-blue-600">${acc.account_type}</p>
                        <p class="text-sm text-white px-2 py-1 rounded-full ${acc.status === 'Active' ? 'bg-green-500' : 'bg-red-500'}">${acc.status}</p>
                    </div>
                    <p class="text-gray-600 mt-2 text-sm">A/N: ${acc.account_number}</p>
                    <p class="text-3xl font-bold text-gray-800 mt-1">${acc.balance} <span class="text-xl font-normal">EGP</span></p>
                </div>
                <button data-account-id="${acc.id}" data-account-number="${acc.account_number}" class="view-transactions-btn mt-4 w-full bg-gray-200 text-gray-800 font-semibold py-2 px-4 rounded-lg hover:bg-gray-300 transition duration-300">
                    View Transactions
                </button>
            </div>
        `;
        accountsListEl.innerHTML += accountCard;
    });

    // Add event listeners to the new buttons
    document.querySelectorAll('.view-transactions-btn').forEach(button => {
        button.addEventListener('click', () => {
            const accountId = button.dataset.accountId;
            const accountNumber = button.dataset.accountNumber;
            openTransactionsModal(accountId, accountNumber);
        });
    });
}

async function openTransactionsModal(accountId, accountNumber) {
    modalAccountNumberEl.textContent = `For Account: ${accountNumber}`;
    transactionAccountIdInput.value = accountId;
    transactionsHistoryListEl.innerHTML = '<p class="text-center text-gray-500">Loading history...</p>';
    transactionsModal.classList.remove('hidden');

    // Fetch and render transactions
    try {
        const token = localStorage.getItem('accessToken');
        const transactions = await apiFetchTransactionsForAccount(accountId, token);
        renderTransactions(transactions);
    } catch (error) {
        transactionsHistoryListEl.innerHTML = `<p class="text-center text-red-500">${error.message}</p>`;
    }
}

function renderTransactions(transactions) {
    transactionsHistoryListEl.innerHTML = '';
    if (transactions.length === 0) {
        transactionsHistoryListEl.innerHTML = '<p class="text-center text-gray-500">No transactions found for this account.</p>';
        return;
    }

    transactions.sort((a, b) => new Date(b.transaction_date) - new Date(a.transaction_date));

    transactions.forEach(tx => {
        const isDeposit = parseFloat(tx.amount) >= 0;
        const transactionItem = `
            <div class="flex justify-between items-center p-3 rounded-lg ${isDeposit ? 'bg-green-50' : 'bg-red-50'}">
                <div>
                    <p class="font-semibold">${isDeposit ? 'Deposit' : 'Withdrawal'}</p>
                    <p class="text-sm text-gray-500">${new Date(tx.transaction_date).toLocaleString()}</p>
                </div>
                <p class="font-bold text-lg ${isDeposit ? 'text-green-600' : 'text-red-600'}">
                    ${isDeposit ? '+' : ''}${tx.amount} EGP
                </p>
            </div>
        `;
        transactionsHistoryListEl.innerHTML += transactionItem;
    });
}

async function handleNewTransaction(event) {
    event.preventDefault();
    const token = localStorage.getItem('accessToken');
    const accountId = transactionAccountIdInput.value;
    const type = document.getElementById('transaction-type').value;
    let amount = parseFloat(document.getElementById('transaction-amount').value);

    if (type === 'withdrawal') {
        amount = -amount; // Make amount negative for withdrawals
    }

    const payload = { account_id: parseInt(accountId), amount };

    try {
        await apiCreateTransaction(payload, token);
        showMessage('Transaction successful!', false, transactionMessageArea);
        newTransactionForm.reset();

        // Refresh transactions list and accounts list
        const transactions = await apiFetchTransactionsForAccount(accountId, token);
        renderTransactions(transactions);

        const accounts = await apiFetchAccounts(token);
        renderAccounts(accounts);

    } catch (error) {
        showMessage(error.message, true, transactionMessageArea);
    }
}


// --- Initial Page Load ---
document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('accessToken');
    if (!token) {
        handleLogout(); // Redirect to login if no token
        return;
    }

    try {
        // Fetch and render initial data
        const user = await apiFetchProfile(token);
        renderProfile(user);

        const accounts = await apiFetchAccounts(token);
        renderAccounts(accounts);

        // Setup main event listeners
        logoutBtn.addEventListener('click', handleLogout);
        closeModalBtn.addEventListener('click', () => transactionsModal.classList.add('hidden'));
        newTransactionForm.addEventListener('submit', handleNewTransaction);

    } catch (error) {
        // If token is invalid or expired
        handleLogout();
    }
});
