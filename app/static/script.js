// EasyOCR Training Dashboard JavaScript

// Global state
let statusPollInterval = null;
let currentDatasetPath = null;

// DOM Elements
const sampleDatasetRadio = document.getElementById('sample-dataset');
const uploadDatasetRadio = document.getElementById('upload-dataset');
const uploadForm = document.getElementById('upload-form');
const sampleInfo = document.getElementById('sample-info');
const uploadBtn = document.getElementById('upload-btn');
const trainBtn = document.getElementById('train-btn');
const resetBtn = document.getElementById('reset-btn');
const imagesInput = document.getElementById('images-input');
const labelsInput = document.getElementById('labels-input');
const languagesInput = document.getElementById('languages');
const gpuCheckbox = document.getElementById('gpu-checkbox');

// Status elements
const statusValue = document.getElementById('status-value');
const messageValue = document.getElementById('message-value');
const progressFill = document.getElementById('progress-fill');
const progressValue = document.getElementById('progress-value');

// Results elements
const resultsSection = document.getElementById('results-section');
const accuracyValue = document.getElementById('accuracy-value');
const totalSamplesValue = document.getElementById('total-samples-value');
const correctPredictionsValue = document.getElementById('correct-predictions-value');
const resultsTable = document.getElementById('results-table');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    loadSampleDatasetInfo();
    checkHealth();
});

// Event Listeners
function initializeEventListeners() {
    sampleDatasetRadio.addEventListener('change', handleDatasetChange);
    uploadDatasetRadio.addEventListener('change', handleDatasetChange);
    uploadBtn.addEventListener('click', handleUpload);
    trainBtn.addEventListener('click', handleTrain);
    resetBtn.addEventListener('click', handleReset);
}

function handleDatasetChange() {
    if (sampleDatasetRadio.checked) {
        uploadForm.style.display = 'none';
        sampleInfo.style.display = 'block';
        currentDatasetPath = null;
    } else {
        uploadForm.style.display = 'block';
        sampleInfo.style.display = 'none';
    }
}

// API Functions
async function checkHealth() {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        console.log('Health check:', data);
    } catch (error) {
        console.error('Health check failed:', error);
        showMessage('Failed to connect to API server', 'error');
    }
}

async function loadSampleDatasetInfo() {
    const previewDiv = document.getElementById('sample-preview');
    
    try {
        const response = await fetch('/api/sample-dataset');
        const data = await response.json();
        
        let html = `<p><strong>Sample Count:</strong> ${data.sample_count}</p>`;
        html += '<div style="margin-top: 10px;">';
        
        data.samples.forEach(sample => {
            html += `
                <div class="sample-item">
                    <strong>${sample.filename}:</strong> ${sample.text}
                </div>
            `;
        });
        
        html += '</div>';
        previewDiv.innerHTML = html;
        
    } catch (error) {
        console.error('Failed to load sample dataset:', error);
        previewDiv.innerHTML = '<p class="loading">Failed to load sample dataset</p>';
    }
}

async function handleUpload() {
    const images = imagesInput.files;
    const labels = labelsInput.files[0];
    
    if (!images || images.length === 0) {
        alert('Please select at least one image file');
        return;
    }
    
    if (!labels) {
        alert('Please select a labels.txt file');
        return;
    }
    
    uploadBtn.disabled = true;
    uploadBtn.textContent = '📤 Uploading...';
    
    try {
        const formData = new FormData();
        
        // Add all image files
        for (let i = 0; i < images.length; i++) {
            formData.append('files', images[i]);
        }
        
        // Add labels file
        formData.append('labels', labels);
        
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error('Upload failed');
        }
        
        const data = await response.json();
        currentDatasetPath = data.dataset_path;
        
        alert(`Dataset uploaded successfully!\n${data.message}`);
        
        // Clear inputs
        imagesInput.value = '';
        labelsInput.value = '';
        
    } catch (error) {
        console.error('Upload error:', error);
        alert('Failed to upload dataset. Please try again.');
    } finally {
        uploadBtn.disabled = false;
        uploadBtn.textContent = '📤 Upload Dataset';
    }
}

