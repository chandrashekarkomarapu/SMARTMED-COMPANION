document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('prescription-file');
    const browseButton = document.getElementById('browse-button');
    const scanButton = document.getElementById('scan-button');
    const removeButton = document.getElementById('remove-file-button');
    const dropzone = document.getElementById('dropzone');
    const filePreview = document.getElementById('file-preview');
    const ocrStatus = document.getElementById('ocr-status');
    const ocrOutput = document.getElementById('ocr-output');
    const form = document.getElementById('confirmation-form');

    browseButton.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', () => {
        const file = fileInput.files[0];
        if (file) {
            filePreview.textContent = file.name;
            filePreview.classList.remove('hidden');
        }
    });

    dropzone.addEventListener('dragover', (event) => {
        event.preventDefault();
        dropzone.style.borderColor = '#1d7aaa';
    });
    dropzone.addEventListener('drop', (event) => {
        event.preventDefault();
        const file = event.dataTransfer.files[0];
        if (file) {
            fileInput.files = event.dataTransfer.files;
            filePreview.textContent = file.name;
            filePreview.classList.remove('hidden');
        }
    });
    removeButton.addEventListener('click', () => {
        fileInput.value = '';
        filePreview.classList.add('hidden');
        ocrOutput.textContent = 'No prescription scanned yet.';
        ocrStatus.textContent = 'Waiting for file';
        ocrStatus.className = 'status-pill info';
    });

    scanButton.addEventListener('click', async () => {
        const file = fileInput.files[0];
        if (!file) {
            window.showToast('Please select a prescription file first.', 'warning');
            return;
        }
        ocrStatus.textContent = 'Scanning...';
        ocrStatus.className = 'status-pill info';
        const formData = new FormData();
        formData.append('file', file);
        try {
            const response = await fetch('/prescriptions/upload', { method: 'POST', body: formData });
            const result = await response.json();
            if (!response.ok) throw new Error(result.detail || 'Unable to read the prescription.');
            ocrStatus.textContent = `OCR Confidence: ${result.confidence}`;
            ocrStatus.className = result.confidence >= 60 ? 'status-pill success' : 'status-pill warning';
            ocrOutput.textContent = result.text || 'No readable text found.';
            const parsed = result.parsed || {};
            form.elements.medicine_name.value = parsed.medicine_name || '';
            form.elements.strength.value = parsed.strength || '';
            form.elements.frequency.value = parsed.frequency || '';
            form.elements.duration.value = parsed.duration || '';
            form.elements.instructions.value = parsed.instructions || '';
            if (parsed.frequency === 'Uncertain') {
                form.elements.frequency.style.border = '2px solid #f3b15d';
            }
        } catch (error) {
            ocrStatus.textContent = 'OCR failed';
            ocrStatus.className = 'status-pill danger';
            ocrOutput.textContent = error.message || 'Unable to read the prescription. Please try a clearer image.';
            window.showToast(error.message, 'error');
        }
    });

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const values = Object.fromEntries(new FormData(form).entries());
        if (!values.medicine_name) {
            window.showToast('Please confirm at least the medicine name before saving.', 'warning');
            return;
        }
        try {
            const response = await fetch('/prescriptions/confirm', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: new URLSearchParams({
                    prescription_id: '1',
                    medicine_name: values.medicine_name,
                    strength: values.strength,
                    frequency: values.frequency,
                    duration: values.duration,
                    instructions: values.instructions,
                })
            });
            const result = await response.json();
            if (!response.ok) throw new Error(result.detail || 'Unable to confirm prescription.');
            window.showToast('Prescription confirmed and saved.', 'success');
        } catch (error) {
            window.showToast(error.message, 'error');
        }
    });
});
