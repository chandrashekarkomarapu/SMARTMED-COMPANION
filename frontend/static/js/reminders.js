document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-action]').forEach((button) => {
        button.addEventListener('click', async () => {
            const reminderId = button.dataset.reminderId;
            const action = button.dataset.action;
            const endpoint = action === 'taken' ? `/reminders/${reminderId}/taken` : `/reminders/${reminderId}/missed`;
            try {
                const response = await fetch(endpoint, { method: 'POST' });
                const result = await response.json();
                if (!response.ok) throw new Error(result.detail || 'Unable to update reminder.');
                window.showToast(result.message || 'Reminder updated.', 'success');
            } catch (error) {
                window.showToast(error.message, 'error');
            }
        });
    });
});