async function handleTrain() {
    // Prepare training request
    const datasetType = sampleDatasetRadio.checked ? 'sample' : 'uploaded';
    
    if (datasetType === 'uploaded' && !currentDatasetPath) {
        alert('Please upload a dataset first');
        return;
    }
    
    const languages = languagesInput.value
        .split(',')
        .map(lang => lang.trim())
        .filter(lang => lang.length > 0);
    
    if (languages.length === 0) {
        alert('Please specify at least one language');
        return;
    }
    
    const requestBody = {
        dataset_type: datasetType,
        dataset_path: currentDatasetPath,
        languages: languages,
        gpu: gpuCheckbox.checked
    };
    
    trainBtn.disabled = true;
    
    try {
        const response = await fetch('/api/train', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Training failed to start');
        }
        
        const data = await response.json();
        console.log('Training started:', data);
        
        // Start polling for status
        startStatusPolling();
        
        // Show reset button
        resetBtn.style.display = 'inline-block';
        
    } catch (error) {
        console.error('Training error:', error);
        alert(`Failed to start training: ${error.message}`);
        trainBtn.disabled = false;
    }
}

async function handleReset() {
    try {
        const response = await fetch('/api/reset', {
            method: 'POST'
        });
        
        if (!response.ok) {
            throw new Error('Reset failed');
        }
        
        // Stop polling
        if (statusPollInterval) {
            clearInterval(statusPollInterval);
            statusPollInterval = null;
        }
        
        // Reset UI
        updateStatusUI({
            status: 'idle',
            message: 'Ready to start training',
            progress: 0
        });
        
        resultsSection.style.display = 'none';
        trainBtn.disabled = false;
        resetBtn.style.display = 'none';
        
    } catch (error) {
        console.error('Reset error:', error);
        alert('Failed to reset training state');
    }
}

function startStatusPolling() {
    // Clear any existing interval
    if (statusPollInterval) {
        clearInterval(statusPollInterval);
    }
    
    // Poll immediately
    pollStatus();
    
    // Then poll every 1 second
    statusPollInterval = setInterval(pollStatus, 1000);
}

async function pollStatus() {
    try {
        const response = await fetch('/api/status');
        const status = await response.json();
        
        updateStatusUI(status);
        
        // Stop polling if training is completed or failed
        if (status.status === 'completed' || status.status === 'failed') {
            if (statusPollInterval) {
                clearInterval(statusPollInterval);
                statusPollInterval = null;
            }
            
            trainBtn.disabled = false;
            
            // Show results if completed
            if (status.status === 'completed' && status.results) {
                displayResults(status.results);
            }
        }
        
    } catch (error) {
        console.error('Status poll error:', error);
    }
}

function updateStatusUI(status) {
    // Update status badge
    statusValue.textContent = status.status.charAt(0).toUpperCase() + status.status.slice(1);
    statusValue.className = 'status-badge status-' + status.status;
    
    // Update message
    messageValue.textContent = status.message || 'No message';
    
    // Update progress
    const progress = status.progress || 0;
    progressFill.style.width = progress + '%';
    progressValue.textContent = progress + '%';
}

function displayResults(results) {
    // Show results section
    resultsSection.style.display = 'block';
    
    // Update summary stats
    accuracyValue.textContent = results.accuracy + '%';
    totalSamplesValue.textContent = results.total_samples;
    correctPredictionsValue.textContent = results.correct_predictions;
    
    // Display detailed results
    let html = '<div class="result-row" style="font-weight: bold; background: var(--primary-color); color: white;">';
    html += '<div>Filename</div>';
    html += '<div>Ground Truth</div>';
    html += '<div>Predicted</div>';
    html += '<div>Status</div>';
    html += '</div>';
    
    if (results.details && results.details.length > 0) {
        results.details.forEach(detail => {
            const statusClass = detail.correct ? 'result-correct' : 'result-incorrect';
            const statusText = detail.correct ? '✓ Correct' : '✗ Wrong';
            
            html += '<div class="result-row">';
            html += `<div><strong>${detail.filename}</strong></div>`;
            html += `<div>${detail.ground_truth}</div>`;
            html += `<div>${detail.predicted}</div>`;
            html += `<div class="${statusClass}">${statusText}</div>`;
            html += '</div>';
        });
    }
    
    resultsTable.innerHTML = html;
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function showMessage(message, type = 'info') {
    // Simple message display (could be enhanced with a toast notification)
    console.log(`[${type.toUpperCase()}] ${message}`);
}
