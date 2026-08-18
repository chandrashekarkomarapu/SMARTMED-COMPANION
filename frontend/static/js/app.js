document.addEventListener('DOMContentLoaded', () => {
    const toastContainer = document.getElementById('toast-container');
    window.showToast = function (message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        toastContainer.appendChild(toast);
        setTimeout(() => toast.remove(), 3000);
    };
    document.querySelector('.mobile-menu-btn')?.addEventListener('click', () => {
        document.querySelector('.sidebar').classList.toggle('open');
    });
});
