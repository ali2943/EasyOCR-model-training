# Visual Getting Started Guide

This guide provides a visual walkthrough of using the EasyOCR Training application.

## 📋 Table of Contents
1. [Installation](#installation)
2. [Starting the Web UI](#starting-the-web-ui)
3. [Using the Dashboard](#using-the-dashboard)
4. [Sample Dataset Gallery](#sample-dataset-gallery)
5. [Training Process](#training-process)
6. [Viewing Results](#viewing-results)

## 📦 Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/ali2943/EasyOCR-model-training.git
cd EasyOCR-model-training
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

The installation includes:
- ✅ EasyOCR - For OCR functionality
- ✅ FastAPI - Web framework
- ✅ Uvicorn - ASGI server
- ✅ Pillow - Image processing
- ✅ OpenCV - Computer vision
- ✅ PyTorch - Deep learning framework

## 🚀 Starting the Web UI

Launch the web application:

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Open your browser and navigate to: **http://localhost:8000**

## 🎨 Using the Dashboard

### Main Dashboard Features

The web UI consists of several key sections:

#### 1. **Dataset Selection**
- Choose between sample dataset or upload your own
- Radio buttons for easy selection
- Sample dataset automatically loaded

#### 2. **Sample Dataset Gallery**
- Visual preview of all 15 sample images
- Interactive gallery with hover effects
- Each image shows filename and text content
- Grid layout for easy browsing

#### 3. **Training Configuration**
- Language selection (default: English)
- GPU toggle (if available)
- Simple, intuitive controls

#### 4. **Training Progress**
- Real-time status updates
- Progress bar with percentage
- Color-coded status badges:
  - **Gray**: Idle
  - **Orange**: Running
  - **Green**: Completed
  - **Red**: Failed

#### 5. **Results Display**
- Accuracy percentage
- Total samples processed
- Correct predictions count
- Detailed per-image results table

## 🖼️ Sample Dataset Gallery

The sample dataset includes 15 diverse images:

### Text Variations
1. **Regular Text** - Standard font, clear and simple
2. **Bold Text** - Heavy weight for emphasis
3. **Italic Text** - Slanted for style
4. **Monospaced** - Fixed-width for code/numbers

### Content Types
- Simple phrases: "Hello World", "Machine Learning"
- Technical terms: "Optical Character Recognition"
- Numbers: "1234567890"
- Special characters: "@#$%&*"
- Emails: "test@example.com"
- URLs: "www.example.org"

### Visual Elements
- Different background colors
- Border decorations
- Various text sizes
- Multiple line lengths

## 🎯 Training Process

### Step-by-Step Workflow

**Step 1: Select Dataset**
- Default: Sample dataset (15 images)
- Alternative: Upload your own dataset

**Step 2: Configure Settings**
- Set language (e.g., `en` for English)
- Enable GPU if available
- Click "Start Training"

**Step 3: Monitor Progress**
- Watch real-time progress bar
- Read status messages
- See current processing step

**Step 4: Review Results**
- Automatic display when complete
- Summary statistics at the top
- Detailed table below

### Training Timeline

Typical training run on sample dataset:
- **Initialization**: 1-2 seconds
- **Dataset Loading**: 1 second
- **Image Processing**: 5-10 seconds
- **Total Time**: ~15 seconds

## 📊 Viewing Results

### Results Summary

The results section shows three key metrics:

1. **Accuracy** - Percentage of correct predictions
2. **Total Samples** - Number of images processed
3. **Correct Predictions** - Count of accurate results

### Detailed Results Table

For each image:
- **Filename** - Image identifier
- **Ground Truth** - Expected text
- **Predicted** - OCR output
- **Status** - ✓ Correct or ✗ Wrong

### Understanding Results

- **High Accuracy (>90%)**: Model performs well on this dataset
- **Medium Accuracy (70-90%)**: Some challenging images
- **Low Accuracy (<70%)**: Dataset may be too complex or diverse

## 🔄 Workflow Diagram

![Training Workflow](images/workflow.png)

## 🏗️ System Architecture

![System Architecture](images/architecture.png)

## 💡 Tips & Tricks

### Optimizing Performance
1. Use GPU if available for faster processing
2. Start with the sample dataset to familiarize yourself
3. Keep custom datasets under 100 images for best experience

### Custom Datasets
1. Prepare images (JPG or PNG)
2. Create labels.txt in format: `filename<TAB>text`
3. Upload through the web UI
4. Start training

### Troubleshooting
- **Slow Performance**: Try CPU mode if GPU causes issues
- **Low Accuracy**: Ensure labels.txt matches image content exactly
- **Upload Failed**: Check file formats and sizes

## 🎓 Next Steps

After getting started:

1. **Experiment with Languages**: Try `en,fr,de` for multi-language
2. **Upload Custom Data**: Use your own OCR datasets
3. **Explore the API**: Check `/docs` for API documentation
4. **Integrate in Code**: Use the EasyOCRModel class directly

## 📚 Additional Resources

- Main README: Comprehensive project documentation
- API Docs: http://localhost:8000/docs (when server running)
- Sample Dataset README: Details about the dataset format
- QUICKSTART.md: Quick reference guide

## ✨ Key Features Recap

![Features Showcase](images/features.png)

- 🖼️ **Image OCR**: Accurate text extraction
- 📊 **Web Dashboard**: User-friendly interface
- 🌍 **Multi-language**: Support for 80+ languages
- ⚡ **Fast Processing**: Quick training and validation
- 📈 **Analytics**: Detailed metrics and results
- 🔧 **Easy Setup**: Simple pip install and run

## 🎉 You're Ready!

You now have everything you need to start using EasyOCR Training. Happy training! 🚀
