# Sample OCR Training Dataset

This directory contains a comprehensive sample dataset for OCR training demonstrations with diverse text styles and content types.

## Dataset Structure

The dataset follows a simple format suitable for OCR training:

```
data/sample_dataset/
├── image_001.jpg       # Sample image 1
├── image_002.jpg       # Sample image 2
├── ...
├── image_015.jpg       # Sample image 15
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
image_009.jpg	BOLD TEXT EXAMPLE
```

Each line contains:
1. **Filename**: The name of the image file
2. **Text**: The ground truth text that appears in the image

## Dataset Contents

The sample dataset includes **15 diverse images** with various text styles and content types:

### Regular Text (Images 1-8)
- Hello World
- Machine Learning
- Optical Character Recognition
- Deep Learning OCR
- Training Dataset
- Sample Text 123
- Python FastAPI
- EasyOCR Model

### Diverse Styles (Images 9-15)
- **BOLD TEXT EXAMPLE** (Bold font)
- *Italic Style Text* (Italic font)
- `Numbers: 1234567890` (Monospaced font with numbers)
- Special @#$%&* Chars (Special characters)
- Light Background (Different background color with border)
- Email: test@example.com (Email format)
- Website: www.example.org (URL format)

## Visual Features

The dataset showcases:
- ✅ **Multiple font styles**: Regular, Bold, Italic, Monospaced
- ✅ **Various content types**: Text, numbers, special characters, emails, URLs
- ✅ **Different backgrounds**: White, light gray
- ✅ **Visual elements**: Some images include borders
- ✅ **Different sizes**: Varied text lengths and image dimensions

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
4. Browse the visual gallery of all 15 sample images
5. Click "Start Training"

The training process will use these images and their corresponding labels for demonstration purposes.

## Notes

- Images are generated programmatically using PIL/Pillow
- Designed to demonstrate OCR capabilities across different text styles
- Real OCR training datasets would typically be more complex and varied
- The dataset is optimized for quick testing and demonstration
- All images are stored as JPG format for consistency
