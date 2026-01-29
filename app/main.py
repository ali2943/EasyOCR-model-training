"""
FastAPI application for EasyOCR training
Provides a web UI for OCR training with dataset upload and management
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

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from easy_ocr_model import EasyOCRModel

# Initialize FastAPI app
app = FastAPI(
    title="EasyOCR Training API",
    description="Web API for OCR model training and inference",
    version="1.0.0"
)

# Global variables for training state
# Note: In production with multiple workers, use a proper state management solution
# like Redis, database, or in-memory cache with locking mechanisms
training_state = {
    "status": "idle",  # idle, running, completed, failed
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
    dataset_type: str  # "sample" or "uploaded"
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
    return {"status": "healthy", "message": "EasyOCR Training API is running"}


@app.get("/api/datasets")
async def list_datasets():
    """List available datasets"""
    datasets = []
    
    # Add sample dataset
    if SAMPLE_DATASET_DIR.exists():
        labels_file = SAMPLE_DATASET_DIR / "labels.txt"
        if labels_file.exists():
            with open(labels_file, 'r', encoding='utf-8') as f:
                sample_count = len([line for line in f if line.strip()])
            datasets.append({
                "name": "Sample Dataset",
                "type": "sample",
                "path": str(SAMPLE_DATASET_DIR),
                "image_count": sample_count
            })
    
    # Add uploaded datasets
    if UPLOAD_DIR.exists():
        for dataset_dir in UPLOAD_DIR.iterdir():
            if dataset_dir.is_dir():
                labels_file = dataset_dir / "labels.txt"
                if labels_file.exists():
                    with open(labels_file, 'r', encoding='utf-8') as f:
                        upload_count = len([line for line in f if line.strip()])
                    datasets.append({
                        "name": dataset_dir.name,
                        "type": "uploaded",
                        "path": str(dataset_dir),
                        "image_count": upload_count
                    })
    
    return {"datasets": datasets}


@app.post("/api/upload")
async def upload_dataset(
    files: List[UploadFile] = File(...),
    labels: UploadFile = File(...)
):
    """Upload a new dataset with images and labels"""
    try:
        # Validate number of files
        if len(files) > 100:
            raise HTTPException(status_code=400, detail="Maximum 100 files allowed per upload")
        
        # Create a new upload directory with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        upload_path = UPLOAD_DIR / f"dataset_{timestamp}"
        upload_path.mkdir(parents=True, exist_ok=True)
        
        # Save images with validation
        image_count = 0
        max_file_size = 10 * 1024 * 1024  # 10MB per file
        
        for file in files:
            if file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                # Sanitize filename to prevent path traversal
                safe_filename = Path(file.filename).name
                if not safe_filename or safe_filename.startswith('.'):
                    continue
                
                file_path = upload_path / safe_filename
                content = await file.read()
                
                # Validate file size
                if len(content) > max_file_size:
                    raise HTTPException(status_code=400, detail=f"File {safe_filename} exceeds 10MB limit")
                
                with open(file_path, 'wb') as f:
                    f.write(content)
                image_count += 1
        
        # Save and validate labels file
        labels_path = upload_path / "labels.txt"
        labels_content = await labels.read()
        
        # Validate labels file size
        if len(labels_content) > 1024 * 1024:  # 1MB max for labels
            raise HTTPException(status_code=400, detail="Labels file exceeds 1MB limit")
        
        # Validate labels file is valid UTF-8 text
        try:
            labels_text = labels_content.decode('utf-8')
        except UnicodeDecodeError:
            raise HTTPException(status_code=400, detail="Labels file must be valid UTF-8 text")
        
        # Validate format (each line should have tab-separated values)
        lines = [line for line in labels_text.strip().split('\n') if line.strip()]
        for i, line in enumerate(lines):
            if '\t' not in line:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Invalid labels format at line {i+1}. Expected: filename<TAB>text"
                )
        
        with open(labels_path, 'w', encoding='utf-8') as f:
            f.write(labels_text)
        
        return {
            "success": True,
            "message": f"Dataset uploaded successfully with {image_count} images",
            "dataset_path": str(upload_path),
            "image_count": image_count
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@app.post("/api/train")
async def start_training(request: TrainingRequest, background_tasks: BackgroundTasks):
    """Start a training job"""
    global training_state
    
    # Validate languages
    if not request.languages or not all(lang.strip() for lang in request.languages):
        raise HTTPException(status_code=400, detail="At least one valid language code is required")
    if training_state["status"] == "running":
        raise HTTPException(status_code=400, detail="Training is already in progress")
    
    # Validate dataset
    if request.dataset_type == "sample":
        dataset_path = SAMPLE_DATASET_DIR
    elif request.dataset_type == "uploaded":
        if not request.dataset_path:
            raise HTTPException(status_code=400, detail="Dataset path required for uploaded datasets")
        dataset_path = Path(request.dataset_path)
    else:
        raise HTTPException(status_code=400, detail="Invalid dataset type")
    
    if not dataset_path.exists():
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    labels_file = dataset_path / "labels.txt"
    if not labels_file.exists():
        raise HTTPException(status_code=404, detail="Labels file not found in dataset")
    
    # Initialize training state
    training_state = {
        "status": "running",
        "message": "Training started",
        "progress": 0,
        "start_time": datetime.now().isoformat(),
        "end_time": None,
        "dataset": str(dataset_path),
        "results": None
    }
    
    # Start training in background
    background_tasks.add_task(
        run_training_job,
        dataset_path=dataset_path,
        languages=request.languages,
        gpu=request.gpu
    )
    
    return {
        "success": True,
        "message": "Training job started",
        "status": training_state["status"]
    }


async def run_training_job(dataset_path: Path, languages: List[str], gpu: bool):
    """
    Background task to run training/validation job
    
    Note: This is a demonstration function that validates the OCR model
    against the dataset. In a real training scenario, this would involve
    actual model fine-tuning.
    """
    global training_state
    
    try:
        # Update progress
        training_state["message"] = "Initializing OCR model..."
        training_state["progress"] = 10
        
        # Initialize the EasyOCR model
        model = EasyOCRModel(languages=languages, gpu=gpu)
        await asyncio.sleep(1)  # Simulate initialization time
        
        # Read labels
        training_state["message"] = "Loading dataset..."
        training_state["progress"] = 20
        
        labels_file = dataset_path / "labels.txt"
        dataset_samples = []
        with open(labels_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and '\t' in line:
                    filename, text = line.split('\t', 1)
                    dataset_samples.append((filename, text))
        
        await asyncio.sleep(1)
        
        # Process each image (simulating training/validation)
        training_state["message"] = "Processing images..."
        total_samples = len(dataset_samples)
        correct_predictions = 0
        results_detail = []
        
        for i, (filename, ground_truth) in enumerate(dataset_samples):
            image_path = dataset_path / filename
            
            if image_path.exists():
                # Run OCR on the image
                predicted_text = model.get_full_text(image_path)
                
                # Check if prediction matches ground truth
                is_correct = predicted_text.strip().lower() == ground_truth.strip().lower()
                if is_correct:
                    correct_predictions += 1
                
                results_detail.append({
                    "filename": filename,
                    "ground_truth": ground_truth,
                    "predicted": predicted_text,
                    "correct": is_correct
                })
            
            # Update progress
            progress = 20 + int((i + 1) / total_samples * 70)
            training_state["progress"] = progress
            training_state["message"] = f"Processing image {i + 1}/{total_samples}"
            
            # Small delay for demonstration purposes (can be removed in production)
            await asyncio.sleep(0.5)
        
        # Calculate accuracy
        accuracy = (correct_predictions / total_samples * 100) if total_samples > 0 else 0
        
        # Training completed successfully
        training_state["status"] = "completed"
        training_state["message"] = "Training completed successfully"
        training_state["progress"] = 100
        training_state["end_time"] = datetime.now().isoformat()
        training_state["results"] = {
            "total_samples": total_samples,
            "correct_predictions": correct_predictions,
            "accuracy": round(accuracy, 2),
            "details": results_detail
        }
        
    except Exception as e:
        # Training failed
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
    with open(labels_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and '\t' in line:
                filename, text = line.split('\t', 1)
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


@app.post("/api/detect")
async def detect_text(file: UploadFile = File(...)):
    """
    Detect text in an uploaded image and return bounding boxes
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Validate file size (10MB max)
        max_file_size = 10 * 1024 * 1024
        content = await file.read()
        if len(content) > max_file_size:
            raise HTTPException(status_code=400, detail="File size exceeds 10MB limit")
        
        # Save the uploaded file temporarily
        temp_dir = Path("/tmp/ocr_uploads")
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"upload_{timestamp}_{Path(file.filename).name}"
        temp_file = temp_dir / safe_filename
        
        with open(temp_file, 'wb') as f:
            f.write(content)
        
        # Initialize OCR model (using English by default)
        model = EasyOCRModel(languages=['en'], gpu=False)
        
        # Perform OCR
        results = model.read_image(str(temp_file))
        
        # Format results
        formatted_results = []
        for bbox, text, confidence in results:
            formatted_results.append({
                "bbox": bbox,
                "text": text,
                "confidence": float(confidence)
            })
        
        # Clean up temporary file
        try:
            temp_file.unlink()
        except Exception:
            pass
        
        return {
            "success": True,
            "results": formatted_results,
            "count": len(formatted_results)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Detection failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
