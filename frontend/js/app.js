// ========== Voxtral PWA - Main Application ==========

// API Configuration
const API_BASE = window.location.origin;
const API_HEALTH = `${API_BASE}/health`;
const API_TRANSCRIBE = `${API_BASE}/api/transcribe`;

// State Management
const state = {
    isRecording: false,
    mediaRecorder: null,
    audioChunks: [],
    recordingStartTime: null,
    timerInterval: null,
    currentBlob: null,
    serverOnline: false,
    modelLoaded: false
};

// DOM Elements
const elements = {
    btnRecord: document.getElementById('btnRecord'),
    btnStop: document.getElementById('btnStop'),
    btnTranscribe: document.getElementById('btnTranscribe'),
    btnCopy: document.getElementById('btnCopy'),
    btnClearHistory: document.getElementById('btnClearHistory'),
    recordText: document.getElementById('recordText'),
    timeDisplay: document.getElementById('timeDisplay'),
    waveform: document.getElementById('waveform'),
    transcriptionBox: document.getElementById('transcriptionBox'),
    loading: document.getElementById('loading'),
    loadingText: document.getElementById('loadingText'),
    serverStatus: document.getElementById('serverStatus'),
    modelStatus: document.getElementById('modelStatus'),
    historyList: document.getElementById('historyList'),
    toast: document.getElementById('toast')
};

// ========== Utility Functions ==========

function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}

function showToast(message, type = 'info') {
    elements.toast.textContent = message;
    elements.toast.className = `toast show ${type}`;

    setTimeout(() => {
        elements.toast.classList.remove('show');
    }, 3000);
}

function updateUI() {
    // Update button states
    elements.btnRecord.disabled = !state.serverOnline || state.isRecording;
    elements.btnStop.disabled = !state.isRecording;
    elements.btnTranscribe.disabled = !state.currentBlob || state.isRecording;

    // Update recording button
    if (state.isRecording) {
        elements.btnRecord.classList.add('recording');
        elements.recordText.textContent = 'Grabando...';
    } else {
        elements.btnRecord.classList.remove('recording');
        elements.recordText.textContent = 'Grabar';
    }
}

// ========== Server Health Check ==========

async function checkServerHealth() {
    try {
        const response = await fetch(API_HEALTH);
        const data = await response.json();

        state.serverOnline = data.status === 'ok';
        state.modelLoaded = data.model_loaded;

        elements.serverStatus.textContent = state.serverOnline ? 'Online' : 'Offline';
        elements.serverStatus.className = `status-value ${state.serverOnline ? 'online' : 'offline'}`;

        elements.modelStatus.textContent = state.modelLoaded ? 'Cargado' : 'No cargado';
        elements.modelStatus.className = `status-value ${state.modelLoaded ? 'loaded' : 'error'}`;

        if (!state.modelLoaded && state.serverOnline) {
            showToast('Servidor online pero modelo no cargado. Revisa la configuración.', 'warning');
        }
    } catch (error) {
        console.error('Error checking server health:', error);
        state.serverOnline = false;
        elements.serverStatus.textContent = 'Offline';
        elements.serverStatus.className = 'status-value offline';
        elements.modelStatus.textContent = '-';
        showToast('No se puede conectar al servidor local', 'error');
    }

    updateUI();
}

// ========== Audio Recording ==========

async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

        // Use appropriate MIME type
        const mimeType = MediaRecorder.isTypeSupported('audio/webm') ? 'audio/webm' : 'audio/mp4';
        state.mediaRecorder = new MediaRecorder(stream, { mimeType });

        state.audioChunks = [];
        state.recordingStartTime = Date.now();

        state.mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                state.audioChunks.push(event.data);
            }
        };

        state.mediaRecorder.onstop = async () => {
            const blob = new Blob(state.audioChunks, { type: mimeType });
            state.currentBlob = blob;

            // Stop all tracks
            stream.getTracks().forEach(track => track.stop());

            showToast(`Audio grabado: ${(blob.size / 1024).toFixed(1)} KB`, 'success');
            updateUI();
        };

        state.mediaRecorder.start();
        state.isRecording = true;

        // Start timer
        startTimer();

        // Animate waveform
        elements.waveform.classList.add('active');

        updateUI();
        showToast('Grabación iniciada', 'success');

    } catch (error) {
        console.error('Error starting recording:', error);
        showToast('Error al acceder al micrófono. Verifica los permisos.', 'error');
    }
}

function stopRecording() {
    if (state.mediaRecorder && state.isRecording) {
        state.mediaRecorder.stop();
        state.isRecording = false;

        // Stop timer
        stopTimer();

        // Stop waveform animation
        elements.waveform.classList.remove('active');

        updateUI();
    }
}

function startTimer() {
    let seconds = 0;
    elements.timeDisplay.textContent = formatTime(seconds);

    state.timerInterval = setInterval(() => {
        seconds++;
        elements.timeDisplay.textContent = formatTime(seconds);
    }, 1000);
}

