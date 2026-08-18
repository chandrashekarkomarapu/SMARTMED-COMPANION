document.addEventListener('DOMContentLoaded', () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const voiceButton = document.getElementById('voice-button');
    const readButtons = document.querySelectorAll('[data-speech]');

    if (SpeechRecognition) {
        const recognition = new SpeechRecognition();
        recognition.lang = 'en-US';
        recognition.interimResults = false;
        recognition.continuous = false;
        if (voiceButton) {
            voiceButton.addEventListener('click', () => {
                recognition.start();
                voiceButton.textContent = 'Listening...';
            });
        }
        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            const input = document.querySelector('input[type="search"]');
            if (input) input.value = transcript;
            if (window.showToast) window.showToast('Voice input captured.', 'success');
        };
        recognition.onerror = () => {
            if (window.showToast) window.showToast('Voice input is not supported by this browser. Please use text input.', 'warning');
        };
    } else if (window.showToast) {
        window.showToast('Voice input is not supported by this browser. Please use text input.', 'warning');
    }

    readButtons.forEach((button) => {
        button.addEventListener('click', () => {
            const text = button.dataset.speech || '';
            if (!text) return;
            if ('speechSynthesis' in window) {
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = 'en-US';
                window.speechSynthesis.cancel();
                window.speechSynthesis.speak(utterance);
            }
        });
    });
});
