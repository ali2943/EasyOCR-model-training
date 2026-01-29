// EasyOCR Image Text Recognition - JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const uploadZone = document.getElementById('upload-zone');
    const imageInput = document.getElementById('image-input');
    const processBtn = document.getElementById('process-btn');
    const languagesInput = document.getElementById('languages-input');
    const gpuCheckbox = document.getElementById('gpu-checkbox');
    
    const previewSection = document.getElementById('preview-section');
    const previewImage = document.getElementById('preview-image');
    
    const statusSection = document.getElementById('status-section');
    const processingMessage = document.getElementById('processing-message');
    
    const resultsSection = document.getElementById('results-section');
    const annotatedImage = document.getElementById('annotated-image');
    const detectionsList = document.getElementById('detections-list');
    const totalDetectionsEl = document.getElementById('total-detections');
    const avgConfidenceEl = document.getElementById('avg-confidence');
    
    const copyTextBtn = document.getElementById('copy-text-btn');
    const newImageBtn = document.getElementById('new-image-btn');
    
    let selectedFile = null;
    let currentResults = null;
    
    // Upload Zone Click Handler
    uploadZone.addEventListener('click', () => {
        imageInput.click();
    });
    
    // Keyboard accessibility for upload zone
    uploadZone.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            imageInput.click();
        }
    });
    
    // Drag and Drop Handlers
    uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadZone.classList.add('drag-over');
    });
    
    uploadZone.addEventListener('dragleave', () => {
        uploadZone.classList.remove('drag-over');
    });
    
    uploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadZone.classList.remove('drag-over');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileSelection(files[0]);
        }
    });
    
    // File Input Change Handler
    imageInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelection(e.target.files[0]);
        }
    });
    
    // Handle File Selection
    function handleFileSelection(file) {
        // Validate file type
        const validTypes = ['image/jpeg', 'image/jpg', 'image/png'];
        if (!validTypes.includes(file.type)) {
            alert('Please select a JPG or PNG image');
            return;
        }
        
        // Validate file size (10MB)
        const maxSize = 10 * 1024 * 1024;
        if (file.size > maxSize) {
            alert('File size must be less than 10MB');
            return;
        }
        
        selectedFile = file;
        
        // Show preview
        const reader = new FileReader();
        reader.onload = (e) => {
            previewImage.src = e.target.result;
            previewSection.style.display = 'block';
            processBtn.disabled = false;
            
            // Update upload zone text
            const uploadText = uploadZone.querySelector('.upload-text');
            uploadText.textContent = `Selected: ${file.name}`;
        };
        reader.readAsDataURL(file);
        
        // Hide results if showing
        resultsSection.style.display = 'none';
        statusSection.style.display = 'none';
    }
    
    // Process Button Click Handler
    processBtn.addEventListener('click', async () => {
        if (!selectedFile) {
            alert('Please select an image first');
            return;
        }
        
        // Disable button during processing
        processBtn.disabled = true;
        
        // Show status section
        statusSection.style.display = 'block';
        resultsSection.style.display = 'none';
        processingMessage.textContent = 'Analyzing image and detecting text...';
        
        // Prepare form data
        const formData = new FormData();
        formData.append('image', selectedFile);
        formData.append('languages', languagesInput.value);
        formData.append('gpu', gpuCheckbox.checked);
        
        try {
            // Send OCR request
            const response = await fetch('/api/ocr', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'OCR processing failed');
            }
            
            const result = await response.json();
            currentResults = result;
            
            // Hide status, show results
            statusSection.style.display = 'none';
            displayResults(result);
            
        } catch (error) {
            console.error('Error:', error);
            // Show user-friendly error message
            const errorMessage = error.message || 'An error occurred during OCR processing';
            alert(`Error: ${errorMessage}`);
            statusSection.style.display = 'none';
            processBtn.disabled = false;
        }
    });
    
    // Display Results
    function displayResults(result) {
        // Show results section
        resultsSection.style.display = 'block';
        
        // Display annotated image
        annotatedImage.src = `data:image/jpeg;base64,${result.annotated_image}`;
        
        // Clear previous detections
        detectionsList.innerHTML = '';
        
        // Display detections
        if (result.detections && result.detections.length > 0) {
            result.detections.forEach((detection, index) => {
                const item = document.createElement('div');
                item.className = 'detection-item';
                
                const textDiv = document.createElement('div');
                textDiv.className = 'detection-text';
                textDiv.textContent = detection.text;
                
                const confidence = detection.confidence * 100;
                const confidenceDiv = document.createElement('div');
                confidenceDiv.className = 'detection-confidence';
                
                // Color code by confidence
                if (confidence >= 80) {
                    confidenceDiv.classList.add('confidence-high');
                } else if (confidence >= 50) {
                    confidenceDiv.classList.add('confidence-medium');
                } else {
                    confidenceDiv.classList.add('confidence-low');
                }
                
                confidenceDiv.textContent = `Confidence: ${confidence.toFixed(1)}%`;
                
                item.appendChild(textDiv);
                item.appendChild(confidenceDiv);
                detectionsList.appendChild(item);
            });
            
            // Calculate average confidence (with safety check)
            if (result.detections.length > 0) {
                const avgConfidence = result.detections.reduce((sum, d) => sum + d.confidence, 0) / result.detections.length * 100;
                avgConfidenceEl.textContent = `${avgConfidence.toFixed(1)}%`;
            } else {
                avgConfidenceEl.textContent = '0%';
            }
            
        } else {
            detectionsList.innerHTML = '<div class="detection-item"><div class="detection-text">No text detected in the image</div></div>';
            avgConfidenceEl.textContent = '0%';
        }
        
        // Update stats
        totalDetectionsEl.textContent = result.total_detections || 0;
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    
    // Copy Text Button Handler
    copyTextBtn.addEventListener('click', () => {
        if (!currentResults || !currentResults.detections) {
            return;
        }
        
        const allText = currentResults.detections.map(d => d.text).join('\n');
        
        navigator.clipboard.writeText(allText).then(() => {
            // Show feedback
            const originalText = copyTextBtn.textContent;
            copyTextBtn.textContent = '✓ Copied!';
            setTimeout(() => {
                copyTextBtn.textContent = originalText;
            }, 2000);
        }).catch(err => {
            console.error('Failed to copy:', err);
            alert('Failed to copy text to clipboard');
        });
    });
    
    // New Image Button Handler
    newImageBtn.addEventListener('click', () => {
        // Reset everything
        selectedFile = null;
        currentResults = null;
        imageInput.value = '';
        previewSection.style.display = 'none';
        resultsSection.style.display = 'none';
        statusSection.style.display = 'none';
        processBtn.disabled = true;
        
        const uploadText = uploadZone.querySelector('.upload-text');
        uploadText.textContent = 'Click to select or drag and drop an image';
        
        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
});
