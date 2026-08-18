document.addEventListener('DOMContentLoaded', () => {
    const reminderForm = document.getElementById('reminder-form');

    if (reminderForm) {
        reminderForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const formData = new FormData(reminderForm);
            const payload = Object.fromEntries(
                Array.from(formData.entries()).map(([key, value]) => [key, String(value).trim()])
            );

            if (!payload.medicine_name || !payload.time) {
                window.showToast('Please fill in the medicine name and time.', 'warning');
                return;
            }

            try {
                const response = await fetch('/reminders', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                const result = await response.json().catch(() => ({}));
                if (!response.ok) throw new Error(result.detail || 'Unable to create reminder.');

                window.showToast('Reminder added successfully.', 'success');
                reminderForm.reset();
                const panel = document.getElementById('reminder-form-panel');
                if (panel && window.bootstrap) {
                    const collapse = window.bootstrap.Collapse.getInstance(panel) || new window.bootstrap.Collapse(panel, { toggle: false });
                    collapse.hide();
                }
                setTimeout(() => window.location.reload(), 400);
            } catch (error) {
                window.showToast(error.message || 'Unable to create reminder.', 'error');
            }
        });
    }

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
                setTimeout(() => window.location.reload(), 300);
            } catch (error) {
                window.showToast(error.message, 'error');
            }
        });
    });
});
