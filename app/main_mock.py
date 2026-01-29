"""
Mock FastAPI application for testing UI (without EasyOCR dependency)
This version demonstrates the web interface without requiring the full EasyOCR installation
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List
import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime
import asyncio

# Initialize FastAPI app
app = FastAPI(
    title="EasyOCR Training API (Mock)",
    description="Web API for OCR model training and inference (Demo Mode)",
    version="1.0.0"
)

# Global variables for training state
training_state = {
    "status": "idle",
    "message": "",
    "progress": 0,
    "start_time": None,
    "end_time": None,
    "dataset": None,
    "results": None
}

# Paths
BASE_DIR = Path(__file__).parent.parent
STATIC_DIR = BASE_DIR / "app" / "static"
SAMPLE_DATASET_DIR = BASE_DIR / "data" / "sample_dataset"
UPLOAD_DIR = BASE_DIR / "data" / "uploads"

# Create upload directory if it doesn't exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


class TrainingRequest(BaseModel):
    """Request model for training"""
    dataset_type: str
    dataset_path: Optional[str] = None
    languages: List[str] = ["en"]
    gpu: bool = False


class TrainingStatus(BaseModel):
    """Response model for training status"""
    status: str
    message: str
    progress: int
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    dataset: Optional[str] = None
    results: Optional[dict] = None


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main UI page"""
    html_file = STATIC_DIR / "index.html"
    if not html_file.exists():
        raise HTTPException(status_code=404, detail="UI not found")
    
    with open(html_file, 'r') as f:
        return HTMLResponse(content=f.read())


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "EasyOCR Training API is running (Mock Mode)"}


@app.get("/api/datasets")
async def list_datasets():
    """List available datasets"""
    datasets = []
    
    if SAMPLE_DATASET_DIR.exists():
        labels_file = SAMPLE_DATASET_DIR / "labels.txt"
        if labels_file.exists():
            with open(labels_file, 'r') as f:
                sample_count = len(f.readlines())
            datasets.append({
                "name": "Sample Dataset",
                "type": "sample",
                "path": str(SAMPLE_DATASET_DIR),
                "image_count": sample_count
            })
    
    return {"datasets": datasets}


