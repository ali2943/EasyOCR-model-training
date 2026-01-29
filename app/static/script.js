// EasyOCR Text Detection JavaScript

// Global state
let uploadedImage = null;
let uploadedImageFile = null;

// DOM Elements
const uploadArea = document.getElementById('upload-area');
const imageInput = document.getElementById('image-input');
const previewSection = document.getElementById('preview-section');
const previewImage = document.getElementById('preview-image');
const detectBtn = document.getElementById('detect-btn');
const clearBtn = document.getElementById('clear-btn');
const resultsSection = document.getElementById('results-section');
const loadingSection = document.getElementById('loading-section');
const resultCanvas = document.getElementById('result-canvas');
const detectedTextList = document.getElementById('detected-text-list');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
});

// Event Listeners
function initializeEventListeners() {
    // Click to upload
    uploadArea.addEventListener('click', () => {
        imageInput.click();
    });
    
    // File selection
    imageInput.addEventListener('change', handleImageSelect);
    
    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#4a90e2';
        uploadArea.style.backgroundColor = '#f0f8ff';
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.style.borderColor = '#ddd';
        uploadArea.style.backgroundColor = '#fafafa';
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#ddd';
        uploadArea.style.backgroundColor = '#fafafa';
        
        if (e.dataTransfer.files.length > 0) {
            const file = e.dataTransfer.files[0];
            if (file.type.startsWith('image/')) {
                handleFile(file);
            } else {
                alert('Please upload an image file');
            }
        }
    });
    
    // Detect button
    detectBtn.addEventListener('click', handleDetect);
    
    // Clear button
    clearBtn.addEventListener('click', handleClear);
}

function handleImageSelect(event) {
    const file = event.target.files[0];
    if (file) {
        handleFile(file);
    }
}

function handleFile(file) {
    uploadedImageFile = file;
    
    const reader = new FileReader();
    reader.onload = (e) => {
        uploadedImage = e.target.result;
        previewImage.src = uploadedImage;
        uploadArea.style.display = 'none';
        previewSection.style.display = 'block';
        resultsSection.style.display = 'none';
    };
    reader.readAsDataURL(file);
}

function handleClear() {
    uploadedImage = null;
    uploadedImageFile = null;
    imageInput.value = '';
    uploadArea.style.display = 'block';
    previewSection.style.display = 'none';
    resultsSection.style.display = 'none';
}

async function handleDetect() {
    if (!uploadedImageFile) {
        alert('Please select an image first');
        return;
    }
    
    // Show loading
    loadingSection.style.display = 'block';
    resultsSection.style.display = 'none';
    detectBtn.disabled = true;
    
    try {
        const formData = new FormData();
        formData.append('file', uploadedImageFile);
        
        const response = await fetch('/api/detect', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Detection failed');
        }
        
        const data = await response.json();
        displayResults(data);
        
    } catch (error) {
        console.error('Detection error:', error);
        alert(`Failed to detect text: ${error.message}`);
    } finally {
        loadingSection.style.display = 'none';
        detectBtn.disabled = false;
    }
}

function displayResults(data) {
    resultsSection.style.display = 'block';
    
    // Draw bounding boxes on canvas
    const img = new Image();
    img.onload = () => {
        const canvas = resultCanvas;
        const ctx = canvas.getContext('2d');
        
        // Set canvas size to match image
        canvas.width = img.width;
        canvas.height = img.height;
        
        // Draw the image
        ctx.drawImage(img, 0, 0);
        
        // Draw bounding boxes
        ctx.strokeStyle = '#00ff00';
        ctx.lineWidth = 3;
        ctx.font = '16px Arial';
        ctx.fillStyle = '#00ff00';
        
        data.results.forEach((result, index) => {
            const bbox = result.bbox;
            
            // Draw rectangle
            const minX = Math.min(...bbox.map(p => p[0]));
            const minY = Math.min(...bbox.map(p => p[1]));
            const maxX = Math.max(...bbox.map(p => p[0]));
            const maxY = Math.max(...bbox.map(p => p[1]));
            
            ctx.strokeRect(minX, minY, maxX - minX, maxY - minY);
            
            // Draw index number
            ctx.fillText(`${index + 1}`, minX, minY - 5);
        });
    };
    img.src = uploadedImage;
    
    // Display detected text list
    let html = '';
    if (data.results.length === 0) {
        html = '<p style="color: #666;">No text detected in the image.</p>';
    } else {
        html = '<div class="text-results">';
        data.results.forEach((result, index) => {
            const confidence = (result.confidence * 100).toFixed(2);
            html += `
                <div class="text-item">
                    <div class="text-number">${index + 1}</div>
                    <div class="text-content">
                        <div class="text-value">${result.text}</div>
                        <div class="text-confidence">Confidence: ${confidence}%</div>
                    </div>
                </div>
            `;
        });
        html += '</div>';
    }
    detectedTextList.innerHTML = html;
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}
