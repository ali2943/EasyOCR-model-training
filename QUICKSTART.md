# FastAPI Web App Quick Start Guide

This guide will help you get started with the EasyOCR Training web application.

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

## Installation

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone https://github.com/ali2943/EasyOCR-model-training.git
   cd EasyOCR-model-training
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   This will install:
   - FastAPI - Web framework
   - Uvicorn - ASGI server
   - EasyOCR - OCR library
   - And all other required dependencies

## Running the Application

### Option 1: Using the Full Application (with EasyOCR)

Start the FastAPI server:
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Option 2: Using the Mock Server (for Testing)

If you want to test the UI without installing the heavy EasyOCR dependencies:
```bash
python app/main_mock.py
```

### Access the Web UI

Open your browser and navigate to:
```
http://localhost:8000
```

## Using the Web Interface

### 1. Select a Dataset

**Option A: Use Sample Dataset**
- Click the "Use Sample Dataset" radio button (selected by default)
- You'll see a preview of 8 sample images with their labels

**Option B: Upload Custom Dataset**
- Click the "Upload Custom Dataset" radio button
- Select your image files (JPG, PNG)
- Select your labels.txt file
- Click "Upload Dataset"

### 2. Configure Training

- **Languages**: Comma-separated language codes (e.g., "en" for English, "en,es,fr" for multiple)
- **GPU**: Check this box if you have CUDA-enabled GPU (optional)

### 3. Start Training

- Click the "🚀 Start Training" button
- Watch the progress bar update in real-time
- View status messages as the training progresses

### 4. View Results

After training completes, you'll see:
- **Accuracy**: Overall accuracy percentage
- **Total Samples**: Number of images processed
- **Correct Predictions**: Number of correct OCR predictions
- **Detailed Results Table**: Per-image results with ground truth vs predicted text

## API Endpoints

The application provides the following REST API endpoints:

### GET /
Serves the main web UI

### GET /api/health
Health check endpoint
```bash
curl http://localhost:8000/api/health
```

### GET /api/sample-dataset
Get information about the sample dataset
```bash
curl http://localhost:8000/api/sample-dataset
```

### POST /api/train
Start a training job
```bash
curl -X POST http://localhost:8000/api/train \
  -H "Content-Type: application/json" \
  -d '{"dataset_type": "sample", "languages": ["en"], "gpu": false}'
```

### GET /api/status
Get current training status
```bash
curl http://localhost:8000/api/status
```

### POST /api/reset
Reset training state
```bash
curl -X POST http://localhost:8000/api/reset
```

## Dataset Format

The application expects datasets in the following format:

```
dataset_directory/
├── image_001.jpg
├── image_002.jpg
├── ...
└── labels.txt
```

The `labels.txt` file should contain tab-separated values:
```
image_001.jpg	Hello World
image_002.jpg	Machine Learning
```

Format: `<filename><TAB><text>`

## Sample Dataset

The repository includes a sample dataset in `data/sample_dataset/` with:
- 8 sample images
- Corresponding labels.txt file
- Script to regenerate the dataset

See `data/sample_dataset/README.md` for more information.

## Troubleshooting

### Server won't start
- Make sure port 8000 is not already in use
- Check that all dependencies are installed: `pip install -r requirements.txt`

### EasyOCR models downloading
- On first run, EasyOCR will download model files (~100MB)
- This only happens once
- Models are cached in `~/.EasyOCR/`

### Out of memory
- If you run out of memory, try:
  - Using CPU instead of GPU (uncheck GPU option)
  - Processing fewer images at once
  - Reducing image sizes

## Development

### Running Tests

Validate the application structure:
```bash
python test_app_structure.py
```

### API Documentation

FastAPI provides automatic API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Support

For issues or questions:
1. Check the main README.md
2. Review the sample dataset documentation
3. Open an issue on GitHub

## Next Steps

- Try the sample dataset to familiarize yourself with the UI
- Upload your own OCR dataset
- Experiment with different language configurations
- Explore the API endpoints for programmatic access