@app.post("/api/upload")
async def upload_dataset(
    files: List[UploadFile] = File(...),
    labels: UploadFile = File(...)
):
    """Upload a new dataset with images and labels"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        upload_path = UPLOAD_DIR / f"dataset_{timestamp}"
        upload_path.mkdir(parents=True, exist_ok=True)
        
        image_count = 0
        for file in files:
            if file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                file_path = upload_path / file.filename
                with open(file_path, 'wb') as f:
                    content = await file.read()
                    f.write(content)
                image_count += 1
        
        labels_path = upload_path / "labels.txt"
        with open(labels_path, 'wb') as f:
            content = await labels.read()
            f.write(content)
        
        return {
            "success": True,
            "message": f"Dataset uploaded successfully with {image_count} images",
            "dataset_path": str(upload_path),
            "image_count": image_count
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@app.post("/api/train")
async def start_training(request: TrainingRequest, background_tasks: BackgroundTasks):
    """Start a training job"""
    global training_state
    
    if training_state["status"] == "running":
        raise HTTPException(status_code=400, detail="Training is already in progress")
    
    if request.dataset_type == "sample":
        dataset_path = SAMPLE_DATASET_DIR
    elif request.dataset_type == "uploaded":
        if not request.dataset_path:
            raise HTTPException(status_code=400, detail="Dataset path required")
        dataset_path = Path(request.dataset_path)
    else:
        raise HTTPException(status_code=400, detail="Invalid dataset type")
    
    if not dataset_path.exists():
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    labels_file = dataset_path / "labels.txt"
    if not labels_file.exists():
        raise HTTPException(status_code=404, detail="Labels file not found")
    
    training_state = {
        "status": "running",
        "message": "Training started",
        "progress": 0,
        "start_time": datetime.now().isoformat(),
        "end_time": None,
        "dataset": str(dataset_path),
        "results": None
    }
    
    background_tasks.add_task(run_mock_training, dataset_path=dataset_path)
    
    return {
        "success": True,
        "message": "Training job started (Mock Mode - simulated)",
        "status": training_state["status"]
    }


async def run_mock_training(dataset_path: Path):
    """Mock training job that simulates OCR validation"""
    global training_state
    
    try:
        training_state["message"] = "Initializing OCR model (Mock)..."
        training_state["progress"] = 10
        await asyncio.sleep(2)
        
        training_state["message"] = "Loading dataset..."
        training_state["progress"] = 20
        
        labels_file = dataset_path / "labels.txt"
        dataset_samples = []
        with open(labels_file, 'r') as f:
            for line in f:
                if '\t' in line:
                    filename, text = line.strip().split('\t', 1)
                    dataset_samples.append((filename, text))
        
        await asyncio.sleep(2)
        
        # Simulate processing
        training_state["message"] = "Processing images (Mock)..."
        total_samples = len(dataset_samples)
        results_detail = []
        
        # Simulate high accuracy for mock
        import random
        correct_predictions = 0
        
        for i, (filename, ground_truth) in enumerate(dataset_samples):
            # Mock prediction (90% accuracy)
            is_correct = random.random() > 0.1
            predicted_text = ground_truth if is_correct else ground_truth + " (simulated error)"
            
            if is_correct:
                correct_predictions += 1
            
            results_detail.append({
                "filename": filename,
                "ground_truth": ground_truth,
                "predicted": predicted_text,
                "correct": is_correct
            })
            
            progress = 20 + int((i + 1) / total_samples * 70)
            training_state["progress"] = progress
            training_state["message"] = f"Processing image {i + 1}/{total_samples}"
            
            await asyncio.sleep(1)
        
        accuracy = (correct_predictions / total_samples * 100) if total_samples > 0 else 0
        
        training_state["status"] = "completed"
        training_state["message"] = "Training completed (Mock)"
        training_state["progress"] = 100
        training_state["end_time"] = datetime.now().isoformat()
        training_state["results"] = {
            "total_samples": total_samples,
            "correct_predictions": correct_predictions,
            "accuracy": round(accuracy, 2),
            "details": results_detail
        }
        
    except Exception as e:
        training_state["status"] = "failed"
        training_state["message"] = f"Training failed: {str(e)}"
        training_state["progress"] = 0
        training_state["end_time"] = datetime.now().isoformat()


@app.get("/api/status", response_model=TrainingStatus)
async def get_training_status():
    """Get the current training status"""
    return TrainingStatus(**training_state)


@app.post("/api/reset")
async def reset_training():
    """Reset the training state"""
    global training_state
    
    training_state = {
        "status": "idle",
        "message": "",
        "progress": 0,
        "start_time": None,
        "end_time": None,
        "dataset": None,
        "results": None
    }
    
    return {"success": True, "message": "Training state reset"}


@app.get("/api/sample-dataset")
async def get_sample_dataset_info():
    """Get information about the sample dataset"""
    if not SAMPLE_DATASET_DIR.exists():
        raise HTTPException(status_code=404, detail="Sample dataset not found")
    
    labels_file = SAMPLE_DATASET_DIR / "labels.txt"
    if not labels_file.exists():
        raise HTTPException(status_code=404, detail="Labels file not found")
    
    samples = []
    with open(labels_file, 'r') as f:
        for line in f:
            if '\t' in line:
                filename, text = line.strip().split('\t', 1)
                samples.append({
                    "filename": filename,
                    "text": text
                })
    
    return {
        "path": str(SAMPLE_DATASET_DIR),
        "sample_count": len(samples),
        "samples": samples
    }


@app.get("/api/sample-image/{filename}")
async def get_sample_image(filename: str):
    """Serve a sample dataset image"""
    # Sanitize filename to prevent path traversal
    safe_filename = Path(filename).name
    if not safe_filename or safe_filename.startswith('.'):
        raise HTTPException(status_code=400, detail="Invalid filename")
    
    image_path = SAMPLE_DATASET_DIR / safe_filename
    
    if not image_path.exists() or not image_path.is_file():
        raise HTTPException(status_code=404, detail="Image not found")
    
    # Verify it's an image file
    if not image_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    return FileResponse(image_path)


@app.post("/api/ocr")
async def perform_ocr(
    image: UploadFile = File(...),
    languages: str = "en",
    gpu: bool = False
):
    """
    Mock OCR endpoint - returns simulated OCR results
    """
    try:
        import base64
        
        # Validate file type
        if not image.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            raise HTTPException(status_code=400, detail="Only JPG and PNG images are supported")
        
        # Read the image content
        content = await image.read()
        
        # Validate file size (10MB max)
        max_file_size = 10 * 1024 * 1024
        if len(content) > max_file_size:
            raise HTTPException(status_code=400, detail="File size exceeds 10MB limit")
        
        # Convert image to base64 for mock response
        image_b64 = base64.b64encode(content).decode('utf-8')
        
        # Mock OCR results
        mock_detections = [
            {
                "text": "Hello World",
                "confidence": 0.95,
                "bbox": [[10, 10], [200, 10], [200, 50], [10, 50]]
            },
            {
                "text": "This is a demo",
                "confidence": 0.92,
                "bbox": [[10, 60], [250, 60], [250, 100], [10, 100]]
            },
            {
                "text": "EasyOCR Test",
                "confidence": 0.88,
                "bbox": [[10, 110], [220, 110], [220, 150], [10, 150]]
            }
        ]
        
        return {
            "success": True,
            "detections": mock_detections,
            "annotated_image": image_b64,  # In real version, this would be the image with boxes drawn
            "total_detections": len(mock_detections)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    print("Starting FastAPI Mock Server...")
    print("This is a demonstration version without EasyOCR dependency")
    uvicorn.run(app, host="0.0.0.0", port=8000)
