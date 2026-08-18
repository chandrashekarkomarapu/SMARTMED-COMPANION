document.addEventListener('DOMContentLoaded', () => {
    if (!('Notification' in window)) {
        if (window.showToast) {
            window.showToast('Browser notifications are not supported. Please check the reminder schedule manually.', 'warning');
        }
        return;
    }
    if (Notification.permission === 'default') {
        Notification.requestPermission().catch(() => {
            if (window.showToast) {
                window.showToast('Browser notifications are not supported. Please check the reminder schedule manually.', 'warning');
            }
        });
    }
});
