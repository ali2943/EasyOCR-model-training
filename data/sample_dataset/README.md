# Sample OCR Training Dataset

This directory contains a small sample dataset for OCR training demonstrations.

## Dataset Structure

The dataset follows a simple format suitable for OCR training:

```
data/sample_dataset/
├── image_001.jpg       # Sample image 1
├── image_002.jpg       # Sample image 2
├── ...
├── image_008.jpg       # Sample image 8
├── labels.txt          # Ground truth labels
├── create_dataset.py   # Script to regenerate dataset
└── README.md           # This file
```

## Labels Format

The `labels.txt` file contains the ground truth text for each image in a tab-separated format:

```
<filename><TAB><text>
```

Example:
```
image_001.jpg	Hello World
image_002.jpg	Machine Learning
```

Each line contains:
1. **Filename**: The name of the image file
2. **Text**: The ground truth text that appears in the image

## Dataset Contents

The sample dataset includes 8 images with the following texts:
- Hello World
- Machine Learning
- Optical Character Recognition
- Deep Learning OCR
- Training Dataset
- Sample Text 123
- Python FastAPI
- EasyOCR Model

## Regenerating the Dataset

If you need to regenerate the dataset (e.g., after modifications):

```bash
cd data/sample_dataset
python create_dataset.py
```

This will create new images and update the labels.txt file.

## Usage

This dataset can be used with the FastAPI web app to demonstrate OCR training functionality:

1. Start the FastAPI server
2. Navigate to the web UI
3. Select "Use Sample Dataset" option
4. Click "Start Training"

The training process will use these images and their corresponding labels for demonstration purposes.

## Notes

- Images are simple text-on-white-background for demonstration
- Real OCR training datasets would be more complex and varied
- This dataset is intentionally kept small for quick testing
- Images are generated programmatically using PIL/Pillow