function stopTimer() {
    if (state.timerInterval) {
        clearInterval(state.timerInterval);
        state.timerInterval = null;
    }
}

// ========== Transcription ==========

async function transcribeAudio() {
    if (!state.currentBlob) {
        showToast('No hay audio para transcribir', 'error');
        return;
    }

    try {
        // Show loading
        elements.loading.classList.add('active');
        elements.loadingText.textContent = 'Transcribiendo audio...';
        elements.btnTranscribe.disabled = true;

        // Convert audio to WAV format if needed
        const audioBlob = await convertToWav(state.currentBlob);

        // Create FormData
        const formData = new FormData();
        formData.append('audio', audioBlob, 'recording.wav');

        // Send to API
        const response = await fetch(API_TRANSCRIBE, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();

        if (data.success) {
            // Display transcription
            displayTranscription(data.text);

            // Save to history
            saveToHistory(data.text);

            showToast('Transcripción completada', 'success');
        } else {
            throw new Error(data.error || 'Error desconocido');
        }

    } catch (error) {
        console.error('Error transcribing:', error);
        showToast(`Error al transcribir: ${error.message}`, 'error');
    } finally {
        // Hide loading
        elements.loading.classList.remove('active');
        updateUI();
    }
}

async function convertToWav(blob) {
    // For now, just return the blob
    // In production, you might want to convert to proper WAV format
    // using Web Audio API or a library like audiobuffer-to-wav
    return blob;
}

function displayTranscription(text) {
    if (text && text.trim()) {
        elements.transcriptionBox.innerHTML = `<p>${escapeHtml(text)}</p>`;
        elements.btnCopy.disabled = false;
    } else {
        elements.transcriptionBox.innerHTML = '<p class="placeholder">La transcripción está vacía</p>';
        elements.btnCopy.disabled = true;
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ========== Clipboard ==========

async function copyToClipboard() {
    const text = elements.transcriptionBox.textContent;

    if (!text || text.trim() === '') {
        showToast('No hay texto para copiar', 'error');
        return;
    }

    try {
        await navigator.clipboard.writeText(text);
        showToast('Texto copiado al portapapeles', 'success');
    } catch (error) {
        console.error('Error copying to clipboard:', error);
        showToast('Error al copiar texto', 'error');
    }
}

// ========== History Management ==========

function loadHistory() {
    try {
        const history = JSON.parse(localStorage.getItem('transcriptionHistory') || '[]');
        displayHistory(history);
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

function saveToHistory(text) {
    try {
        const history = JSON.parse(localStorage.getItem('transcriptionHistory') || '[]');

        const item = {
            text: text,
            timestamp: Date.now(),
            date: new Date().toLocaleString('es-ES')
        };

        history.unshift(item); // Add to beginning

        // Keep only last 20 items
        if (history.length > 20) {
            history.pop();
        }

        localStorage.setItem('transcriptionHistory', JSON.stringify(history));
        displayHistory(history);
    } catch (error) {
        console.error('Error saving to history:', error);
    }
}

function displayHistory(history) {
    if (!history || history.length === 0) {
        elements.historyList.innerHTML = '<p class="placeholder">No hay transcripciones guardadas</p>';
        return;
    }

    elements.historyList.innerHTML = history.map((item, index) => `
        <div class="history-item" onclick="loadHistoryItem(${index})">
            <div class="history-item-time">${item.date}</div>
            <div class="history-item-text">${escapeHtml(item.text)}</div>
        </div>
    `).join('');
}

function loadHistoryItem(index) {
    try {
        const history = JSON.parse(localStorage.getItem('transcriptionHistory') || '[]');
        const item = history[index];

        if (item) {
            displayTranscription(item.text);
            showToast('Transcripción cargada del historial', 'success');

            // Scroll to transcription
            elements.transcriptionBox.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    } catch (error) {
        console.error('Error loading history item:', error);
    }
}

function clearHistory() {
    if (confirm('¿Estás seguro de que quieres borrar todo el historial?')) {
        localStorage.removeItem('transcriptionHistory');
        displayHistory([]);
        showToast('Historial borrado', 'success');
    }
}

// ========== Event Listeners ==========

elements.btnRecord.addEventListener('click', startRecording);
elements.btnStop.addEventListener('click', stopRecording);
elements.btnTranscribe.addEventListener('click', transcribeAudio);
elements.btnCopy.addEventListener('click', copyToClipboard);
elements.btnClearHistory.addEventListener('click', clearHistory);

// Make loadHistoryItem available globally
window.loadHistoryItem = loadHistoryItem;

// ========== Service Worker Registration ==========

if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('Service Worker registered:', registration);
            })
            .catch(error => {
                console.log('Service Worker registration failed:', error);
            });
    });
}

// ========== Initialization ==========

async function init() {
    console.log('Initializing Voxtral PWA...');

    // Check server health
    await checkServerHealth();

    // Load history
    loadHistory();

    // Check server health periodically
    setInterval(checkServerHealth, 30000); // Every 30 seconds

    console.log('Voxtral PWA ready!');
}

// Start the app
init();
